resource "null_resource" "print_message" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "echo 'Hello, this Terraform script does not create anything.'"
  }
}
