# intro-to-aws-services-workshop
Lambda code used for the Serverless Calculator HTTP API demo during Hack at UCI's Intro to AWS Services workshop on 04/20/2023.

## To deploy

#### Set up your AWS resources

1. Create a DynamoDB with name "CalculatorTable"
- Partition key = expression, String

2. Create a Lambda with name "CalculatorLambda"
- Use runtime Python 3.10
- Copy the code from the repo file lambda_function.py into CalculatorLambda

3. Give CalculatorLambda IAM permissions to read DynamoDB
- CalculatorLambda -> Configuration -> Permissions --> Under execution role, click the role name --> Add permissions -> Attach policies -> Add policy "AmazonDynamoDBFullAccess"

4. Create an HTTP API on API Gateway with the name "Calculator API"
- Integration: Choose Lambda, and select your CalculatorLambda
- Configure the following routes:
  - GET /add -> CalculatorLambda
  - GET /sub -> CalculatorLambda 
  - GET /mult -> CalculatorLambda
  - GET /div -> CalculatorLambda
  - POST /save -> CalculatorLambda
- Stage: default

## Usage
- Recommend using [Postman](https://web.postman.co/) for sending HTTP requests to test your API
- To test/use a GET route:
  - Into your web browser or w/ Postman GET request: {API_ENDPOINT_URL}/add?x=10&y=7 --> returns 17
- To test/use a POST route:
  - Postman POST request: {API_ENDPOINT_URL}/save
    - Body --> raw --> type in {"expression": "10 * 7"} --> saves the entry {"expression": "10 * 7", "result": 70} into DynamoDB CalculatorTable

Feel free to clone this repository and make your own configured API routes and Lambda logic!
