pipeline {
    agent any

    environment {
        IMAGE_NAME = "payment-api"
        GITOPS_REPO = "git@github.com:Ivandjoko/payment-api-gitops.git"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "kind load docker-image ${IMAGE_NAME}:${IMAGE_TAG} --name sbdp-lab"
            }
        }

        stage('Update GitOps Repo') {
            steps {
                sh """
                    rm -rf gitops-repo
                    git clone ${GITOPS_REPO} gitops-repo
                    cd gitops-repo/base
                    sed -i 's|image: .*|image: ${IMAGE_NAME}:${IMAGE_TAG}|' payment-api-deployment.yaml
                    git config user.email "jenkins@sbdp-lab.local"
                    git config user.name "Jenkins CI"
                    git add payment-api-deployment.yaml
                    git commit -m "Update image to ${IMAGE_TAG}" || echo "Rien à committer"
                    git push origin main
                """
            }
        }
    }
}
