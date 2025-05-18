from aws_cdk import (
    Stack,
    Size,
)
from constructs import Construct

from aws_cdk.aws_ec2 import (
    Vpc,
    IpAddresses,
    SubnetConfiguration,
    SubnetType,
    Instance,
    InstanceType,
    InstanceClass,
    InstanceSize,
    MachineImage,
    Volume,
)


class CdkStack(Stack):

    AVAIL_ZONE = "eu-central-1b"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = Vpc(
            self, "PostgresVPC", ip_addresses=IpAddresses.cidr("10.0.0.0/25"), availability_zones=[self.AVAIL_ZONE],
            restrict_default_security_group=False, enable_dns_hostnames=False, nat_gateways=0,
            subnet_configuration=[
                SubnetConfiguration(name="public", subnet_type=SubnetType.PUBLIC, map_public_ip_on_launch=True),
            ]
        )

        postgres_server = Instance(
            self, "PostgresInstance", vpc=vpc,
            instance_type=InstanceType.of(instance_class=InstanceClass.T3, instance_size=InstanceSize.SMALL),
            machine_image=MachineImage.generic_linux({"eu-central-1": "ami-03250b0e01c28d196"})
        )

        data_volume = Volume(
            self, "DataVolume", availability_zone=self.AVAIL_ZONE, size=Size.gibibytes(30),
        )
        data_volume.grant_attach_volume(postgres_server.role)
