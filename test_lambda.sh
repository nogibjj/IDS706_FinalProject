aws lambda invoke --function-name myfastapp --cli-binary-format raw-in-base64-out \
--payload '{ "payload": "Hello, Lambda!" }'  output.json 

cat output.json