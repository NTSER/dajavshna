provider "aws" {
  region  = "us-east-1"
  profile = "NTSER"
}

terraform {
  backend "s3" {
    profile      = "NTSER"
    bucket       = "dajavshnabucket"
    key          = "terraform.tfstate"
    encrypt      = true
    region       = "us-east-1"
    use_lockfile = true
  }
}

data "aws_caller_identity" "current" {}
