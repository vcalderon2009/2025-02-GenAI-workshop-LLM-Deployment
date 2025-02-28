/* ----------------------------------------------------------------------------
 * Name: 01_ecs_cluster.tf
 *
 * Description: Builds the ECS Cluster for the microservices environment
 * --------------------------------------------------------------------------*/


resource "aws_ecs_cluster" "ecs_cluster" {
  name = local.application_suffix

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = local.tags
}
