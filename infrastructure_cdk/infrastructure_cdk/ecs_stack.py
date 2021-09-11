from aws_cdk import (
    aws_ecs as ecs,
    aws_ecr_assets as ecr_assets,
    aws_ecs_patterns as ecs_patterns,
    core
)


class EcsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        cluster = ecs.Cluster(self, "Globalmantics-Ecs-Cluster", vpc = vpc)
        
        image_asset = ecr_assets.DockerImageAsset(self, "Globalmantics-Landing-Page",
            directory = "./globalmantics-container-app")
            
        image = ecs.ContainerImage.from_docker_image_asset(image_asset)
        
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "Globalmantics-Fargate",
            cluster = cluster,
            cpu = 256,
            memory_limit_mib = 512,
            desired_count = 3,
            listener_port = 80,
            task_image_options = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image = image,
                    container_name = "Globalmantics-Landing-Page",
                    container_port = 80,
                ),
            public_load_balancer = True,
        )

        