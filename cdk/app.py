#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack


app = cdk.App()
env = cdk.Environment(region="eu-central-1")
CdkStack(app, "PostgresStack", env=env)

app.synth()
