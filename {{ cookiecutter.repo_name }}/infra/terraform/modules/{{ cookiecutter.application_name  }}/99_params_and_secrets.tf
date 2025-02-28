/* ----------------------------------------------------------------------------
 * Name: 99_params_and_secrets.tf
 *
 * Description: Infra metadata that gets stored in the Parameter Store Manager.
 *              This will be used by the application code for lookup purposes.
 * --------------------------------------------------------------------------*/

resource "aws_ssm_parameter" "app_params" {
  name        = "/${var.application}/${var.env_name}/config"
  description = "Application Infra Lookup Values"
  type        = "SecureString"

  value = jsonencode(
    {
      ecs_task_definition     = "${aws_ecs_task_definition.ecs_task_definition.family}:${aws_ecs_task_definition.ecs_task_definition.revision}"
      ecs_task_container      = "${var.application}-${local.env}"
      ecs_cluster             = aws_ecs_cluster.ecs_cluster.name
      ecr_repo                = aws_ecr_repository.ecr_repository.repository_url
      ecr_repository_name     = aws_ecr_repository.ecr_repository.name
      ecr_registry_id         = aws_ecr_repository.ecr_repository.registry_id
      ecs_subnets             = var.subnets
      ecs_security_group_name = aws_security_group.application_svc_sg.name
      ecs_security_group_id   = aws_security_group.application_svc_sg.id
    }
  )

  tags = local.tags
}
