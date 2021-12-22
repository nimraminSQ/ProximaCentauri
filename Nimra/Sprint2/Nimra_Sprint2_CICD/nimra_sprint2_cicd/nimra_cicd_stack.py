from aws_cdk import (
    core as cdk,
    # aws_pipelines as pipelines,
    # aws_codepipeline_actions as cp_actions
    # aws_sqs as sqs,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class NimraCicdStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        print('I am running from Nimras sprint2 infra stack')
        
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "NimraSprint2CicdQueue",
        #     visibility_timeout=cdk.Duration.seconds(300),
        # )
