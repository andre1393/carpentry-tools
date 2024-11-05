resource "aws_lambda_function" "carpentry_tools_lambda" {
  function_name = "carpentry-tools-lambda"
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.carpentry_tools.repository_url}:latest"
  role          = aws_iam_role.lambda_execution_role.arn
  memory_size   = 128
  timeout       = 30
  environment {
    variables = {
      GOOGLE_SERVICE_ACCOUNT_FILE = var.google_service_account_file
      LOG_LEVEL                   = var.log_level
    }
  }
  lifecycle {
    ignore_changes = [image_uri]
  }
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
