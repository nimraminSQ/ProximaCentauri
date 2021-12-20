import boto3
import os

import constants as constants

class DynamoDBTable:
    def __init__(self):
        self.resource = boto3.resource('dynamodb') 
        
    def dynamo_put_data(self, MessageID, Timestamp, Url):
        
        table_name=os.getenv('table_name') # Get the table_name from environment var
        table = self.resource.Table(table_name) #Get table from dynamodb with name table_name
        
        #Inserts data intot the dynamodb table
        table.put_item(TableName=table_name, 
        Item={
        'MessageID': MessageID,
        'TimeStamp': Timestamp,
        'url': Url,
        })
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       