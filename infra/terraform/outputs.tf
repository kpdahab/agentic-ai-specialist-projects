output "account_id" {
  value       = data.aws_caller_identity.current.account_id
  description = "AWS account ID"
}

output "ecr_repo_url" {
  value       = module.ecr.repo_url
  description = "ECR repository URL"
}

output "lambda_name" {
  value       = module.lambda.lambda_name
}

output "api_url" {
  value       = module.apigateway.api_endpoint
}

output "dynamodb_table" {
  value       = module.dynamodb.table_name
}
