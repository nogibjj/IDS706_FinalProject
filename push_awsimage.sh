# Build the Docker image
docker build -t myfastapp:latest .

# Tag the image with the registry name
docker tag myfastapp:latest 558669332806.dkr.ecr.us-east-1.amazonaws.com/myfastapp:latest

# Push the tagged image to the AWS Docker registry
docker push 558669332806.dkr.ecr.us-east-1.amazonaws.com/myfastapp:latest
