pipeline {
    agent any
    tools {
      terraform 'terraform'
      git 'jgit'
    }
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
    }
    stages {
        stage('Checkout Code') {
            steps {
                echo 'checkout branch'
            }
        }
        stage('Terraform Init') {
            steps {
                script {
                    echo 'terraform init'
                }
            }
        }
        stage('Terraform Plan') {
            steps {
                script {
                    echo 'terraform init'
                }
            }
        }
        stage('Terraform Apply') {
            steps {
                script {
                    echo 'terraform apply -auto-approve tfplan'
                }
            }
        }
    }
}
