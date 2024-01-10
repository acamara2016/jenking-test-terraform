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
        stage('Storing parameters for terraform') {
            steps {
                script {
                    sh "export TF_VAR_branch_name=${branch_name}; export TF_VAR_image_tag=${image_tag}"
                }
            }
        }
        stage('Testing parameters') {
            steps {
                script {
                    sh "echo ${branch_name} ${image_tag}"
                }
            }
        }
        stage('Terraform Init') {
            steps {
                script {
                    sh 'terraform init'
                }
            }
        }
        stage('Terraform Plan') {
            steps {
                script {
                   sh "terraform plan -var='branch_name=${branch_name}' -var='image_tag=${image_tag}'"
                }
            }
        }
        stage('Terraform Apply') {
            steps {
                script {
                    sh "terraform apply -auto-approve -var='branch_name=${branch_name}' -var='image_tag=${image_tag}'"
                }
            }
        }
    }
}

