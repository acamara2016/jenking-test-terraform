# Define the variable
variable "environment" {}
variable "image_tag" {}

# Output the value of the TF_VAR_branch_name variable
output "output_branch_name" {
  value = var.environment
}

output "output_image_tag" {
  value = var.image_tag
}
