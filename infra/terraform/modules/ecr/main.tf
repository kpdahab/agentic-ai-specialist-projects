variable "repo_name" {}

resource "aws_ecr_repository" "this" {
  name                 = var.repo_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "repo_url" {
  value = aws_ecr_repository.this.repository_url
}
