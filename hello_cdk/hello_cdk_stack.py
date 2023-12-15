
import aws_cdk as core
#from aws_cdk import Stack, App, aws_s3 as s3
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns, 
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources,
    aws_dynamodb as ddb,
)

'''
app = core.App()
stack = core.Stack(app, "Stack", env=core.Environment(region="us-west-2"))
queue = sqs.Queue(
            stack, "HelloCdkQueue",
            visibility_timeout=Duration.seconds(300),
        )

aws_cdk(core/cdk -aws-cdk-lib) --> This AWS CDK construct library provides APIs to define your CDK application and add CDK constructs to the application.
To use this package, you need to declare this package and the constructs package as dependencies.

According to the kind of project you are developing:
For projects that are CDK libraries, declare them both under the devDependencies **and** peerDependencies sections.
For CDK apps, declare them under the dependencies section only.

stack -->A root construct which represents a single CloudFormation stack.


requirements.txt
aws-cdk-lib==2.60.0
constructs>=10.0.0,<11.0.0

This is a change from the previous version which is cdk version 1. 
In the previous version you had to import all of the independent or the specific rather AWS resources, that you want to work with 
as part of your project.
so for example, if you wanted to use S3, you had to go and find the S3 construct and import that into your project. if you wanted to use SQS 
you have to do the same thing. 

And just as a quick little primer, constructs are just kind of these encapsulations of cloud resources.
so it could be an SQS queue, it could be a Lambda function, it could be an S3 bucket or it could be a bunch of different things 
like an S3 bucket and a Lambda function. so that's a higher level "abstraction construct" but by default you
just get access to some generic ones that AWS provides for you. These are kind of, like the building blocks that you'll be using 
throughout this project. okay so that's it for requirements.txt
'''
#class HelloCdkStack(Stack):
class HelloCdkStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        myqueue = sqs.Queue(
            self, "HelloCdkQueue",
            visibility_timeout=Duration.seconds(300),
        )

        mytopic = sns.Topic(
            self, "HelloCdkTopic"
        )

        mytopic.add_subscription(subs.SqsSubscription(myqueue))

        iam.Group(self, "gid")

        #module.class.property -->(_lambda.Runtime.PYTHON_3_8)
        #module.class.method --> (_lambda.Code.from_asset('lambda'))
        sqs_lambda = _lambda.Function(self,"lambda",runtime=_lambda.Runtime.PYTHON_3_8, 
                                      code=_lambda.Code.from_asset('lambda'), 
                                      handler= 'lambda_handler.handler_name'
                                      function_name='mycdklambda')
        
        table=ddb.Table(self,"dynamodbtable",
                        table_name='myddbtable1', 
                        partition_key={'name': 'path', 
                                       'type': ddb.AttributeType.STRING}
                        )
        ddbtable= ddb.Table(self, "dynamodbtable", 
                            table_name='myddbtable2',
                            partition_key= ddb.Attribute(name="id", 
                                                         type= ddb.AttributeType.STRING)
                            )
        
        #create event source
        sqs_event_source = lambda_event_sources.SqsEventSource(myqueue)

        #add SQS event source to lambda
        sqs_lambda.add_event_source(sqs_event_source)



'''

import aws_cdk.aws_kinesis as kinesis

stream = ddb.Stream(self, "Stream")
table = ddb.Table(self, "Table",
            partition_key=ddb.Attribute(name="id", type=ddb.AttributeType.STRING),
            kinesis_stream=stream
        )


app = cdk.App()
HelloCdkStack(app, "hello-cdk")

'''

'''
"Module" is a collection of classes or methods/functions or variable/property or it can be combination of all 
class, methods and variable.
Each class is a collection of methods and properties
Each property might have its own function

Constructs(module) are classes (such as sqs, sns, lambda etc.,) 
which define a "piece of system state". 
Constructs(like sqs,sns,lambda) can be composed together to form higher-level building blocks which 
represent more complex state.

Constructs are often used to represent the *desired state* of cloud applications. 
For example, in the AWS CDK, which is used to define the desired state(complete/final infrastructure 
provisioning with all the three resources such as sns,sqs, and lambda using cloudformation template) 
for AWS infrastructure using CloudFormation, the lowest-level construct represents
 a *resource definition* (for SQS, SNS & Lambda) in a CloudFormation template. 
These resources are composed to represent higher-level logical units of a cloud 
application, etc.

desired state = represent higher-level logical units of a cloud application

Represents the building block of the construct graph.
All constructs besides the root construct must be created within the scope of 
stack.
'''
chatGPT question:
can you please explain CDK construct and scope of construct with simple example?

# 'HelloCdkStack' is a construct that represents an AWS CloudFormation stack.
# 'myqueue' is a construct that represents an sqs queue.
# The scope of 'myqueue' construct is 'HelloCdkStack', indicating that it is defined within the 
# context of the 'HelloCdkStack' stack.
mytopic is a construct that represents a SNS topic
sqs_lambda is a construct that represents a lambda function
sqs_event_source is a construct that represents a SQS event source

In the context of AWS Cloud Development Kit (CDK), a construct is a fundamental building block of
AWS infrastructure using CloudFormation for building any cloud application.
It represents a piece of AWS infrastructure. 
A CDK app is essentially made up of constructs that define various AWS resources and 
their relationships.

Here's a simple breakdown:

Construct:
A construct is a higher-level abstraction that represents an AWS resource or a set of resources.
It could be something like an S3 bucket, a Lambda function, or an entire VPC.

Scope:
The scope of a construct(myqueue,mytopic,sqs_lambda,sqs_event_source) 
refers to where it exists(under what app stack it is getting created)
within the CDK apps hierarchy. 
Constructs can be nested within each other, forming a tree-like structure (see "tree.json"). 
The scope determines the context in which a construct is defined.

scope: the first argument is always the scope in which this construct is created. 
In almost all cases, you’ll be defining constructs within the scope of current construct, 
which means you’ll usually just want to pass "self" for the first argument.
Make a habit out of it.

id: the second argument is the local identity of the construct. 
It’s an ID that has to be unique amongst construct within the same scope. 
The CDK uses this identity to calculate the CloudFormation Logical ID for each resource defined
within this scope
https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html#identifiers_logical_ids

kwargs: the last (sometimes optional) arguments is always a set of initialization arguments. 
Those are specific to each construct. For example, the lambda.Function construct accepts 
arguments like runtime, code and handler. 
You can explore the various options using your IDE’s auto-complete or online documentation
https://docs.aws.amazon.com/cdk/api/v1/docs/aws-lambda-readme.html

constructs module
https://docs.aws.amazon.com/cdk/api/v1/docs/constructs-readme.html
AWS CDK Python Reference
https://docs.aws.amazon.com/cdk/api/v1/python/


So far, it seems like the only tool we have at our disposal to update our stack is cdk deploy.
But cdk deploy takes time; it has to deploy your CloudFormation stack and upload the 
lambda directory from your disk to the boostrap bucket. If we’re just changing our lambda code,
we don’t actually need to update the CloudFormation stack, so that part of cdk deploy is wasted
effort.
We really only need to update our lambda code. It would be great if we had some 
other mechanism for doing only that… which is "Hotswap deployments"

This command deliberately introduces drift in CloudFormation stacks in order to speed up 
deployments. For this reason, only use it for development purposes. 
*****Never use hotswap for your production deployments!*****

We can speed up that deployment time with cdk deploy --hotswap, which will assess whether a
hotswap deployment can be performed instead of a CloudFormation deployment.
If possible, the CDK CLI will use AWS service APIs to directly make the changes; 
otherwise it will fall back to performing a full CloudFormation deployment.

cdk deploy --hotswap 
to deploy a hotswappable change to your AWS Lambda asset code

We can do better than calling "cdk deploy" or "cdk deploy --hotswap" each time. 
"cdk watch" is similar to cdk deploy except that instead of being a one-shot operation, 
it monitors your code and assets for changes and attempts to perform a deployment 
automatically when a change is detected. By default, "cdk watch" will use the --hotswap flag,
which inspects the changes and determines if those changes can be hotswapped. 
Calling "cdk watch --no-hotswap" will disable the hotswap behavior.

Looking at your cdk.json file
When the cdk watch command runs, the files that it observes are determined by the "watch" setting
in the "cdk.json" file. It has two sub-keys, "include" and "exclude", each of which can be either
a single string or an array of strings. Each entry is interpreted as a path relative to the 
location of the cdk.json file. Globs, both * and **, are allowed to be used.

if you want "cdk watch" to watch other files, you can change the settings of the "include" in 
the "cdk.json" file 

lambda logs:
https://cdkworkshop.com/30-python/40-hit-counter/500-logs.html


    
