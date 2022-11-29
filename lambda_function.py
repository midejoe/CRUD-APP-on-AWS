#import necessary modules
import boto3
import json
from custom_encoder import CustomEncoder
import logging

##############################################################################################################

#define the logger
logger = logging.getLogger()
#set the logger level
logger.setLevel(logging.INFO)

##############################################################################################################

#define dynamodbtable
dynamodbTableName = 'student-records'
#get the dynamodb resource using boto3
dynamodb = boto3.resource('dynamodb')
#get the table
table = dynamodb.Table(dynamodbTableName)

##############################################################################################################

#define methods
getMethod = 'GET' #get item
postMethod = 'POST' #create new item
patchMethod = 'PATCH' #update item
deleteMethod = 'DELETE' #delete item

##############################################################################################################

#define Paths
healthPath = '/health' #api health path
studentPath = '/student' #a student path
studentsPath = '/students' #all students path

##############################################################################################################

#define a function that takes an event and context object(entry point)
def lambda_handler(event, context):
    #log the request to see what the request looks like
    logger.info(event)
    #extract the httpMethod from the event object
    httpMethod = event['httpMethod']
    #extract the path from the event object
    path = event['path']

    #conditions to handle different http method and path scenarios
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == studentPath:
        response = getStudent(event['queryStringParameters']['studentId'])
    elif httpMethod == getMethod and path == studentsPath:
        response = getStudents()
    elif httpMethod == postMethod and path == studentPath:
        response = saveStudent(json.loads(event['body']))
    elif httpMethod == patchMethod and path == studentPath:
        requestBody = json.loads(event['body'])
        response = modifyStudent(requestBody['studentId'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == studentPath:
        requestBody = json.loads(event['body'])
        response = deleteStudent(requestBody['studentId'])
    else:
        response = buildResponse(404, 'Not Found')

    return response

############################################################################################################## 

# define response method
def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' #allows cross regional access (to integrate with front end with different host name)
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response

##############################################################################################################

#define get student record
def getStudent(studentId):
    try:
        response = table.get_item(
            Key={
                'studentId': studentId
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'StudentId: %s not found' % studentId})
    except:
        logger.exception('Do your custom error handling here. Logging it here!!')

##############################################################################################################

#define get all students records
def getStudents():
    try:
        response = table.scan()
        result = response['Items']

        #NOTE: if the table is large, there is a limit the scan method can get. Therefore we keep quering it using the 'LastEvaluatedKey'

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluateKey'])
            result.extend(response['Items'])

        body = {
            'students': result
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. Logging it here!!')

##############################################################################################################

#define save student info
def saveStudent(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. Logging it here!!')

#########################################################################################################################

#define modify student info method
def modifyStudent(studentId, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'studentId': studentId
            },
            UpdateExpression='set %s = :value' % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttrebutes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. Logging it here!!')

##############################################################################################################

#define delete student info method
def deleteStudent(studentId):
    try:
        response = table.delete_item(
            Key={
                'studentId': studentId
            },
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETED',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling here. Logging it here!!')

##############################################################################################################




