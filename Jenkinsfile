pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'your-aws-region'
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
    post {
        always {
            cleanWs()
        }
    }
}  
