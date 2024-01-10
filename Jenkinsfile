pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
    }
    stages {
        stage('Checkout Code') {
            steps {
                sh label: '', script: 'checkout main'
            }
        }
        stage('Terraform Init') {
            steps {
                script {
                    sh label: '', script: 'terraform init'
                }
            }
        }
        stage('Terraform Plan') {
            steps {
                script {
                    sh label: '', script: 'terraform plan'
                }
            }
        }
    }
}
