# Define the variable
variable "branch_name" {}

# Output the value of the TF_VAR_branch_name variable
output "output_branch_name" {
  value = var.branch_name
}
