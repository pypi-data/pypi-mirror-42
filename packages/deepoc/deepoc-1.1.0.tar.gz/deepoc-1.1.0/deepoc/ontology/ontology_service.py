class OntologyService:

    def get_real_id(self, ontology_id):
        """
        Because some ontology have alternative ids, those alt ids don't have definition
        This will find the real ontology id of those alt ids
        :param ontology_id: str
        :return:
        """
        raise NotImplementedError("Should have implemented this")

    def get_ontology_name(self, ontology_id):
        """
        Get ontology name from ontology id
        :param ontology_id:
        :return:
        """
        raise NotImplementedError("Should have implemented this")

    def get_root_ontology_id(self, ontology_id):
        """
        Find root ontology in the ontology graph
        :param ontology_id:
        :return:
        """
        raise NotImplementedError("Should have implemented this")

    def find_shortest_distance(self, source, target):
        """
        Find the shortest distance between two ontology inside the ontology graph
        :param source:
        :param target:
        """
        raise NotImplementedError("Should have implemented this")

    def all_possible_paths(self, source, target):
        """
        Find all possible paths from source to target inside the ontology graph
        :param source:
        :param target:
        """
        raise NotImplementedError("Should have implemented this")

    def search(self, keyword):
        """
        search for either ontology_id or name
        :type keyword: str
        """
        raise NotImplementedError("Should have implemented this")
