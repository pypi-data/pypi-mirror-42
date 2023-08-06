import json
import logging
import os

import deepoc

logging.basicConfig(level=logging.INFO)
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

train_file = os.path.join('dataset', 'training.csv')
test_file = os.path.join('dataset', 'testing.csv')
val_file = os.path.join('dataset', 'validating.csv')
class_file = os.path.join('dataset', 'classes.txt')

logger.info("Loading ground truth data...")
with open('ground_truth.json') as f:
    ground_truth = json.load(f)

with open(class_file) as f:
    content = f.readlines()
    classes = [x.strip() for x in content]

    features = ['GO:0008150', 'GO:0009987', 'GO:0065007', 'GO:0050789', 'GO:0050896', 'GO:0050794', 'GO:0008152', 'GO:0007154', 'GO:0023052', 'GO:0051716', 'GO:0071704', 'GO:0044237', 'GO:0005575', 'GO:0007165', 'GO:0003674', 'GO:0005623', 'GO:0044464', 'GO:0044238', 'GO:0006807', 'GO:0065008', 'GO:0032501', 'GO:0005622', 'GO:0044424', 'GO:0042221', 'GO:0032991', 'GO:1901564', 'GO:0043170', 'GO:0051179', 'GO:0051234', 'GO:0006810', 'GO:0044260', 'GO:0010033', 'GO:0044281', 'GO:0009058', 'GO:0048583', 'GO:0003008', 'GO:0035556', 'GO:0003824', 'GO:0006950', 'GO:0070887', 'GO:1901576', 'GO:0019222', 'GO:0010646', 'GO:0005737', 'GO:0023051', 'GO:0044444', 'GO:0007166', 'GO:0044249', 'GO:0034641', 'GO:0043226', 'GO:0007267', 'GO:0043229', 'GO:0019538', 'GO:0009719', 'GO:0071310', 'GO:0032502', 'GO:0006082', 'GO:0044267', 'GO:0005488', 'GO:0031323', 'GO:0060255', 'GO:0007049', 'GO:0009966', 'GO:1901360', 'GO:0046483', 'GO:0009725', 'GO:0019752', 'GO:0006725', 'GO:0043436', 'GO:0032879', 'GO:0016020', 'GO:0071495', 'GO:0005515', 'GO:1901700', 'GO:0044422', 'GO:0044446', 'GO:0071840', 'GO:0071702', 'GO:0016043', 'GO:0006811', 'GO:0048856', 'GO:0043227', 'GO:0003013', 'GO:0010817', 'GO:0043412', 'GO:1902494', 'GO:0051171', 'GO:0005975', 'GO:0051049', 'GO:0048518', 'GO:0006464', 'GO:0036211', 'GO:0009628', 'GO:0044271', 'GO:0065009', 'GO:0033554', 'GO:0006793', 'GO:0032940', 'GO:0006796', 'GO:0046903', 'GO:0044425', 'GO:0022402', 'GO:0140096', 'GO:0042592', 'GO:0006812', 'GO:0051239', 'GO:0002376', 'GO:0008015', 'GO:0009914', 'GO:0009605', 'GO:0051704', 'GO:0010467', 'GO:0022857', 'GO:0005215', 'GO:0015318', 'GO:1901566', 'GO:0043231', 'GO:0007167', 'GO:0023061', 'GO:0042391', 'GO:0046873', 'GO:0016772', 'GO:0016787', 'GO:0009056', 'GO:0022803', 'GO:0016740', 'GO:0046879', 'GO:0022890', 'GO:0008324', 'GO:0015267', 'GO:0015075', 'GO:0010468', 'GO:0005216', 'GO:0016301', 'GO:0016310', 'GO:0006955', 'GO:0030001', 'GO:0032870', 'GO:0080090', 'GO:0022838', 'GO:1901575', 'GO:0005261', 'GO:0042493', 'GO:0043232', 'GO:0043228', 'GO:0001508', 'GO:1902531', 'GO:0048869', 'GO:0016773', 'GO:1901362', 'GO:0071944', 'GO:0098796', 'GO:0044262', 'GO:0007275', 'GO:0044419', 'GO:0009059', 'GO:1901698', 'GO:0018130', 'GO:0048519', 'GO:0071705', 'GO:0050790', 'GO:0044283', 'GO:0019438', 'GO:0051726', 'GO:0044403', 'GO:0005886', 'GO:0051246', 'GO:0034645', 'GO:0048511', 'GO:1990234', 'GO:0006468', 'GO:0007623', 'GO:1990904', 'GO:0034654', 'GO:0006091', 'GO:0099536', 'GO:0044057', 'GO:0009889', 'GO:0032268', 'GO:0048523', 'GO:0098916', 'GO:0032787', 'GO:0006996', 'GO:0099537', 'GO:0010243', 'GO:0002790', 'GO:0055085', 'GO:0005102', 'GO:0003012', 'GO:0022836', 'GO:0098772', 'GO:1901701', 'GO:0000278', 'GO:0015833', 'GO:0007268', 'GO:0042886', 'GO:0004672', 'GO:0044459', 'GO:0055114', 'GO:0007169']

    train, test, val = deepoc.generate_dataset(ground_truth, features, classes)

    # Writing dataset to file
    deepoc.write_dataset_to_file(train, train_file)
    deepoc.write_dataset_to_file(test, test_file)
    deepoc.write_dataset_to_file(val, val_file)
