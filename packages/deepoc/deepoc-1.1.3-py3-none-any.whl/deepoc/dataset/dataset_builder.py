import csv
import logging
from random import shuffle

from deepoc.similarity import similarity_service

logger = logging.getLogger(__name__)


def write_dataset_to_file(dataset, file_path):
    keys = list(dataset[0].keys())
    keys.remove('model')
    keys = ['model'] + keys
    keys.remove('class')
    keys = keys + ['class']

    with open(file_path, 'w') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(dataset)


def __calculate_similarity_matrix(ground_truth, features, classes):
    tmp_result = []
    for idx, model in enumerate(ground_truth):
        logger.debug("Processing model %s %d/%d" % (model, idx, len(ground_truth)))
        tmp_result.append({
            'model': model,
            'features_result': similarity_service.calculate_similarity(ground_truth[model]['ontologies'], features),
            'class': ground_truth[model]['class']
        })

    result = {}
    for model_result in tmp_result:
        model_data = {'model': model_result['model']}
        for record in model_result['features_result']:
            # Tensorflow is not allowed to have ':' character in columns list
            feature = record['feature'].replace(":", "_")
            model_data[feature] = record['score']
        model_data['class'] = classes.index(model_result['class'])

        # If all similarity of the record = 0, then ignore it
        has_val = False
        for key in model_data:
            if key not in ['model', 'class']:
                if model_data[key] > 0:
                    has_val = True
        if not has_val:
            continue
        if model_data['class'] in result:
            result[model_data['class']].append(model_data)
        else:
            result[model_data['class']] = [model_data]
    for key in result:
        shuffle(result[key])
    return result


def generate_dataset(ground_truth, features, classes, test_percent=20, val_percent=5):
    """

    :param classes: list of categories
    :type classes: list
    :param val_percent: how many percent of ground truth data will be used for validating
    :param test_percent: how many percent of ground truth data will be used for testing
    :type features: list
    :type ground_truth: dict
    """
    logger.info("Generating dataset...")

    result = __calculate_similarity_matrix(ground_truth, features, classes)

    logger.info("Separating dataset...")
    train_data = []
    val_data = []
    test_data = []
    for class_id in result:
        for index, model in enumerate(result[class_id]):
            current_percent = (float(index) / float(len(result[class_id]))) * 100
            if current_percent <= test_percent:
                test_data.append(model)
            elif current_percent <= test_percent + val_percent:
                val_data.append(model)
            else:
                train_data.append(model)
    shuffle(train_data)
    shuffle(test_data)
    shuffle(val_data)
    logger.info("Dataset generated!")
    return train_data, test_data, val_data
