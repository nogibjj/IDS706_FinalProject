# Final Project 
[![CI](https://github.com/nogibjj/IDS706_FinalProject/actions/workflows/cicd.yml/badge.svg)](https://github.com/nogibjj/IDS706_FinalProject/actions/workflows/cicd.yml)
# Overview
This project demonstrates how to deploy a microservice using pre-trained NLP model to categorize a statement to negtive, positive or neutral categories. This project is deployed through AWS Lambda, a serverless framework.

# Model

## model_training
  ### data source
  
  Pre training dataset is coming from kaggle: https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news/data
  
  ### trainModel.ipynb
  
  This notebook is to anaylyze the data and train a DNN model for categorizing.
  
## saved_model

  This directory has the pre-trained model result with the best performance
  
## vectorizer

  This directory keeps the data preprocessing model based on the dataset we used.

# Microservice
## Intro

This service will load the pre trained model to help users categorize the input statement. We utilized fastapi library to achieve this function and logging library to log the info. 

<img width="933" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/68cbe3af-da03-4d1c-8dfb-6bb3d8dfd636">

<img width="821" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/c6da940e-1dd8-4a67-869d-6ebbd727113c">

## Test Locally

Type the following command in terminal to startup the service:
```
uvicorn main:app --reload
```

<img width="854" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/74d3c91e-d11b-4177-813d-1ed906a7a5f0">
<img width="584" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/f30cd297-bea0-41ef-b240-95638e9b8e2f">

Here we will see the homepage of the service which calls the index() function.


To get a fancy page to see all apis of the service, go to the `http://127.0.0.1:8000/docs`

<img width="1676" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/586efdf2-61e6-48b6-959d-9e49a1699120">

Then we can click the process text service and click `try it out` to test our categorizing service.

<img width="1820" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/9b99d2cf-ae99-4960-866a-fcd8e4f17d99">

The response should be in json format, something like :

 {"Raw Text": <user input>, "Categories": <netural/positive/negtive>}

# Distroless Container Image

<img width="593" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/20bce4a4-db93-45be-a14e-9916c4370d05">

To build an image:
```
docker build -t myapp .
```

Run through docker image:

```
docker run -p 8080:8080 myapp
```

# Deploy in AWS Lambda

## 1. Update dockerfile to adapt to Lambda environment

<img width="611" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/51766820-a554-4b54-9054-8b14ce03cb5c">

## 2. Upload the image to AWS ECR
<img width="1868" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/4e1d3279-6c67-4543-9bbb-cb76f8cb7526">

Click on the `Create Repository` if you dont have one.

Then go into one repository and upload your microservice image.

Here is some commands to upload.

1.Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:
  ```
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your repository>
   ```
2.Build your Docker image using the following command
```
docker build -t <appname> .
```
3.After the build is completed, tag your image so you can push the image to this repository:
```
docker tag myfastapp:latest <your repository>/<appname>:latest
```

4.Run the following command to push this image to your newly created AWS repository:

```
docker push <your repository>/<appname>:latest
```

Then we will have our image in ECR for later use.
<img width="1604" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/2388dcd3-3f87-4f76-8d8c-796e586c81cc">

## 3. Create a lambda function
<img width="1862" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/14c344b8-4ea9-4cdd-8f45-8d0c83c65a07">

1. Set permissions

<img width="1729" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/3af63c36-18f2-44dc-a8ed-b33fe26adb82">

Add neccessary permissions( you may not be allowed to use the service due to some permission limits)
<img width="1456" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/d11ad569-4ef2-419f-987c-e284b4534243">

2. Set AWS configure in your terminal

```
aws configure
```

check your account security page to get the security key and set up in your terminal

3. Set `timeout` and `memory`
   
In case some apps take longer time to startup or need larger memory space.
<img width="1500" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/d7609760-bd84-4307-b593-8aec604560f3">

4. A simple test
![Alt text](image.png)

## 4. Test using AWS CLI
```
aws lambda invoke --function-name myfastapp --cli-binary-format raw-in-base64-out \
--payload '{ "payload": "Hello, Lambda!" }'  output.json 
```

```
cat output.json
```

I got a shell script for lambda test :

<img width="477" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/750867e6-37e8-45e0-baea-6ae9578bcdd6">


# Load Test

* using python concurrency library to simulate concurrent requests to the AWS Lambda function
  <img width="1165" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/127906e5-ae2f-4313-a222-8227539bcad8">
  <img width="1373" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/c7a9b490-3b21-4247-9965-0b84fc831759">

* Result
  
  <img width="687" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/c353c21a-8395-439f-bacd-e499c98fa0ee">

  1000 Requests has 938 successful cases and 62 failed cases, success rate 0.938
  
  Total time elapsed: 27.29908561706543 seconds
  
  36.63126355319651 requests per second

  <img width="675" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/a624182b-9d3a-4d05-a665-6a5c5a3755b5">
  
  10000 Requests has 7110 successful cases and 2890 failed cases, success rate 0.711
  
  Total time elapsed: 180.69083070755005 seconds
  
  55.3431513975665 requests per second
  
the service didn't achieve 10000 successful requests per second. I think its due to several reasons:
  
  * The aws concurrency limits.
    
  * python scripts concurrent requests delay: creating 10000 threads to send testing requests costs a lot
    
  * our model takes much time for data processing and prediction. Its kinda not a "microservice"
    
    
    
    
  
  We may upgrade our service through increasing the concurrency in aws:
  <img width="1631" alt="image" src="https://github.com/nogibjj/IDS706_FinalProject/assets/108935314/d0e66141-3858-4053-8648-88a723ed7272">

# Run
There are several shell scripts.

`make install`: Install dependencies

`make lint`: Linting code

`make format`: Formatting code

`make test`: Testing app functions

`make trainModel`: Pretraining the model for deployment

`make clearDocker`: Clearing docker space 

`make pushDocker`: Pushing docker image to AWS ECR

`make testLambda`: Testing services deployed in Lambda


# Video Demo:
https://youtu.be/4UqS68EEPa4
# Some advice:
* Double check your account configure before utilizing lambda apps
* Attention to dockerfile configure(aws lambda has its unique environment) && Test your image before uploading (takes much time)
  Use the following command to test:
  ```
  docker run -p 9000:8080 docker-image:test
  ```
  
  ```
  curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'
  ```
  This commands simulate what will happen in the aws lambda app.

  Check this site: https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/images-test.html

  
# Reference :
https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/images-test.html

https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/images-create.html

https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/lambda-invocation.html

https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/invocation-sync.html

https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/invocation-async.html

https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html
