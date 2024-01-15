pipeline {
    agent any
    tools {
      terraform 'terraform'
      git 'jgit'
    }
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        TERRAFORM_STATE_FILE = "${WORKSPACE}/topaz-data-refresh/terraform.tfstate"
    }
    stages {
        stage('cd into topaz-data-refresh') {
            steps {
                script {
                    sh "cd topaz-data-refresh-service"
                }
            }
        }
        stage('Parameters') {
            steps {
                script {
                    sh "echo deploying topaz-data-refresh for environment: ${environment} and image_tag: ${image_tag}"
                }
            }
        }
        stage('Terraform Init') {
            steps {
                script {
                    sh "terraform init -backend-config=${TERRAFORM_STATE_FILE}"
                }
            }
        }
        stage('Terraform Plan') {
            steps {
                script {
                   sh "terraform plan -var='environment=${environment}' -var='image_tag=${image_tag}'"
                }
            }
        }
        stage('Terraform Apply') {
            steps {
                script {
                    sh "terraform apply -auto-approve -var='environment=${environment}' -var='image_tag=${image_tag}'"
                }
            }
        }
    }
}

