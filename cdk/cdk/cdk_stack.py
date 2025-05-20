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
    UserData,
    MultipartUserData,
    MultipartBody,
)

from pathlib import Path


class CdkStack(Stack):

    AVAIL_ZONE = "eu-central-1b"
    ASSETS_PATH = Path(__file__).parents[1].joinpath("assets")

    def read_asset_file(self, file_name: str) -> str:
        with open(self.ASSETS_PATH.joinpath(file_name)) as file:
            return file.read()

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = Vpc(
            self, "PostgresVPC", ip_addresses=IpAddresses.cidr("10.0.0.0/25"), availability_zones=[self.AVAIL_ZONE],
            restrict_default_security_group=False, enable_dns_hostnames=False, nat_gateways=0,
            subnet_configuration=[
                SubnetConfiguration(name="public", subnet_type=SubnetType.PUBLIC, map_public_ip_on_launch=True),
            ]
        )

        cloud_init = self.read_asset_file("cloud-init.yaml")

        user_data_boot = UserData.for_linux()
        user_data_boot.add_commands(cloud_init)

        multipart = MultipartUserData()
        multipart.add_part(MultipartBody.from_user_data(user_data_boot, "text/cloud-boothook"))

        postgres_server = Instance(
            self, "PostgresInstance", vpc=vpc,
            instance_type=InstanceType.of(instance_class=InstanceClass.T3, instance_size=InstanceSize.SMALL),
            machine_image=MachineImage.generic_linux(
                {"eu-central-1": "ami-03250b0e01c28d196"},
                user_data=multipart,
            )
        )

        data_volume = Volume(
            self, "DataVolume", availability_zone=self.AVAIL_ZONE, size=Size.gibibytes(30),
        )
        data_volume.grant_attach_volume(postgres_server.role)
