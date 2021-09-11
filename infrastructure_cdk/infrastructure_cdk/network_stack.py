from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, 
        cidr = "10.0.0.0/16", subnet_mask = 24, nat_gateways = 1,
        db_port = 5432,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.vpc = ec2.Vpc(self, "VPC",
            max_azs = 6,
            cidr = cidr,
            nat_gateways = nat_gateways,
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    subnet_type = ec2.SubnetType.PUBLIC,
                    name = "Public",
                    cidr_mask = subnet_mask
                ),
                ec2.SubnetConfiguration(
                    subnet_type = ec2.SubnetType.PRIVATE,
                    name = "Private",
                    cidr_mask = subnet_mask
                ),
                ec2.SubnetConfiguration(
                    subnet_type = ec2.SubnetType.ISOLATED,
                    name = "ISOLATED",
                    cidr_mask = subnet_mask
                ),
            ]
        )
        
        public_subnets = self.vpc.public_subnets
        private_subnets = self.vpc.private_subnets
        isolated_subnets = self.vpc.isolated_subnets
        
        isolated_nacl = ec2.NetworkAcl(self, "DBNacl",
            vpc = self.vpc,
            subnet_selection = ec2.SubnetSelection(subnets = isolated_subnets)
        )
        
        for id, subnet in enumerate (private_subnets, start = 1):
            
            isolated_nacl.add_entry("DBNaclIngress{0}".format(id*100),
                rule_number = id * 100,
                #cidr = ec2.AclCidr.ipv4(ec2.PrivateSubnet.ipv4_cidr_block),
                cidr = ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                traffic = ec2.AclTraffic.tcp_port_range(db_port, db_port),
                rule_action = ec2.Action.ALLOW,
                direction = ec2.TrafficDirection.INGRESS
            )
            
            isolated_nacl.add_entry("DBNaclEgress{0}".format(id*100),
                rule_number = id * 100,
                #cidr = ec2.AclCidr.ipv4(ec2.PrivateSubnet(self, subnet).ipv4_cidr_block),
                cidr = ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                traffic = ec2.AclTraffic.tcp_port_range(1024, 65535), # RFC 6056
                rule_action = ec2.Action.ALLOW,
                direction = ec2.TrafficDirection.EGRESS
            )