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

        stage('SAST - Semgrep') {
            steps {
                sh '''
                    docker run --rm \
                      --volumes-from jenkins \
                      -w "$PWD" \
                      semgrep/semgrep \
                      semgrep scan --config p/python --config p/owasp-top-ten \
                      --metrics=off --error .
                '''
            }
        }  
        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
                sh "docker build --pull -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('SCA - Trivy') {
            steps {
                sh '''
                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      -v trivy-cache:/root/.cache/ \
                      aquasec/trivy image \
                      --severity HIGH,CRITICAL --ignore-unfixed --no-progress --exit-code 1 \
                      $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh "kind load docker-image ${IMAGE_NAME}:${IMAGE_TAG} --name sbdp-lab"
            }
        }
        stage('Update GitOps Repo') {
            steps {
                sshagent(credentials: ['gitops-ssh-key']) {
                    sh """
                        mkdir -p ~/.ssh
                        ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null
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
}
