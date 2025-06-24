resource "aws_lb" "todo_alb" {
  name               = "ToDo-App-ALB"
  subnets            = aws_subnet.public.*.id
  load_balancer_type = "application"
  security_groups    = [aws_security_group.todo_alb_sg.id]

  tags = {
    Environment = var.environment
    Application = var.app_name
  }
}


resource "aws_lb_target_group" "todo_tgroup" {
  name        = "${var.app_name}-alb-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.todo_vpc.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "15"
    protocol            = "HTTP"
    matcher             = "200-299"
    timeout             = "10"
    path                = "/healthcheck"
    unhealthy_threshold = "2"
  }
}

resource "aws_lb_listener" "http_redirect" {
  load_balancer_arn = aws_lb.todo_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https_forward" {
  load_balancer_arn = aws_lb.todo_alb.arn
  port              = 443
  protocol          = "HTTPS"

  ssl_policy      = "ELBSecurityPolicy-TLS-1-2-Ext-2018-06"
  certificate_arn = "arn:aws:acm:us-east-1:327083199573:certificate/482b572d-781f-461f-9423-9daf1a913c7c"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.todo_tgroup.arn
  }
}

