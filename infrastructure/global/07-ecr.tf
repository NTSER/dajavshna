resource "aws_ecr_repository" "todo_app" {
  name = var.app_name
}

resource "aws_ecr_repository" "redis" {
  name = "redis"
}
