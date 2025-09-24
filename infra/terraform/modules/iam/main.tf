# Lambda execution role
resource "aws_iam_role" "lambda_exec" {
  name = "my-agentic-app-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# CloudWatch logging
resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Bedrock policy
resource "aws_iam_role_policy" "bedrock_access" {
  name = "lambda-bedrock-access"
  role = aws_iam_role.lambda_exec.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["bedrock:InvokeModel", "bedrock:Retrieve"]
      Resource = "*"
    }]
  })
}

# Secrets Manager policies
resource "aws_secretsmanager_secret" "openai" {
  name        = "OPENAI_API_KEY"
  description = "OpenAI API Key"
}
resource "aws_secretsmanager_secret_version" "openai_ver" {
  secret_id     = aws_secretsmanager_secret.openai.id
  secret_string = var.openai_api_key
}

resource "aws_secretsmanager_secret" "anthropic" {
  name        = "ANTHROPIC_API_KEY"
  description = "Anthropic API Key"
}
resource "aws_secretsmanager_secret_version" "anthropic_ver" {
  secret_id     = aws_secretsmanager_secret.anthropic.id
  secret_string = var.anthropic_api_key
}
