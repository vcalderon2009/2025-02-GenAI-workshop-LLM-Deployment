/* ----------------------------------------------------------------------------
 * Name: 05_load_balancer.tf
 *
 * Description: Create an ALB to handle service traffic routing
 * --------------------------------------------------------------------------*/

resource "aws_lb" "application_alb" {
  name               = "lb-${application_suffix}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.application_alb_sg.id]
  subnets            = var.public_subnets
}

resource "aws_lb_target_group" "application_tg" {
  name        = "${var.application}-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.default_vpc
  target_type = "ip"

  health_check {
    path                = "/api/health"
    port                = 8000
    interval            = 300
    timeout             = 100
    healthy_threshold   = 5
    unhealthy_threshold = 5
    matcher             = "200"
  }
}

resource "aws_lb_listener" "application_alb_http_listener" {
  load_balancer_arn = aws_lb.application_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
      host        = "#{host}"
      path        = "/#{path}"
      query       = "#{query}"
    }
  }
}

resource "aws_lb_listener" "application_alb_https_listener" {
  load_balancer_arn = aws_lb.application_alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.application_tg.arn
  }
}

resource "aws_route53_record" "application_record" {
  zone_id = var.route53_zone_id
  name    = var.subdomain_name
  type    = "A"

  alias {
    name                   = aws_lb.application_alb.dns_name
    zone_id                = aws_lb.application_alb.zone_id
    evaluate_target_health = true
  }
}
