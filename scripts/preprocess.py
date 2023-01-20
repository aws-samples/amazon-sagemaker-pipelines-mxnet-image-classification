#!/usr/bin/python3.7

import argparse
import os
import logging
import subprocess


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    
    ###### 1. Parse input arguments ######
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-s3-bucket', type=str, dest='INPUT_S3_BUCKET')
    parser.add_argument('--train-split-percentage', type=str, default=0.70, dest='TRAIN_SPLIT_PERCENTAGE')
    parser.add_argument('--validation-split-percentage', type=str, default=0.15, dest='VALIDATION_SPLIT_PERCENTAGE')
    parser.add_argument('--test-split-percentage', type=str, default=0.15, dest='TEST_SPLIT_PERCENTAGE')

    args = parser.parse_args()
    print(args.INPUT_S3_BUCKET)
    
    ###### 2. Create RecordIO files from image files ######
    logger.debug("Creating RecordIO files from image files")
    
    DATASET_NAME="ImageData"
    BASE_DIR="/opt/ml/processing/input/data"
    IM2REC_PATH="/opt/ml/processing/input/code/im2rec.py"
    
    command = f"cd {BASE_DIR};\
            pwd;\
            ls;\
            rm *.rec;\
            echo 'Downloading im2rec.py script from Apache MXNet';\
            wget -P /opt/ml/processing/input/code/ https://raw.githubusercontent.com/apache/incubator-mxnet/master/tools/im2rec.py;\
            cd /opt/ml/processing/input/code/;\
            pwd;\
            cd {BASE_DIR};\
            echo 'Creating LST files';\
            python {IM2REC_PATH} --list --recursive --pass-through --test-ratio={args.TEST_SPLIT_PERCENTAGE} --train-ratio={args.TRAIN_SPLIT_PERCENTAGE} {DATASET_NAME} {DATASET_NAME} > {DATASET_NAME}_classes;\
            echo 'Label classes:';\
            cat {DATASET_NAME}_classes;\
            python {IM2REC_PATH} --num-thread=4 {DATASET_NAME}_train.lst {DATASET_NAME};\
            python {IM2REC_PATH} --num-thread=4 {DATASET_NAME}_val.lst {DATASET_NAME};\
            python {IM2REC_PATH} --num-thread=4 {DATASET_NAME}_test.lst {DATASET_NAME};\
            ls -lh *.rec"
    
    ret = subprocess.run(command, capture_output=True, shell=True)
    print(ret.stdout.decode())

    ###### 3. Upload RecordIO files to S3 ######
    logger.debug("Uploading newly created RecordIO back to S3")

    # Upload our train and test RecordIO files back to S3 bucket    
    TRAIN_CHANNEL = '/opt/ml/processing/train'
    VALIDATION_CHANNEL = '/opt/ml/processing/validation'
    TEST_CHANNEL = '/opt/ml/processing/test'

    # Clean up any existing data in S3
    os.system(f"aws s3 rm {args.INPUT_S3_BUCKET}/recordIO/train --recursive")
    os.system(f"aws s3 rm {args.INPUT_S3_BUCKET}/recordIO/validation --recursive")
    os.system(f"aws s3 rm {args.INPUT_S3_BUCKET}/recordIO/test --recursive")
    
    # Upload the rec files to the train, validation, test channels
    os.system(f"cp /opt/ml/processing/input/data/{DATASET_NAME}_train.rec {TRAIN_CHANNEL}")
    os.system(f"cp /opt/ml/processing/input/data/{DATASET_NAME}_val.rec {VALIDATION_CHANNEL}")
    os.system(f"cp /opt/ml/processing/input/data/{DATASET_NAME}_test.rec {TEST_CHANNEL}")
    
    print("Done!")
