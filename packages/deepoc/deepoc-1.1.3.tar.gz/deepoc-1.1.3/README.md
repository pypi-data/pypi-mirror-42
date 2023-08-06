
# DeepOC
  
DeepOC is the core of [BioModel Classifier](https://bitbucket.org/biomodels/model-classifier/src/master/) - the python application to classify biomodels automatically using Deep Neural Network. DeepOC provides some very low level functions for classifying model based on ontology, which allow us to adapt to any other projects.

## Installing

    pip install deepoc

## Usage
First, you need a ground truth dataset, which is a dict of model and list of it's corresponding ontologies

    {
	    "model_1": ["GO:00001", "GO:00003", "GO:00002"],
	    "model_2: ["GO:00004", "GO:00002"]
    }
To generate dataset and train DNN model:

    ground_truth = ...
    train_file = "path/to/your train csv file"
    test_file = "path/to/your test csv file"
    val_file = "path/to/your val csv file"
    features = deepoc.build_features(ground_truth)
    
    # Picking the first 300 features  
    selected_features = [feature['feature'] for idx, feature in enumerate(features) if idx < 300]
    
    train, test, val = deepoc.generate_dataset(ground_truth, features, classes)
    
    # Writing dataset to file  
    deepoc.write_dataset_to_file(train, train_file)  
    deepoc.write_dataset_to_file(test, test_file)  
    deepoc.write_dataset_to_file(val, val_file)
    
    # Configure DNN model to use Gradient Descent optimizer, 1 hidden layer with 150 nodes, learning rate of 0.001 and dropout rate of 0.5
    classifier = DeepOCClassifier(workspace, 'GD', [150], 0.001, train_file, test_file, classes, 0.5)
    # Train the model with 3000 epoch, validate every 10 epochs and batch size of 16
    classifier.train_dll_model(3000, 10, 16)
    
    # Validate the result:
    for record in val:
	    model = record['model']
	    predict_result = classifier.predict(record)  
	    logger.info('Model %s: %s', model, predict_result)

More examples can be found in *tests* folder.

### Classify model based on any ontology other than Gene Ontology
To make this library work with other kind of ontology, implement the [OntologyService](https://bitbucket.org/biomodels/deepoc/src/master/deepoc/ontology/ontology_service.py) according to your ontology and instantize your object at [https://bitbucket.org/biomodels/deepoc/src/master/deepoc/ontology/__init__.py](https://bitbucket.org/biomodels/deepoc/src/master/deepoc/ontology/__init__.py) 

## Developers

-   [Vu Tu](https://bitbucket.org/vmtu)

## Contact

## Licensing

Biological Model Classifier source code is distributed under the GNU Affero General Public License.  
Please read  [license.txt](LICENSE)  for information on the software availability and distribution.