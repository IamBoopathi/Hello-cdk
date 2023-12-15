#!/usr/bin/env python3

import aws_cdk as cdk
#from aws_cdk import Stack, App, aws_s3 as s3

from hello_cdk.hello_cdk_stack import HelloCdkStack


app = cdk.App()
HelloCdkStack(app, "hello-cdk")

app.synth()
