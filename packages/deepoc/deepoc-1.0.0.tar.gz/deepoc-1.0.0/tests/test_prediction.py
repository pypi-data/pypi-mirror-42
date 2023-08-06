import csv
import logging
import os

from deepoc import DeepOCClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
train_file = os.path.join('dataset', 'training.csv')
test_file = os.path.join('dataset', 'testing.csv')
val_file = os.path.join('dataset', 'validating.csv')
class_file = os.path.join('dataset', 'classes.txt')
workspace = 'model'
logging.getLogger("tensorflow").setLevel(logging.ERROR)


with open(class_file) as f:
    content = f.readlines()

classes = [x.strip() for x in content]
classifier = DeepOCClassifier('model', 'GD', [120, 60], 0.0001, train_file, test_file, classes)

with open(val_file) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        predict_result = classifier.predict(row)
        logger.info('Model %s: %s', row['model'], predict_result)



