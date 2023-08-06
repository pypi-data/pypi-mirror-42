import json
import logging

import deepoc

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Loading ground truth data...")
with open('ground_truth.json') as f:
    ground_truth = json.load(f)

    logger.info("Building features list")
    features = deepoc.build_features(ground_truth)

    # Picking the first 300 features
    selected_features = [feature['feature'] for idx, feature in enumerate(features) if idx < 300]

    logger.info("Features: %s", features)
