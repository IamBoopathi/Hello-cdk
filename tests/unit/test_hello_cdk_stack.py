import aws_cdk as core
import aws_cdk.assertions as assertions
from hello_cdk.hello_cdk_stack import HelloCdkStack


'''
app = core.App()
stack = core.Stack(app, "Stack", env=core.Environment(region="us-west-2"))
queue = sqs.Queue(
            stack, "HelloCdkQueue",
            visibility_timeout=Duration.seconds(300),
        )
'''

def test_sqs_queue_created():
    app = core.App()
    stack = HelloCdkStack(app, "hello-cdk")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = HelloCdkStack(app, "hello-cdk")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)


