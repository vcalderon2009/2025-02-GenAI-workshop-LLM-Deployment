/* ----------------------------------------------------------------------------
 * Name: 03_ecs_task_definition.tf
 *
 * Description: Creates ECS Fargate Task Definition and adds associated roles and policies
 * --------------------------------------------------------------------------*/

# ----------------------------------- LOGS ------------------------------------

# ---- CloudWatch Log Groups

resource "aws_cloudwatch_log_group" "application_log_group" {
    name = "/aws/ecs/microservices-${local.application_suffix}"
    retention_in_days = 30
}

# -------------------------------- IAM ROLES ----------------------------------

# ---- ECS Execution Role
resource "aws_iam_role" "ecs_exec_role" {
  name = "${local.application_suffix}-exec"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Sid    = ""
          Principal = {
            Service = "ecs-tasks.amazonaws.com"
          }
        }
      ]
    }
  )

  tags = local.tags

}


# ---- ECS Task Role
resource "aws_iam_role" "ecs_task_role" {
  name = "${local.application_suffix}-task"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17",
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Sid    = ""
          Principal = {
            Service = "ecs-tasks.amazonaws.com"
          }
        },
      ]
    }
  )

  tags = local.tags
}

# ------------------------------ IAM POLICIES ---------------------------------

# ---- Secrets Manager Policy
resource "aws_iam_policy" "secrets_manager_policy" {
    name = "SecretsManagerReadPolicy-${local.application_suffix}"
    policy = jsonencode(
        {
            Version = "2012-10-17",
            Statement = [
                {
                    Action = [
                        "secretsmanager:GetSecretValue"
                    ],
                    Effect = "Allow",
                    Resource = "arn:aws:secretsmanager:${var.region_name}:${var.aws_account_id}:secret:${var.huggingface_secret_name}"
                }
            ]

        }
    )
}

resource "aws_iam_policy" "ecr_task_manager_policy" {
    name = "ECSTaskECRPolicy-${local.application_suffix}"
    policy = jsonencode(
        {
            Version = "2012-10-17",
            Statement = [
                {
                    Action = [
                            "ecr:BatchCheckLayerAvailability",
                            "ecr:BatchGetImage",
                            "ecr:CompleteLayerUpload",
                            "ecr:GetDownloadUrlForLayer",
                            "ecr:InitiateLayerUpload",
                            "ecr:PutImage",
                            "ecr:UploadLayerPart"
                    ],
                    Effect = "Allow",
                    Resource = "arn:aws:ecr:${var.region_name}:${var.aws_account_id}:repository/${local.application_suffix}"
                },
                {
                    Action = [
                            "ecr:GetAuthorizationToken"
                    ],
                    Effect = "Allow",
                    Resource = "*"
                }
            ]

        }
    )
}


# ----------------------- IAM POLICIES - ATTACHMENT ---------------------------

resource "aws_iam_role_policy_attachment" "ecs_secrets_manager_attach" {
    role = aws_iam_role.ecs_task_role.name
    policy_arn = aws_iam_policy.secrets_manager_policy.arn
}

resource "aws_iam_role_policy_attachment" "ecr_repository_manager_attach" {
    role = aws_iam_role.ecs_exec_role.name
    policy_arn = aws_iam_policy.ecr_task_manager_policy.arn
}

# --------------------------- ECS TASK DEFINITION -----------------------------

# ---- ECS Task Definition

resource "aws_ecs_task_definition" "ecs_task_definition" {
    family = local.application_suffix
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    execution_role_arn = aws_iam_role.ecs_exec_role.arn
    task_role_arn = aws_iam_role.ecs_task_role.arn
    cpu = var.cpu
    memory = var.memory

    container_definitions = jsonencode(
        [
            {
                name = "${local.application_suffix}-api"
                image = "${aws_ecr_repository.ecr_repository.repository_url}:latest"
                essential = true
                logConfiguration = {
                logDriver     = "awslogs"
                secretOptions = []
                "options" : {
                    "awslogs-group" : aws_cloudwatch_log_group.application_log_group.name,
                    "mode" : "non-blocking",
                    "awslogs-create-group" : "true",
                    "max-buffer-size" : "25m",
                    "awslogs-region" : var.region_name,
                    "awslogs-stream-prefix" : "ecs"
                },
              }
                portMappings = [
                    {
                        containerPort = 8000
                        hostPort      = 8000
                        protocol      = "tcp"
                    }
                ]
                "environment" : [
                    {
                        "name": "HF_CREDENTIALS_SECRET_NAME",
                        "value": "${var.huggingface_secret_name}"
                    },
                    {
                      "name" : "AWS_REGION",
                      "value" : "${var.region_name}"
                    },
                    {
                      "name" : "ENV",
                      "value" : "${var.env_name}"
                    }
                ]
            }
        ]
    )

    runtime_platform {
        operating_system_family = "LINUX"
        cpu_architecture = "X86_64"
    }


}




