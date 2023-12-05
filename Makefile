install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=main test_*.py

format:	
	black *.py 

lint:
	pylint --disable=R,C  test_main.py
# pre train the model for the microservice
trainModel:
	ipython -c "%run model_training/trainmodel.ipynb"
# clear docker space
clearDocker:
	bash clear_docker.sh
# push docker image to aws container registry
pushDocker:
	bash push_awsimage.sh
# test the lambda function 
testLambda:
	bash test_lambda.sh

all: install lint format test 