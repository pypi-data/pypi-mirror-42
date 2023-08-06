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


def find_cross_points_from_two_ontologies(possible_paths, possible_paths_2):
    cross_points = set([])
    for ontology1_to_root_paths in possible_paths:
        for path_1 in ontology1_to_root_paths:
            for ontology2_to_root_paths in possible_paths_2:
                for path_2 in ontology2_to_root_paths:
                    for point in find_cross_points(path_1, path_2):
                        cross_points.add(point)
    return cross_points


def parallel_find_cross_point(ontology_possible_paths, m, ontology_possible_paths_2, m2):
    cross_points = {}
    if m == m2:
        return {}
    for point in find_cross_points_from_two_ontologies(
            ontology_possible_paths, ontology_possible_paths_2):
        if point in cross_points:
            cross_points[point] += 1
        else:
            cross_points[point] = 1
    return cross_points


def build_features(model_ontologies, n_cpus=(mp.cpu_count() - 1)):
    """

    :type model_ontologies: dict
    :type n_cpus: number
    :return list of features and its score
    """
    real_ontologies = {}
    possible_paths = {}
    crossing_points = {}
    pool = mp.Pool(processes=n_cpus)
    logger.info("Starting to build features...")
    for model in model_ontologies:
        real_ontologies[model] = set([])
        for ontology in model_ontologies[model]['ontologies']:
            ontology_id = ontology_service.get_real_id(ontology)
            if ontology_id is not None:
                real_ontologies[model].add(ontology_id)

    for model in real_ontologies:
        possible_paths[model] = []
        for ontology_id in real_ontologies[model]:
            root = ontology_service.get_root_ontology_id(ontology_id)
            possible_paths_to_root = ontology_service.all_possible_paths(ontology_id, root)
            possible_paths[model].append(possible_paths_to_root)

    current_index = 0
    for m in possible_paths:
        if current_index % 10 == 0:
            logger.info("Processing %d/%d", current_index, len(possible_paths))
        chunks = [pool.apply(parallel_find_cross_point,
                             args=(possible_paths[m], m, possible_paths[m_2], m_2, )) for m_2 in possible_paths]
        for chunk in chunks:
            for point in chunk:
                if point in crossing_points:
                    crossing_points[point] += chunk[point]
                else:
                    crossing_points[point] = chunk[point]
        current_index += 1
    features = []
    for point in crossing_points:
        features.append({'feature': point, 'score': crossing_points[point]})
    features.sort(key=lambda x: x['score'], reverse=True)
    logger.info("Finished building features")
    return features
