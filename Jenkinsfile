pipeline {
    agent any
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
                echo 'terraform init'
            }
        }
        stage('Terraform Plan') {
            steps {
                echo 'terraform plan'
            }
        }
        stage('Terraform Apply') {
            steps {
                echo 'terraform apply -auto-approve tfplan'
            }
        }
    }
}  
