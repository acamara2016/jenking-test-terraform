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
