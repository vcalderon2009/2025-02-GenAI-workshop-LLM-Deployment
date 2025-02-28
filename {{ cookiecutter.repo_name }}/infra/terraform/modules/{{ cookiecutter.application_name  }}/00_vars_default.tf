/* ----------------------------------------------------------------------------
 * Name: 00_vars_default.tf
 *
 * Description: Default variables which are not environment-specific
 * --------------------------------------------------------------------------*/

 variable "application" {
    type = string
  default     = "{{ cookiecutter.application_name }}"
  description = "The application name (used for tagging, etc.)"
}

variable "region_name" {
    type = string
    default = "{{ cookiecutter.aws_region }}"
}

/* -------------------------- Networking ----------------------------------- */

variable "default_vpc" {
  type        = string
  description = "Default VPC ID."
}

variable "default_subnet" {
  type        = string
  description = "Default subnet ID"
}

variable "subnets" {
  type        = list(string)
  description = "List of subnet IDs for running Fargate tasks."
}

variable "public_subnets" {
  type        = list(string)
  description = "List of public subnet IDs for running Fargate tasks."
}

/* ---------------------- Environment variables ---------------------------- */

variable "account" {
  type        = string
  description = "The AWS account, to which the infrastructure is deployed."
}

variable "aws_account_id" {
  type        = string
  description = "The AWS account, to which the infrastructure is deployed."
}

variable "env_name" {
  type        = string
  description = "Name of the environment."
}

variable "env_id" {
  type        = string
  default     = "01"
  description = "Environment ID"
}

locals {
  env = "${var.env_name}-${var.env_id}"

  tags = {
    application = var.application
    environment = local.env
  }

  application_suffix = "${var.application}-${local.env}"
}

variable "cpu" {
  type        = number
  description = "Number of CPU units used by the task."
  default     = 256
}

variable "memory" {
  type        = number
  description = "Amount (in MiB) of memory used by the task."
  default     = 1024
}

variable "disk_storage" {
  type        = number
  description = "Amount (in GiB) of disk storage to use by the task."
  default     = 100
}

variable "logs_stream_prefix" {
  type        = string
  description = "Prefix to use when submitting logs to CloudWatch"
  default     = "{{ cookiecutter.application_name }}"
}

variable "huggingface_secret_name" {
  type = string
  description = "Name of AWS secret that contains the HF credentials"
}

/* ----------------------------- Route 53 ------------------------------------- */
variable "certificate_arn" {
  type        = string
  description = "arn value for the AWS HTTPS certificate"
}

variable "route53_zone_id" {
  type        = string
  description = "Hosted zone id of Route 53 registered domain"
}

variable "subdomain_name" {
  type        = string
  description = "subdomain to add to the HTTPS endpoint"
}
