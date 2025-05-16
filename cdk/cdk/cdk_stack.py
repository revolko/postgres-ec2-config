from aws_cdk import (
    Stack,
)
from constructs import Construct

from aws_cdk.aws_ec2 import Vpc, IpAddresses, SubnetConfiguration, SubnetType


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = Vpc(
            self, "PostgresVPC", ip_addresses=IpAddresses.cidr("10.0.0.0/25"), availability_zones=["eu-central-1b"],
            restrict_default_security_group=False, enable_dns_hostnames=False, nat_gateways=0,
            subnet_configuration=[
                SubnetConfiguration(name="public", subnet_type=SubnetType.PUBLIC, map_public_ip_on_launch=True),
            ]
        )
