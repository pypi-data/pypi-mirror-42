import csv
import logging
import os

from deepoc import DeepOCClassifier

logging.basicConfig(level=logging.INFO)
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

train_file = os.path.join('dataset', 'training.csv')
test_file = os.path.join('dataset', 'testing.csv')
val_file = os.path.join('dataset', 'validating.csv')
class_file = os.path.join('dataset', 'classes.txt')
workspace = 'model'


with open(class_file) as f:
    content = f.readlines()

classes = [x.strip() for x in content]
classifier = DeepOCClassifier(workspace, 'GD', [150], 0.001, train_file, test_file, classes, 0.5)

with open(val_file) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        model = row['model']
        predict_result = classifier.predict(row)
        logger.info('Model %s: %s', model, predict_result)



