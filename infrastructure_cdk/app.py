#!/usr/bin/env python3
import os
import jsii
from aws_cdk import core

from infrastructure_cdk.lambda_stack import LambdaStack
from infrastructure_cdk.ecs_stack import EcsStack
from infrastructure_cdk.network_stack import NetworkStack
from infrastructure_cdk.instance_stack import InstanceStack

@jsii.implements(core.IAspect)
class CheckTerminationProtection:
    def visit(self, stack):
        if isinstance(stack, core.Stack):
            if (not stack.termination_protection):
                stack.node.add_warning("This stack doesen't have temination protection enabled!")

with open ("./user_data/user_data.sh") as f:
    USER_DATA = f.read()

app = core.App()
LambdaStack(app, "LambdaStack", 
    env = core.Environment(account = os.environ['CDK_DEFAULT_ACCOUNT'],
                           region = os.environ['CDK_DEFAULT_REGION']))
                           
Network = NetworkStack(app, "NetworkStack",
    env = core.Environment(account = os.environ['CDK_DEFAULT_ACCOUNT'],
                           region = os.environ['CDK_DEFAULT_REGION']))

InstanceStack(app, "InstanceStack",
    vpc = Network.vpc,
    user_data = USER_DATA,
    env = core.Environment(account = os.environ['CDK_DEFAULT_ACCOUNT'],
                           region = os.environ['CDK_DEFAULT_REGION']))

EcsStack(app, "EcsStack",
    vpc = Network.vpc,
    env = core.Environment(account = os.environ['CDK_DEFAULT_ACCOUNT'],
                           region = os.environ['CDK_DEFAULT_REGION']))

app.node.apply_aspect(CheckTerminationProtection())                           

app.synth()
