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
        stage('Terraform Init') {
            steps {
                script {
                    'terraform init'
                }
            }
        }
        stage('Terraform Plan') {
            steps {
                script {
                    'terraform plan'
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
