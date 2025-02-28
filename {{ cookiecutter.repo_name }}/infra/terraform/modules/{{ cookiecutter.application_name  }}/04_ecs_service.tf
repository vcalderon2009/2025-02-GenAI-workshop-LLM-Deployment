/* ----------------------------------------------------------------------------
 * Name: 05_ecs_service.tf
 *
 * Description: Create a ECS Service for {{ cookiecutter.project_name }} Task Definition
 * --------------------------------------------------------------------------*/

resource "aws_ecs_service" "ecs_api_service" {
  name                              = "${local.application_suffix}-svc"
  cluster                           = aws_ecs_cluster.ecs_cluster.id
  task_definition                   = aws_ecs_task_definition.ecs_task_definition.arn
  desired_count                     = 1
  health_check_grace_period_seconds = 1000
  launch_type                       = "FARGATE"
  platform_version                  = "1.3.0"
  network_configuration {
    subnets          = var.public_subnets
    security_groups  = [aws_security_group.application_svc_sg.id]
    assign_public_ip = true
  }


  load_balancer {
    target_group_arn = aws_lb_target_group.application_tg.arn
    container_name   = "${local.application_suffix}-api"
    container_port   = 8000
  }
}
