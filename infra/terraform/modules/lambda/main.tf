variable "function_name" {}
variable "image_uri" {}
variable "role_arn" {}
variable "env_vars" {
  type    = map(string)
  default = {}
}

resource "aws_lambda_function" "this" {
  function_name = var.function_name
  package_type  = "Image"
  image_uri     = var.image_uri
  role          = var.role_arn
  memory_size   = 1024
  timeout       = 30

  environment {
    variables = var.env_vars
  }
}

output "lambda_name" {
  value = aws_lambda_function.this.function_name
}

output "lambda_arn" {
  value = aws_lambda_function.this.arn
}
