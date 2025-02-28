terraform {
  required_version = ">= 1.3.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.27"
    }
  }
  backend "s3" {
    bucket = "projects"
    key    = "api_endpoints/application/generator/terraform"
    region = "{{ cookiecutter.region_name }}"
  }
}
provider "aws" {
  region = "{{ cookiecutter.region_name }}"
}

module "application_module" {
    source = "../../modules/{{ cookiecutter.application_name  }}"

    # ---- Networking
    default_vpc = ""
    default_subnet = ""
    subnets = [
        "",
        ""
    ]
    public_subnets = [
        "",
        ""
    ]

    # --- AWS-related
    region_name = "{{ cookiecutter.region_name }}"
    aws_account_id = "{{ cookiecutter.aws_account_id }}"

    # --- Environment-related
    account = "prod"
    env_name = "prod"

    # ----- Hosting-related
    certificate_arn = "arn:aws:acm:us-west-2:{{ cookiecutter.aws_account_id }}:certificate/1234567890-1234-1234-1234-123456789012"
    route53_zone_id = ""
    subdomain_name = "{{ cookiecutter.application_name }}"

    # Memory and CPU settings
    cpu = 1024
    memory = 3072
    disk_storage = 100

    # Secrets
    huggingface_secret_name = ""
}

