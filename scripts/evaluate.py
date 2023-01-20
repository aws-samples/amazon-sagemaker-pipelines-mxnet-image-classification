#!/usr/bin/python3.7

import json
import logging
import pathlib
import pickle
import tarfile
import glob
import mxnet as mx

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    logger.debug("Starting evaluation.")
    
    ###### 1. Loading trained MXNet model ######
    logger.debug("Loading mxnet model.")
    
    model_path = "/opt/ml/processing/model/model.tar.gz"
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")
    
    param_file = glob.glob('./*.params')
    epoch = int(param_file[0][-8])
    sym, arg_params, aux_params = mx.model.load_checkpoint("image-classification", epoch)

    ###### 2. Loading and preparing test .rec file ######
    logger.debug("Reading test data.")
    
    DATASET_NAME="ImageData"
    test_path = f"/opt/ml/processing/test/{DATASET_NAME}_test.rec"
    
    test = mx.io.ImageRecordIter(path_imgrec=test_path,
                                 data_name='data',
                                 label_name='softmax_label',
                                 batch_size=10,
                                 data_shape=(3, 224, 224),
                                 rand_crop=False,
                                 rand_mirro=False)
    
    
    ###### 3. Making predictions on the test set ######
    logger.info("Performing predictions against test data.")
    
    mod = mx.mod.Module(symbol=sym, context=mx.cpu())
    
    mod.bind(for_training=False,
             data_shapes=test.provide_data,
             label_shapes=test.provide_label)
    
    mod.set_params(arg_params, aux_params)

    ###### 4. Calculating evaluation metrics ######
    logger.debug("Calculating accuracy and F1 scores on test set.")
    
    metric = mod.score(eval_data=test, eval_metric=['acc', 'f1'])
    test_accuracy = metric[0][1]
    test_f1 = metric[1][1]

    report_dict = {
        "classification_metrics": {
            "accuracy": {
                "value": test_accuracy
            },
            "f1": {
                "value": test_f1
            }
        },
    }

    ###### 5. Saving evaluation metrics to output path ######
    logger.info("Writing out evaluation report")
    
    output_dir = "/opt/ml/processing/evaluation"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)


    evaluation_path = f"{output_dir}/evaluation.json"
    with open(evaluation_path, "w") as f:
        f.write(json.dumps(report_dict))
        
    print("Done!")
