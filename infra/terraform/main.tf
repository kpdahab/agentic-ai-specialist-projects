########################################
# Account / Region
########################################
data "aws_caller_identity" "current" {}

locals {
  ecr_repo_name = "my-agentic-app"
}

########################################
# Modules
########################################

#--------------------------------------
# ecr
#--------------------------------------
module "ecr" {
  source = "./modules/ecr"
  repo_name = local.ecr_repo_name
}

#--------------------------------------
# iam
#--------------------------------------
module "iam" {
  source = "./modules/iam"
}

#--------------------------------------
# dynamodb
#--------------------------------------
module "dynamodb" {
  source     = "./modules/dynamodb"
  table_name = "agentic-app-sessions"
}

#--------------------------------------
# cloudwatch
#--------------------------------------
module "cloudwatch" {
  source         = "./modules/cloudwatch"
  log_group_name = "/aws/lambda/my-agentic-app"
}

#--------------------------------------
# lambda
#--------------------------------------
module "lambda" {
  source        = "./modules/lambda"
  function_name = "my-agentic-app"
  image_uri     = "${module.ecr.repo_url}:latest"
  role_arn      = module.iam.lambda_role_arn
  env_vars = {
    LLM_PROVIDER         = var.llm_provider
    OPENAI_SECRET_ARN    = module.iam.openai_secret_arn
    ANTHROPIC_SECRET_ARN = module.iam.anthropic_secret_arn
    DYNAMODB_TABLE       = module.dynamodb.table_name
  }
  depends_on = [module.ecr]
}

#--------------------------------------
# apigateway
#--------------------------------------
module "apigateway" {
  source      = "./modules/apigateway"
  lambda_arn  = module.lambda.lambda_arn
  lambda_name = module.lambda.lambda_name
}