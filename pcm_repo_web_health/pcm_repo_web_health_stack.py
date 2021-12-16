from aws_cdk import (
    core as cdk,
    # aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _events_targets,
    aws_iam as aws_iam,
    aws_cloudwatch as _cloudwatch
)

from resources import constants as constants
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PcmRepoWebHealthStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Creating a Lambda function, which calls the Hello World Handler
        # HW_lambda = self.create_lambda("Hello World!", "./resources/", "HelloWorld_lambda.lambda_handler")
        lambda_role = self.create_lambda_role()
        # Creating a Lambda function, which creates and calls the WebHealth Lambda Function
        WH_lambda = self.create_lambda("Hello World!", "./resources/", "webHealth_lambda.lambda_handler", lambda_role)
        
        lambda_schedule = _events.Schedule.rate(cdk.Duration.minutes(1))
        lambda_targets = _events_targets.LambdaFunction(handler=WH_lambda)
        rule = _events.Rule(self, "webHealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        
        
        dimensions = {'URL': constants.URL_TO_MONITOR}
        availability_metric = _cloudwatch.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = 'LATENCY METRIC')
        availability_alarm = _cloudwatch.Alarm(self, 
                                            id ='NimraAvailabilityAlarm',
                                            metric = availability_metric,
                                            comparison_operator =_cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                                            datapoints_to_alarm = 1,
                                            evaluation_periods = 1,
                                            threshold = 1, 
                                            )
    
    
    
        dimensions = {'URL': constants.URL_TO_MONITOR}
        latency_metric = _cloudwatch.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                        metric_name=constants.URL_MONITOR_NAME_LATENCY,
                        dimensions_map = dimensions,
                        period = cdk.Duration.minutes(1),
                        label = 'LATENCY METRIC')
        latency_alarm = _cloudwatch.Alarm(self, 
                                            id ='NimraLatencyAlarm',
                                            metric = latency_metric,
                                            comparison_operator =_cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                            datapoints_to_alarm = 1,
                                            evaluation_periods = 1,
                                            threshold = .28 #.34
                                            )
    
    
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
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
    
   