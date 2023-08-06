import logging
import os
import shutil

from deepoc import DeepOCClassifier

logging.basicConfig(level=logging.INFO)
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

train_file = os.path.join('dataset', 'training.csv')
test_file = os.path.join('dataset', 'testing.csv')
class_file = os.path.join('dataset', 'classes.txt')
workspace = 'model'


with open(class_file) as f:
    content = f.readlines()
    classes = [x.strip() for x in content]

if os.path.isdir(workspace):
    shutil.rmtree(workspace)

classifier = DeepOCClassifier(workspace, 'GD', [150], 0.001, train_file, test_file, classes, 0.5)
classifier.train_dll_model(500, 10, 16)



