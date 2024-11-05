terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  backend "s3" {
    region = "us-east-1"
    key    = "terraform/terraform.tfstate"
    bucket = "carpentry-tools"
  }
}

provider "aws" {
  region = var.aws_region
}


resource "aws_ecr_repository" "carpentry_tools" {
  name                 = "carpentry-tools"
  image_tag_mutability = "MUTABLE" # Set repository to allow mutable tags
  force_delete         = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

output "repository_url" {
  value = aws_ecr_repository.carpentry_tools.repository_url
}