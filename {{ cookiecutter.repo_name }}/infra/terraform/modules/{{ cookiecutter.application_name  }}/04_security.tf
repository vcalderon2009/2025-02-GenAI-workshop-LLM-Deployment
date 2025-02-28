/* ----------------------------------------------------------------------------
 * Name: 04_security_groups.tf
 *
 * Description: Create Secuity groups for network secuity in ECS Service and ALB
 * --------------------------------------------------------------------------*/

resource "aws_security_group" "application_alb_sg" {
  name        = "${var.application}-alb-sg"
  description = "Security group for ALB allowing HTTP and HTTPS traffic"
  vpc_id      = var.default_vpc

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "application_svc_sg" {
  name        = "${var.application}-service-sg"
  description = "Security group for ECS service to accept traffic from ALB"
  vpc_id      = var.default_vpc

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "allow-service-traffic-from-alb" {
  type                     = "ingress"
  from_port                = 8000
  to_port                  = 8000
  protocol                 = "tcp"
  security_group_id        = aws_security_group.application_svc_sg.id
  source_security_group_id = aws_security_group.application_alb_sg.id
}
