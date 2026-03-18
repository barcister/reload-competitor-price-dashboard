terraform {
  required_version = ">= 1.6.0"
}

provider "aws" {
  region = var.aws_region
}

# Terraform-lite placeholder:
# - ECS cluster
# - Fargate services: api, collector, web
# - RDS PostgreSQL
# - ElastiCache Redis
# - S3 bucket for snapshots

variable "aws_region" {
  type    = string
  default = "us-east-1"
}
