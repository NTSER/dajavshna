[
  {
    "name": "${container_name}",
    "image": "${aws_ecr_repository}:${tag}",
    "essential": true,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "${aws_cloudwatch_log_group_name}-service",
        "awslogs-group": "${aws_cloudwatch_log_group_name}"
      }
    },
    "portMappings": [
      {
        "containerPort": 5000,
        "hostPort": 5000,
        "protocol": "tcp"
      }
    ],
    "cpu": 1,
    "environment": [
      {
        "name": "POSTGRES_USER",
        "value": "${postgres_username}"
      },
      {
        "name": "POSTGRES_DB",
        "value": "${database_name}"
      },
      {
        "name": "POSTGRES_SERVER",
        "value": "${database_address}"
      },
      {
        "name": "POSTGRES_PORT",
        "value": "5432"
      },
      {
        "name": "REDIS_HOST",
        "value": "redis"
      },
      {
        "name": "REDIS_PORT",
        "value": "6379"
      },
      {
        "name": "JWT_SECRET_KEY",
        "value": "mysecretkey"
      },
      {
        "name": "JWT_ALGORITHM",
        "value": "HS256"
      },
      {
        "name": "MAIL_USERNAME",
        "value": "dajavshna9@gmail.com"
      },
      {
        "name": "MAIL_PASSWORD",
        "value": "rrte dnkk wkef wocv"
      },
      {
        "name": "MAIL_FROM",
        "value": "dajavshna9@gmail.com"
      },
      {
        "name": "MAIL_FROM_NAME",
        "value": "dajavshna9@gmail.com"
      },
      {
        "name": "MAIL_SERVER",
        "value": "smtp.gmail.com"
      },
      {
        "name": "MAIL_PORT",
        "value": "465"
      }
    ],
    "secrets": [{
      "name": "POSTGRES_PASSWORD",
      "valueFrom": "${postgres_password}"
    }],
    "ulimits": [
      {
        "name": "nofile",
        "softLimit": 65536,
        "hardLimit": 65536
      }
    ],
    "mountPoints": [],
    "memory": 2048,
    "volumesFrom": []
  },
  {
    "name": "redis",
    "image": "${redis_ecr_repository}:7-alpine",
    "essential": false,
    "portMappings": [
      {
        "containerPort": 6379,
        "hostPort": 6379,
        "protocol": "tcp"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "${aws_cloudwatch_log_group_name}-redis",
        "awslogs-group": "${aws_cloudwatch_log_group_name}"
      }
    },
    "memory": 256,
    "cpu": 0
  }
]