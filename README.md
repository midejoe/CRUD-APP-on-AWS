# CRUD-APP-on-AWS
CRUD Application Using API Gateway, Lambda And DynamoDB

## Project Description
We have an application where we want to save records for student data like Student Name, Roll Number, Date of birth, Gender, Class, etc so want to implement CRUD (CREATE, READ, UPDATE and DELETE) operations functionality with AWS Lambda and API-Gateway. We will use Dynamo-DB as a database for this and make connectivity with it using lambda. Right now we are using python as our programming language for this task.

We need to implement a CRUD Application where you need 4 separate lambdas for creating, reading, updating, and deleting the record. After that, you need to connect your lambda with a Dynamodb to save the records there. DynamoDB is an AWS  fully managed proprietary NoSQL database. After that, you need to create API-Gateway and create different methods like GET, POST, UPDATE and DELETE so that you can create communication between lambda and API gateway. When a user wants to add records, it will trigger the get request to the API and then save the records to the dynamo DB which is a database. You will test it using postman. In postman, you have different methods to pass request to the API.

# Solution:

I have provisioned the necessary resources on AWS using the console and also using Terraform. The code for the Lambda function can also be found on this repo.
For testing the URL, I have used POSTMAN to test our REST APIS. You can check the wiki here
