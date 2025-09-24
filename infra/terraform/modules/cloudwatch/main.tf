variable "log_group_name" {}

resource "aws_cloudwatch_log_group" "this" {
  name              = var.log_group_name
  retention_in_days = 14
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.this.name
}
