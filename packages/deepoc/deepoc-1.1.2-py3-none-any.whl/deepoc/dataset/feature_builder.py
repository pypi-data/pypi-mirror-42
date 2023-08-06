import logging
import multiprocessing as mp

from deepoc.ontology import ontology_service

logger = logging.getLogger(__name__)


def find_cross_points(path_1, path_2):
    cross_point = set([])
    for point in path_1:
        for point_2 in path_2:
            if point == point_2:
                cross_point.add(point)
    return cross_point


def find_cross_points_from_two_list_of_paths(possible_paths, possible_paths_2):
    cross_points = set([])
    for path_1 in possible_paths:
        for path_2 in possible_paths_2:
            for point in find_cross_points(path_1, path_2):
                cross_points.add(point)
    return cross_points


def parallel_find_cross_points(ontology, ontology_2):
    cross_points = set([])
    if ontology['name'] == ontology_2['name']:
        return cross_points
    for point in find_cross_points_from_two_list_of_paths(ontology['paths'], ontology_2['paths']):
        cross_points.add(point)
    return cross_points


def build_features(model_ontologies, n_cpus=max(1, mp.cpu_count() - 1)):
    """

    :type model_ontologies: dict
    :type n_cpus: number
    :return list of features and its score
    """
    ontologies = {}
    crossing_points = {}
    pool = mp.Pool(processes=n_cpus)
    logger.info("Starting to build features...")
    for model in model_ontologies:
        for ontology in model_ontologies[model]['ontologies']:
            ontology_id = ontology_service.get_real_id(ontology)
            if ontology_id is not None and ontology_id not in ontologies:
                root = ontology_service.get_root_ontology_id(ontology_id)
                possible_paths_to_root = ontology_service.all_possible_paths(ontology_id, root)
                ontologies[ontology_id] = {'paths': possible_paths_to_root, 'name': ontology_id}

    current_index = 0
    for ontology in ontologies:
        if current_index % 10 == 0:
            logger.info("Processing %d/%d", current_index, len(ontologies))
        chunks = [pool.apply(parallel_find_cross_points,
                             args=(ontologies[ontology], ontologies[m_2], )) for m_2 in ontologies]
        for chunk in chunks:
            for point in chunk:
                if point in crossing_points:
                    crossing_points[point] += 1
                else:
                    crossing_points[point] = 1
        current_index += 1
    features = []
    for point in crossing_points:
        features.append({'feature': point, 'score': crossing_points[point]})
    features.sort(key=lambda x: x['score'], reverse=True)
    logger.info("Finished building features")
    return features
