
# Sprint1: Web Health Monitoring 
## Project Summary:
<br/> For Sprint 1 at SkipQ, we have designed a web health monitoring system, that periodically monitors the web health metrics (i.e. latency and availability) and then raises an alarm If any of the metric breaches a specified threshold. The rasied alarms are to be stored in a dynamodb table.
<br/>
![Alt text](./architecture.png "Title")
<br/>
## GOALS
1. Create a periodic Lambda Function, that checks latency and availability of a specified url at some predefined periodic time.
2. Connect that periodic lambda function with cloud watch, by publishing the latency and availability metric to CloudWatch.
3. Generate an alarm, if the CloudWatch’s metric breaches a certain threshold.
4. Create an SNS Topic that notifies(emails) its subscribers of the breached threshold by sending them an alarm message.
5. Create A table in DynamoDB for keeping a record of the alarm messages.
6. Create another SNS subscription that triggers a lambda function to write into DynamoDB whenever an alarm is triggered.
7. Now, run this application for 4 URLS, by retrieving them from an S3 Bucket.

Services Used 
------------- |
AWS Dynamodb |
AWS Cloudwatch |
S3 buckets |
AWS lambda |
AWS SNS |
AWS events |
AWS events target |

## Installation Guide
1. Clone the repository.
2. cd into the cloned repository.
3. Install requirements with the command pip install -r requirements.txt
4. Type in cdk synth && cdk deploy for deployment.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Author: 
for any queries reach out at:
Name: Nimra Amin
Email: nimra.amin.s@skipq.org

Enjoy!