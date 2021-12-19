import boto3
import os

class dynamoDBTable:
    def __init__(self):
        self.resource = boto3.resource('dynamodb') 
        
    def dynamo_data(self, tableName, alarm_name, created_date):
        table = self.resource.Table(tableName)
        table_name=os.getenv('table_name')
        values = {}
        values['id'] = alarm_name
        values['createdDate'] = created_date
        
        table.put_item(Item = values)