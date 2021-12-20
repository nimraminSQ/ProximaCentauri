import boto3,os
import constants as constants
from dynamoDBTable import DynamoDBTable

def lambda_handler(event, context):
    MessageID = event['Records'][0]['Sns']['MessageId'] #A unique Identifier (partition key)
    Timestamp = event['Records'][0]['Sns']['Timestamp'] #Alarm occurrence time
    db_table = DynamoDBTable() # class that contains put_data function
    print(MessageID)
    db_table.dynamo_put_data(MessageID= MessageID, Timestamp= Timestamp, Url= constants.URL_TO_MONITOR)
    
 