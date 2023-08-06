from deepoc.ontology.ontology_service import OntologyService
import networkx
import obonet

GO_DB = 'http://purl.obolibrary.org/obo/go/go-basic.obo'


class GeneOntologyService(OntologyService):

    def __init__(self):
        self.graph = obonet.read_obo(GO_DB)
        self._id_to_id = {}
        for id_, data in self.graph.nodes(data=True):
            if 'alt_id' in data:
                for alt_id in data['alt_id']:
                    self._id_to_id[alt_id] = id_
            self._id_to_id[id_] = id_
        self._name_to_id = {data['name']: id_ for id_, data in self.graph.nodes(data=True)}
        self._id_to_name = {id_: data['name'] for id_, data in self.graph.nodes(data=True)}
        self._annotation_score = {}

    def all_possible_paths(self, source, target):
        return list(networkx.all_simple_paths(self.graph, source, target))

    def get_ontology_name(self, ontology_id):
        if ontology_id in self._id_to_id:
            return self._id_to_name[ontology_id]
        return None

    def get_real_id(self, ontology_id):
        if ontology_id in self._id_to_id:
            return self._id_to_id[ontology_id]
        return None

    def get_root_ontology_id(self, ontology_id):
        if ontology_id in self._id_to_id:
            node = self.graph.node[ontology_id]
            root_node = self._name_to_id[node['namespace']]
            return root_node
        return None

    def __already_calculated(self, ontology_id_source, ontology_id_target):
        if ontology_id_source in self._annotation_score:
            if ontology_id_target in self._annotation_score[ontology_id_source]:
                return self._annotation_score[ontology_id_source][ontology_id_target]
        return None

    def find_shortest_distance(self, source, target):
        distance = self.__already_calculated(source, target)
        if distance is not None:
            return distance
        try:
            distance = len(networkx.shortest_path(self.graph, source, target))
        except networkx.NetworkXNoPath:
            distance = 0
        except networkx.NodeNotFound:
            distance = 0
        self._annotation_score[source] = {target: distance}
        return distance
