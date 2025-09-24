variable "function_name" { type = string }
variable "image_uri"     { type = string }
variable "role_arn"      { type = string }
variable "env_vars" {
  type    = map(string)
  default = {}
}
