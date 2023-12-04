import concurrent.futures
import boto3
import json

import time
LAMBDA_FUNCTION_NAME = 'myfastapp'
AWS_REGION = 'us-east-1'
PAYLOAD = {'payload': 'this is a test'}  # Customize the payload as needed
CONCURRENT_REQUESTS = 10000

# Function to invoke the Lambda function
def invoke_lambda(_):
    lambda_client = boto3.client('lambda', region_name=AWS_REGION)
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=json.dumps(PAYLOAD)
    )
    result = json.loads(response['Payload'].read().decode())
    return result

# Use ThreadPoolExecutor for concurrent requests
succ_cases = 0
fail_cases = 0
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
    # Submit concurrent requests
    future_to_request = {executor.submit(invoke_lambda, i): i for i in range(CONCURRENT_REQUESTS)}
    
    # Wait for all requests to complete
    for future in concurrent.futures.as_completed(future_to_request):
        request_number = future_to_request[future]
        try:
            result = future.result()
            succ_cases+=1
            # print(f"Request {request_number} successful. Result: {result}")
        except Exception as e:
            fail_cases+=1
            # print(f"Request {request_number} failed. Exception: {e}")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"{CONCURRENT_REQUESTS} Requests has {succ_cases} successful cases and {fail_cases} cases, success rate {succ_cases/CONCURRENT_REQUESTS}")
print(f"Total time elapsed: {elapsed_time} seconds")