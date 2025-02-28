/* ----------------------------------------------------------------------------
 * Name: 02_ecs_repository.tf
 *
 * Description: Builds the ECR repository, to which to push the application
 * image.
 * --------------------------------------------------------------------------*/


resource "aws_ecr_repository" "ecr_repository" {
  name                 = local.application_suffix
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  tags = local.tags
}

