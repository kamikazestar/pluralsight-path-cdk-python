from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    aws_autoscaling as autoscaling,
    aws_iam as iam,
    core
)


class InstanceStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, asg_min = 2, asg_max = 5, ec2_type = 't3.micro', user_data = "", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        bastion = ec2.BastionHostLinux(self, "Bastion",
            vpc = vpc,
            subnet_selection = ec2.SubnetSelection(subnet_type = ec2.SubnetType.PRIVATE),
            instance_name = "bastion-host",
            instance_type = ec2.InstanceType(instance_type_identifier = ec2_type)
        )

        ssm_policy = iam.PolicyStatement(
            effect = iam.Effect.ALLOW,
            resources = ["*"],
            actions = ["ssmmessages:*", "ssm:UpdateInstanceInformation", "ec2messages:*"]
        )
        
        alb = elb.ApplicationLoadBalancer(self, "ALB",
            vpc = vpc,
            internet_facing = True,
            load_balancer_name = "myALB"
        )
        
        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Internet access ALB 80")
        
        listener = alb.add_listener("Web", port = 80, open = True)
        
        linux_ami = ec2.AmazonLinuxImage(generation = ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition =ec2.AmazonLinuxEdition.STANDARD,
            virtualization = ec2.AmazonLinuxVirt.HVM,
            storage = ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )
        
        self.asg = autoscaling.AutoScalingGroup(self, "Globalmantics-Web",
            vpc = vpc,
            vpc_subnets = ec2.SubnetSelection(subnet_type = ec2.SubnetType.PRIVATE),
            instance_type = ec2.InstanceType(instance_type_identifier = ec2_type),
            machine_image = linux_ami,
            user_data = ec2.UserData.custom(user_data),
            desired_capacity = asg_min,
            min_capacity = asg_min,
            max_capacity = asg_max,
        )
        
        self.asg.add_to_role_policy(ssm_policy)
        
        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access port 80 of EC2 in ASG")
        
        listener.add_targets("addTargetGroup", port = 80, targets = [self.asg])
        
        core.CfnOutput(self, "ElbEndpoint", value = alb.load_balancer_dns_name)
        