from aws_cdk import (
    core as cdk,
    pipelines as pipelines,
    aws_codepipeline_actions as cp_actions
    # aws_sqs as sqs,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from nimra_sprint2_cicd.nimra_beta_stage import NimraBetaStage

class NimraPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        source_pipeline = pipelines.CodePipelineSource.git_hub(repo_string = "nimraminSQ/ProximaCentauri",
                                             branch="main",
                                             authentication=cdk.SecretValue.secrets_manager("n_sprint2_gitAuth"), # optional but recommended
                                             trigger = cp_actions.GitHubTrigger.POLL
                                             )
        
        synth_pipeline = pipelines.ShellStep("Synth",
                                            input=source_pipeline,
                                            commands=["ls Nimra", "pwd",
                                                      "cd Nimra/Sprint2/Nimra_Sprint2_CICD",
                                                      "alias python=python3" ,
                                                      "pip install -r requirements-aws.txt",
                                                    #   "pip install -r requirements.txt -t ./infra/resources/dependencies", # for installing external lambda files
                                                      "npm install -g aws-cdk",
                                                      "cdk synth"],
                                            primary_output_directory = "./Nimra/Sprint2/Nimra_Sprint2_CICD/cdk.out"
    )
        pipeline = pipelines.CodePipeline(self,
                                          'NimraPipeline',
                                          synth = synth_pipeline,
                                          self_mutation = True)
        
        beta = NimraBetaStage(self,
                              "NimraBetaStageCICD")
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "NimraSprint2CicdQueue",
        #     visibility_timeout=cdk.Duration.seconds(300),
        # )
        
        pipeline.add_stage(beta,)
                        #   pre= [unit test])