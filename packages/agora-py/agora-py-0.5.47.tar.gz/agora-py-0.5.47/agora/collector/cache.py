# coding=utf-8
"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Ontology Engineering Group
        http://www.oeg-upm.net/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2016 Ontology Engineering Group.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""

import calendar
import logging
import math
import shutil
import zlib
from StringIO import StringIO
from datetime import datetime as dt, timedelta as delta
from threading import Thread, Lock as TLock
from time import sleep

import shortuuid
from concurrent.futures import ThreadPoolExecutor
from rdflib import ConjunctiveGraph
from rdflib.graph import Graph
from redis import ConnectionError
from redis.lock import Lock

from agora.collector.execution import parse_rdf
from agora.collector.http import http_get, extract_ttl
from agora.engine.utils import stopped
from agora.engine.utils.graph import get_triple_store
from agora.engine.utils.kv import get_kv

__author__ = 'Fernando Serena'

log = logging.getLogger('agora.collector.cache')


class RedisCache(object):
    tpool = ThreadPoolExecutor(max_workers=1)

    def __init__(self, persist_mode=None, key_prefix='', min_cache_time=5, force_cache_time=False,
                 base='store', path='cache', redis_host='localhost', redis_port=6379, redis_db=1, redis_file=None,
                 graph_memory_limit=5000):
        self.__key_prefix = key_prefix
        self.__cache_key = '{}:cache'.format(key_prefix)
        self.__persist_mode = persist_mode
        self.__min_cache_time = min_cache_time
        self.__force_cache_time = force_cache_time
        self.__base_path = base
        self._r = get_kv(persist_mode, redis_host, redis_port, redis_db, redis_file, base=base, path=path)
        self.__lock = Lock(self._r, key_prefix)
        self.__mlock = TLock()
        self.__graph_memory_limit = graph_memory_limit
        self.__memory_graphs = {}
        self.__memory_order = []

        self.__resources_ts = {}

        for lock_key in self._r.keys('{}:l*'.format(self.__key_prefix)):
            self._r.delete(lock_key)

        self._r.delete(key_prefix)

        self.__enabled = True
        self.__purge_th = Thread(target=self.__purge)
        self.__purge_th.daemon = True
        self.__purge_th.start()

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    @property
    def min_cache_time(self):
        return self.__min_cache_time

    @min_cache_time.setter
    def min_cache_time(self, t):
        self.__min_cache_time = t

    @property
    def resource_cache(self):
        return self.__resource_cache

    @resource_cache.setter
    def resource_cache(self, rc):
        self.__resource_cache = rc

    @property
    def persist_mode(self):
        return self.__persist_mode

    @property
    def base_path(self):
        return self.__base_path

    def __clean(self, name):
        shutil.rmtree('{}/{}'.format(self.__base_path, name))

    def uri_lock(self, uri):
        with self.__lock:
            key = '{}:l:'.format(self.__key_prefix) + uri
            key = (key[:250]) if len(key) > 250 else key
            return Lock(self._r, key)

    def __purge(self):
        try:
            gids_key = '{}:gids'.format(self.__cache_key)
            while self.__enabled and not stopped.isSet():
                try:
                    gids = self._r.hkeys(gids_key)
                    obsolete = filter(
                        lambda x: not self._r.exists('{}:{}'.format(self.__cache_key, self._r.hget(gids_key, x))),
                        gids)

                    if obsolete:
                        with self._r.pipeline(transaction=True) as p:
                            p.multi()
                            log.debug('Removing {} resouces from cache...'.format(len(obsolete)))
                            for uri in obsolete:
                                lock = self.uri_lock(uri)
                                with lock:
                                    try:
                                        self._r.hdel(gids_key, uri)
                                        self.__forget(uri)
                                    except Exception:
                                        # traceback.print_exc()
                                        log.error('Purging resource {}'.format(uri))
                                    p.execute()
                except Exception, e:
                    if not stopped.isSet():
                        log.error(e.message)
                    self.__enabled = False
                sleep(10)
        except ConnectionError as e:
            raise EnvironmentError(e.message)

    def __memoize(self, key, graph):
        with self.__mlock:
            if len(self.__memory_order) >= self.__graph_memory_limit:
                old_key = self.__memory_order.pop(0)
                if old_key in self.__memory_graphs:
                    del self.__memory_graphs[old_key]

            self.__memory_order.append(key)
            self.__memory_graphs[key] = graph

    def __recall(self, key):
        with self.__mlock:
            return self.__memory_graphs[key]

    def __forget(self, key):
        with self.__mlock:
            try:
                if key in self.__memory_graphs:
                    del self.__memory_graphs[key]
                    self.__memory_order.remove(key)
            except:
                pass

    def release_locks(self):
        try:
            with self.__lock:
                lock_keys = self._r.keys('{}:l:*'.format(self.__key_prefix))
                for k in lock_keys:
                    self._r.delete(k)
        except ConnectionError as e:
            raise EnvironmentError(e.message)

    def create(self, conjunctive=False, gid=None, loader=None, format=None):
        try:
            if conjunctive:
                uuid = shortuuid.uuid()
                g = get_triple_store(self.__persist_mode, base=self.__base_path, path=uuid)
                return g
            else:
                p = self._r.pipeline(transaction=True)
                p.multi()

                g = Graph(identifier=gid)

                lock = self.uri_lock(gid)
                with lock:
                    uuid = self._r.hget('{}:gids'.format(self.__cache_key), gid)
                    if not uuid:
                        uuid = shortuuid.uuid()
                        p.hset('{}:gids'.format(self.__cache_key), gid, uuid)

                    gid_key = '{}:{}'.format(self.__cache_key, uuid)

                    ttl_ts = self._r.hget(gid_key, 'ttl')
                    if ttl_ts is not None:
                        ttl_dt = dt.utcfromtimestamp(int(ttl_ts))
                        now = dt.utcnow()
                        if ttl_dt > now:
                            try:
                                g = self.__recall(gid)
                            except KeyError:
                                source_z = self._r.hget(gid_key, 'data')
                                source = zlib.decompress(source_z)
                                g.parse(StringIO(source), format=format)
                                self.__memoize(gid, g)

                            ttl = math.ceil((ttl_dt - dt.utcnow()).total_seconds())
                            return g, math.ceil(ttl)

                    log.debug('Caching {}'.format(gid))
                    response = loader(gid, format)
                    if response is None and loader != http_get:
                        response = http_get(gid, format)

                    if isinstance(response, bool):
                        return response

                    ttl = self.__min_cache_time
                    source, headers = response
                    if not isinstance(source, Graph) and not isinstance(source, ConjunctiveGraph):
                        parse_rdf(g, source, format, headers)
                        data = g.serialize(format='turtle')
                    else:
                        data = source.serialize(format='turtle')
                        for prefix, ns in source.namespaces():
                            g.bind(prefix, ns)
                        g.__iadd__(source)

                    self.__memoize(gid, g)

                    if not self.__force_cache_time:
                        ttl = extract_ttl(headers) or ttl

                    p.hset(gid_key, 'data', zlib.compress(data))
                    ttl_ts = calendar.timegm((dt.utcnow() + delta(seconds=ttl)).timetuple())
                    p.hset(gid_key, 'ttl', ttl_ts)
                    p.expire(gid_key, ttl)
                    p.execute()
                return g, int(ttl)
        except ConnectionError as e:
            raise EnvironmentError(e.message)

    def release(self, g):
        if isinstance(g, ConjunctiveGraph):
            if self.__persist_mode:
                RedisCache.tpool.submit(self.__clean, g.identifier.toPython())
            else:
                g.remove((None, None, None))

    def expire(self, gid):
        try:
            lock = self.uri_lock(gid)
            with lock:
                uuid = self._r.hget('{}:gids'.format(self.__cache_key), gid)
                with self._r.pipeline(transaction=True) as p:
                    if not uuid:
                        uuid = shortuuid.uuid()
                        p.hset('{}:gids'.format(self.__cache_key), gid, uuid)

                    gid_key = '{}:{}'.format(self.__cache_key, uuid)
                    p.delete(gid_key)
                    p.execute()
        except ConnectionError as e:
            raise EnvironmentError(e.message)

    def get_matching_uris(self, part):
        return filter(lambda gid: part in gid, self._r.hkeys('{}:gids'.format(self.__cache_key)))

    def close(self):
        self.__enabled = False
