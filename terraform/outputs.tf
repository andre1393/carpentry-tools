output "ecr_repository_url" {
  value = module.ecr.repository_url
}

output "api_invoke_url" {
  value = aws_apigatewayv2_stage.default_stage.invoke_url
}

output "lambda_function_name" {
  value = aws_lambda_function.carpentry_tools_lambda.function_name
}
