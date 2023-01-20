# Build and Register an MXNet Image Classification Model via Amazon SageMaker Pipelines 

This architecture describes how to: (1) preprocess an image (.jpg) dataset into the recommended RecordIO input format for image classification, (2) train and evaluate a MXNet binary image classification model using SageMaker, and (3) register the trained model to SageMaker Model Registry. Additionally, this pattern demonstrates how all these ML workflow steps can be defined and automated using SageMaker Pipelines.

## Prerequisites and limitations

### Prerequisites
- An active AWS account
- Access to the following [Pizza or Not Pizza?](https://www.kaggle.com/datasets/carlosrunner/pizza-not-pizza) public dataset
    - **Note:** For this pattern, you will be building a binary image classification model that detects whether an input image contains a pizza food item or not. However, you can modify this pattern to optionally use any image dataset that has two distinct classes (i.e. cat vs. dog)
- An Amazon Simple Storage Service (Amazon S3) bucket to store the image (.jpeg) dataset
- Access to create and configure an Amazon SageMaker Domain and User Profile. For more information about this, see Onboard to Amazon SageMaker Domain in the Amazon SageMaker documentation
- Access to Amazon SageMaker Studio
- An understanding of Amazon SageMaker notebooks and Jupyter notebooks
- An understanding of how to create an AWS Identity and Access Management (IAM) role with basic SageMaker role permissions and S3 bucket access permissions
- Familiarity with Python
- Familiarity with common ML terms and concepts such as “binary classification”, “preprocessing”, “hyperparameters”, etc. For more information about this, see Machine Learning Concepts in the Amazon Machine Learning documentation

### Limitations
- To save processing time and cut costs, only a subset (1000 images) of the [Pizza or Not Pizza? dataset](https://www.kaggle.com/datasets/carlosrunner/pizza-not-pizza) is used to build the image classification model. You can choose to use more (or less) data or choose another dataset entirely (as mentioned above)
- Certain hyperparameters in the model training step are hard-coded (manually set). These are specified in the `image-classification-sagemaker-pipelines.ipynb` Jupyter notebook. For more information about this, see [Image Classification Hyperparameters](https://docs.aws.amazon.com/sagemaker/latest/dg/IC-Hyperparameter.html) in the Amazon SageMaker documentation.
- You can extend upon the existing image classification ML workflow by adding additional steps (e.g. model tuning step) as needed. For more information about this, see [Pipeline Steps](https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html) in the Amazon SageMaker documentation.

## Architecture

### Target technology stack 
- [Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
    - [SageMaker Pipelines](https://aws.amazon.com/sagemaker/pipelines/)
    - [SageMaker Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)
- [Amazon Simple Storage Service (S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)

### Target architecture
![Architecture Diagram](/architecture-diagram.png "Architecture Diagram")

### Automation and scale
After registering the trained model to SageMaker Model Registry, you can choose to deploy the model to a SageMaker endpoint for real-time inference. For more information about this, see [Deploy a Model](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-deploy.html) from the Registry in the Amazon SageMaker documentation.

## Tools
- [Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) — SageMaker is a fully managed ML service
- [Amazon SageMaker Pipelines](https://aws.amazon.com/sagemaker/pipelines/) — SageMaker Pipelines help create, automate, and manage end-to-end ML workflows at scale
- [Amazon SageMaker Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html) — SageMaker Model Registry helps centrally catalog and manage trained ML models
- [Amazon Simple Storage Service (Amazon S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) — Amazon S3 is an object storage service that offers industry-leading scalability, data availability, security, and performance.
- [Python](https://www.python.org/) — Python is a programming language.

## Getting started

### Step 1. Prepare Amazon S3 Bucket for image dataset
- Create a new S3 bucket via the Amazon S3 console
- Create a new folder named “ImageData” within the newly created S3 bucket, .
    - Within the “ImageData” folder, create two subfolders named “Pizza” and “NotPizza”.
- Locally download [Pizza or Not Pizza?](https://www.kaggle.com/datasets/carlosrunner/pizza-not-pizza) dataset on to your computer and unzip its contents
    - You should notice two subdirectories within the downloaded file: (1) “pizza” and (2) “not_pizza”
    - **Note:** You may have to create a free account with Kaggle.com to access the dataset.
- Navigate to the “Pizza” folder in the S3 bucket and upload 500 randomly selected images from the “pizza” subdirectory from the locally downloaded dataset.
- Navigate to the “NotPizza” folder in the S3 bucket and upload 500 randomly selected images from the “not_pizza” subdirectory from the locally downloaded dataset.

### Step 2. Configure Amazon SageMaker Studio environment
- Create a new SageMaker Domain and User Profile via the Amazon SageMaker console
    - Follow the instructions from [Onboard to Amazon SageMaker Domain Using Quick setup](https://docs.aws.amazon.com/sagemaker/latest/dg/onboard-quick-start.html) from the Amazon SageMaker documentation.
    - **Note:** When setting up the IAM role for the user profile, ensure that you give access to the Amazon S3 bucket you created earlier.
- Launch SageMaker Studio application
    - Follow the instructions from [Launch Studio Using the Amazon SageMaker Console](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launch.html#studio-launch-console) from the Amazon SageMaker documentation
- Download the `image-classification-sagemaker-pipelines.ipynb` Jupyter notebook and `scripts` folder from this GitHub repository
- Upload the `image-classification-sagemaker-pipelines.ipynb` Jupyter notebook and `scripts` folder to the SageMaker Studio application

### Step 3. Run the Jupyter notebook in Amazon SageMaker Studio
- Sequentially run the code cells from the `image-classification-sagemaker-pipelines.ipynb` Jupyter notebook within SageMaker Studio
    - **Note:** Make sure to appropriately configure the `TODO` portions of the code before you run the code cells

## Clean up
- Delete the S3 bucket with the image dataset and the default S3 bucket created by the SageMaker session
    - For more information on this, follow the instructions from [Deleting a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/delete-bucket.html) from the Amazon S3 documentation.
    - **Note:** The default S3 bucket created by the SageMaker session should be in the following format: *"sagemaker-{region}-{aws-account-id}”*
- Delete model group from SageMaker Model Registry
     - Follow the instructions from [Delete a Model Group](https://apg-library.amazonaws.com/content-viewer/author/ff1f11b2-ec30-47e5-9e01-835dc10b5a42#:~:text=Follow%20the%20instructions%20from%20Delete%20a%20Model%20Group%20from%20the%20Amazon%20SageMaker%20documentation.) from the Amazon SageMaker documentation.
     - **Note:** The model group name should be *“MXNet-Image-Classification.”* This was previously defined in the `image-classification-sagemaker-pipelines.ipynb` Jupyter notebook
- Delete SageMaker Domain
    - Follow the instructions from [Delete an Amazon SageMaker Domain (console)](https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-delete-domain.html#gs-studio-delete-domain-studio) from the Amazon SageMaker documentation

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

