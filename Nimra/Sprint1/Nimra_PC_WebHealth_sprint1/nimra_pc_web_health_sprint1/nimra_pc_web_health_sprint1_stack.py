from aws_cdk import (
    core as cdk,
    # aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _events_targets,
    aws_iam as aws_iam,
    aws_cloudwatch as _cloudwatch,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as ddb,
    
    aws_s3 as s3, 
    aws_sqs as sqs,
    # aws_s3_notifications as s3_noti,
)

from aws_cdk import core
import os

from resources import constants as constants
class NimraPcWebHealthSprint1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

         # Creating a Lambda function, which calls the Hello World Handler
        # HW_lambda = self.create_lambda("Hello World!", "./resources/", "HelloWorld_lambda.lambda_handler")
        lambda_role = self.create_lambda_role()
        # Creating a Lambda function, which creates and calls the WebHealth Lambda Function
        WH_lambda = self.create_lambda("WebHealthPeriodicLambda", "./resources/", "webHealth_lambda.lambda_handler", lambda_role)
        ddb_lambda_producer = self.create_lambda('Nimra_DDB_PRODUCER', './resources/','dynamodb_lambda.lambda_handler' ,lambda_role)
        
        
        lambda_schedule = _events.Schedule.rate(cdk.Duration.minutes(1))
        lambda_targets = _events_targets.LambdaFunction(handler=WH_lambda)
        rule = _events.Rule(self, "webHealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        #SNS TOPIC 
        topic = sns.Topic(self, "Nimra_webHealthAlarm_sprint1")
        topic.add_subscription(subscriptions.EmailSubscription(
                                                email_address = "nimra.amin.s@skipq.org"))
            
        topic.add_subscription(subscriptions.LambdaSubscription(
                                                fn=ddb_lambda_producer))
                                                
        #  for puclishing aws metrics to cloued watch                      
        dimensions = {'URL': constants.URL_TO_MONITOR}
        availability_metric = _cloudwatch.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = 'AVAILABILITY ALARM METRIC')
        #Setting up the availability alarm
        availability_alarm = _cloudwatch.Alarm(self, 
                                            id ='NimraAvailabilityAlarm',
                                            metric = availability_metric,
                                            comparison_operator =_cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                                            datapoints_to_alarm = 1,
                                            evaluation_periods = 1,
                                            threshold = 1, 
                                            )
    
    
    
        #  for puclishing aws metrics to cloued watch                      
       
        dimensions = {'URL': constants.URL_TO_MONITOR}
        latency_metric = _cloudwatch.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = 'LATENCY ALARM METRIC')
         #Setting up the availability alarm
        latency_alarm = _cloudwatch.Alarm(self, 
                                            id ='NimraLatencyAlarm',
                                            metric = latency_metric,
                                            comparison_operator =_cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                            datapoints_to_alarm = 1,
                                            evaluation_periods = 1,
                                            threshold = .25 #.34
                                            )
        
        availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))
        latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        #### CREATING A DYNAMODB TABLE
         #create table in dynamo db
        try:
            ddb_alarm_table= self.create_ddb_table()
        except: pass
        
        #give read write permissions to our lambda
        ddb_alarm_table.grant_read_write_data(ddb_lambda_producer)
        ###defining SNS service    
        ddb_lambda_producer.add_environment('table_name',constants.TABLE_NAME)
        
        
        s3bucket= s3.Bucket(self, "Nimra_webHealthsprint1_bucket")
         #create a queue that will get bucket events
        queue = sqs.Queue(self, 'Nimra_webheathsprin1_bucket_queue',
        visibility_timeout=cdk.Duration.seconds(300) )
        # Now, create an event on bucket that will work with sqs queue
        # s3bucket.add_event_notification( s3.EventType.OBJECT_CREATED, s3_noti.SqsDestination(queue) )
    
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
                        assumed_by = aws_iam.CompositePrincipal(
                                     aws_iam.ServicePrincipal("lambda.amazonaws.com"),
                                     aws_iam.ServicePrincipal("sns.amazonaws.com") ),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                        ])
            
        return lambdaRole
        
        
    def create_lambda(self, id, asset, handler, role):
        ### Creates a lambda function in python3.6
        return _lambda.Function(self, 
        id,
        handler=handler,  # optional, defaults to 'handler'
        runtime=_lambda.Runtime.PYTHON_3_6,
        code=_lambda.Code.from_asset(asset),
        role=role
        )
    
    def create_ddb_table(self, ):
        # return ddb.Table(self,
        #                 id="Nimra_Table",
        #                 table_name=constants.TABLE_NAME,
        #                 partition_key=ddb.Attribute(name="id", type=ddb.AttributeType.STRING)) 
        #                 # sort_key=ddb.Attribute(name="createdDate", type=ddb.AttributeType.STRING))
        return ddb.Table(self, 
                        id="Nimra_Table",
                        table_name=constants.TABLE_NAME,
                        partition_key=ddb.Attribute(name="MessageID", type=ddb.AttributeType.STRING))    
  