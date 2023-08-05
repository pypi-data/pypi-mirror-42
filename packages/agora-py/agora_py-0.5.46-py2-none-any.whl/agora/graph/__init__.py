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

import logging

import rdflib
from rdflib import BNode
from rdflib import ConjunctiveGraph
from rdflib import Graph
from rdflib import Literal
from rdflib import RDF
from rdflib import RDFS
from rdflib import URIRef
from rdflib import Variable
from rdflib import plugin

from agora.engine.plan.agp import TP, AGP
from agora.engine.plan.graph import AGORA

__author__ = 'Fernando Serena'

log = logging.getLogger('agora.graph')

plugin.register('agora', rdflib.query.Processor, 'agora.graph.processor', 'FragmentProcessor')
plugin.register('agora', rdflib.query.Result, 'agora.graph.processor', 'FragmentResult')


def extract_tps_from_plan(plan):
    # type: (Graph) -> dict
    """

    :param plan: Search Plan graph
    :return: A string triple representing the pattern for all triple pattern nodes
    """

    def extract_node_id(node):
        nid = node
        if (node, RDF.type, AGORA.Variable) in plan:
            nid = Variable(list(plan.objects(node, RDFS.label)).pop())
        elif (node, RDF.type, AGORA.Literal) in plan:
            nid = Literal(list(plan.objects(node, AGORA.value)).pop())
        return nid

    def process_tp_node(tpn):
        predicate = list(plan.objects(tpn, AGORA.predicate)).pop()
        subject_node = list(plan.objects(tpn, AGORA.subject)).pop()
        object_node = list(plan.objects(tpn, AGORA.object)).pop()
        subject = extract_node_id(subject_node)
        object = extract_node_id(object_node)

        return TP(subject, predicate, object)

    return {str(list(plan.objects(tpn, RDFS.label)).pop()): process_tp_node(tpn) for tpn in
            plan.subjects(RDF.type, AGORA.TriplePattern)}


def extract_seed_types_from_plan(plan):
    # type: (Graph) -> dict
    so = list(plan.subject_objects(predicate=AGORA.fromType))
    st_dict = {t: set(plan.objects(subject=tree, predicate=AGORA.hasSeed)) for tree, t in so}
    return st_dict


class AgoraGraph(ConjunctiveGraph):
    def __init__(self, collector):
        super(AgoraGraph, self).__init__()
        self.__collector = collector
        self.__collected = {}
        for prefix, ns in collector.prefixes.items():
            self.bind(prefix, ns)

    def build_agp(self, bgp):
        def tp_part(term):
            if isinstance(term, Variable) or isinstance(term, BNode):
                return '?{}'.format(str(term))
            elif isinstance(term, URIRef):
                return '<{}>'.format(term)
            elif isinstance(term, Literal):
                return term.n3(namespace_manager=self.namespace_manager)

        tps = set([])
        for s, p, o in bgp:
            s_elm = tp_part(s)
            if p == RDF.type and isinstance(o, URIRef):
                o_elm = self.qname(o)
                p_elm = 'a'
            else:
                p_elm = self.qname(p)
                o_elm = tp_part(o)

            tps.add('{} {} {}'.format(s_elm, p_elm, o_elm))
        return AGP(tps, self.__collector.prefixes)

    def gen(self, bgp, filters=None, **kwargs):
        bgp = frozenset(bgp)
        if bgp not in self.__collected:
            agp = self.build_agp(bgp)
            gen_dict = self.__collector.get_fragment_generator(agp, filters=filters, **kwargs)
            return self._produce(gen_dict, bgp)
        else:
            return self._read(bgp)

    def _read(self, bgp):
        for c, tp in self.__collected[bgp]['contexts'].values():
            for s, p, o in self.get_context(c):
                yield tp, s, p, o

    def _produce(self, gen, bgp):
        contexts = {}
        for context, s, p, o in gen['generator']:
            log.debug('Got triple: {} {} {} .'.format(s.encode('utf8', 'replace'), p.encode('utf8', 'replace'),
                                                      o.encode('utf8', 'replace')))
            context_id = str(context)
            if context_id not in contexts:
                contexts[context_id] = (BNode(context_id), context)
            blank_context = contexts.get(context_id)[0]
            self.get_context(blank_context).add((s, p, o))
            yield context, s, p, o

        self.__collected[bgp] = {'plan': gen['plan'], 'contexts': contexts}

    @property
    def collected(self):
        return iter(self.__collected)

    @property
    def collector(self):
        return self.__collector

    def load(self, *tps):
        for x in self.gen(*tps):
            print x

    def query(self, query_object, **kwargs):
        result = super(AgoraGraph, self).query(query_object, processor='agora',
                                               result='agora', graph=self, **kwargs)

        return result

    def search_plan(self, query_object, **kwargs):
        result = super(AgoraGraph, self).query(query_object, processor='agora',
                                               result='agora', **kwargs)

        return result.plan

    def agps(self, query_object):
        from agora.graph.evaluate import extract_bgps
        for bgp, filters in extract_bgps(query_object, prefixes=self.__collector.prefixes):
            yield self.build_agp(bgp.triples), filters
