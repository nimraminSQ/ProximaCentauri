from aws_cdk import (
    core as cdk,
    # aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_events as aws_events,
    aws_events_targets as aws_events_targets
)

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
        
        # Creating a Lambda function, which creates and calls the WebHealth Lambda Function
        WH_lambda = self.create_lambda("Hello World!", "./resources/", "webHealth_lambda.lambda_handler")
         
    def create_lambda(self, id, asset, handler):
        ### Creates a lambda function in python3.6
        return _lambda.Function(self, 
        id,
        handler=handler,  # optional, defaults to 'handler'
        runtime=_lambda.Runtime.PYTHON_3_6,
        code=_lambda.Code.from_asset(asset)
        )
    
   