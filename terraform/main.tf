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

resource "aws_ecr_lifecycle_policy" "carpentry_tools" {
  repository = aws_ecr_repository.carpentry_tools.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Keep last 2 images",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 2
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

output "repository_url" {
  value = aws_ecr_repository.carpentry_tools.repository_url
}