import math

from deepoc.ontology import ontology_service


def __calculate_similarity_score(feature, ontology):
    if feature == ontology:
        return 1
    weight_distance = ontology_service.find_shortest_distance(ontology, feature)
    if weight_distance > 0:
        distance_from_root_first = ontology_service.find_shortest_distance(
            ontology, ontology_service.get_root_ontology_id(ontology))
        distance_from_root_second = ontology_service.find_shortest_distance(
            feature, ontology_service.get_root_ontology_id(feature)
        )
        depth = 2.0 / float(distance_from_root_first + distance_from_root_second + 2)
        return math.pow(1.0 / weight_distance, depth)
    return 0


def __analyze_score(feature, ontologies):
    max_score = 0
    for ontology in ontologies:
        ontology_id = ontology_service.get_real_id(ontology)
        if ontology_id is None:
            continue
        score = __calculate_similarity_score(feature, ontology_id)
        if score > max_score:
            max_score = score
    return max_score


def calculate_similarity(ontologies, features):
    result = []
    for feature in features:
        score = __analyze_score(feature, ontologies)
        result.append({'feature': feature, 'score': score})
    return result
