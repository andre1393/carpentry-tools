variable "aws_region" {
  default     = "us-east-1"
  description = "region where the assets will be created in"
}

variable "google_service_account_file" {
  default     = "/var/task/carpentry-tools-440018-233a8c3c2ecd.json"
  description = "path to google service account credentials file"
}

variable "log_level" {
  default     = "INFO"
  description = "application log level"
}

variable "image_tag" {
  default     = "latest"
  description = "image tag"
}