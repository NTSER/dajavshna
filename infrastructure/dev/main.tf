
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "< 6.0"
    }
  }
}

module "dev" {
  source      = "../../modules"
  environment = "dev"
  app_name    = "dajavshna"

}
