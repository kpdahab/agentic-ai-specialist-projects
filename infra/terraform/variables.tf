variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "llm_provider" {
  description = "Which LLM provider the Lambda should use (openai, anthropic, etc.)"
  type        = string
  default     = "openai"
}

variable "openai_api_key" {
  description = "Initial OpenAI API key (stored in Secrets Manager)"
  type        = string
  sensitive   = true
}

variable "anthropic_api_key" {
  description = "Initial Anthropic API key (stored in Secrets Manager)"
  type        = string
  sensitive   = true
}
