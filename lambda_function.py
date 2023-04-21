import json

# boto3 is the Python AWS SDK. Read more on the documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
import boto3

# Instantiate an interface to AWS DynamoDB, whose methods map close to 1:1 with the DynamoDB service API
ddb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # You can figure out the structure of a Lambda event simply by printing it or returning it.
    # This may give you insights on how to extract the relevant information from the event (which is usually formatted as a JSON object).
    
    # Extract the http method and math operation
    http_method, operation = event['routeKey'].split()
    
    if http_method == "GET":
        # Handle GET mathematical expressions (calculate and return a result)
        
        # Extract the x and y operands
        x = event['queryStringParameters']['x']
        y = event['queryStringParameters']['y']
        try:
            # Try to typecast the x and y operands into integers
            x = int(x)
            y = int(y)
        except:
            # If we can't convert the parameters to an integer, then we throw a 400 Bad Request.
            return {"statusCode": 400}
        
        # Calculate and return a result based on the provided operation and operands
        if operation == '/add':
            return {"result": x + y}
        elif operation == '/sub':
            return {"result": x - y}
        elif operation == '/mult':
            return {"result": x * y}
        elif operation == '/div':
            return {"result": x / y}
        else:
            # If the operand was not one of /add, /sub, /mult, or /div, then we throw a 404 Not Found.
            return {"statusCode": 404}
            
            
    if http_method == "POST":
        # Handle POST mathematical expressions (post the result in DynamoDB)
        
        # Decode the "body" attribute of the event, which contains the relevant information "expression"
        decodedEvent = json.loads(event['body'])
        
        # Split the "expression" string to extract x, op, and y
        tokens = decodedEvent['expression'].split()
        x, op, y = int(tokens[0]), tokens[1], int(tokens[2])
        
        # Calculate and return a result based on the provided operation and operands
        if op == '+':
            result = x + y
        elif op == '-':
            result = x - y
        elif op == '*':
            result = x * y
        elif op == '/':
            result = x / y
        else:
            return {"statusCode": 404}
        
        # Use the ddb_client's put_item method to store the expression string and its calculated result into the DynamoDB named "CalculatorTable"
        data = ddb_client.put_item(
        TableName='CalculatorTable',
        Item={
            'expression': {
              'S': decodedEvent['expression']
            },
            'result': {
              'N': str(result)
            }
        }
        )
        
        # Return a 200 OK response if the expression and result was successfully saved into the DynamoDB.
        response = {
            'statusCode': 200,
            'body': json.dumps(data),
        }
  
        return response
