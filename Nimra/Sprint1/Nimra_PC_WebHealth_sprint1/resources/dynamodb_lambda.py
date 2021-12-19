import boto3,os
def lambda_handler(event, context):
    db=boto3.client('dynamodb')
    MessageID = event['Records'][0]['Sns']['Message']
    Timestamp = event['Records'][0]['Sns']['Timestamp']
    table_name=os.getenv('table_name')
    db.put_item(TableName=table_name,Item={
        'MessageID':{'S':MessageID},
        'TimeStamp':{'S':Timestamp},
    })
    #print("From SNS: " + message)
   # return message





# import json
# from dynamoDBTable import dynamoDBTable
# import constants


# def lambda_handler(events, context):
#     ddb = dynamoDBTable();
#     print('evvents: ', events)
#     mesg = events['Records'][0]['Sns']['Message']
#     mesg = json.loads(mesg)
    
#     alarm_name =  mesg['AlarmName']
#     created_date = mesg['StateChangeTime']
#     print('printing mesg, alarm_name and created_date', mesg, alarm_name, created_date)
#     ddb.dynamo_data(constants.TABLE_NAME, 'Latency_'+created_date, created_date)
