pipeline {
    agent any

    environment {
        IMAGE_NAME = 'jenkins-hello-world'
        CONTAINER_NAME = 'jenkins-hello-world'

        VM_IP = '192.168.18.145'
        VM_USER = 'lucas'

        // ID de la credencial SSH que creaste en Jenkins
        SSH_CREDS = 'ssh-ubuntu'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Save Docker Image') {
            steps {
                sh '''
                    docker save ${IMAGE_NAME}:latest -o ${IMAGE_NAME}.tar
                '''
            }
        }

        stage('Copy Image to Ubuntu') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: "${SSH_CREDS}",
                        keyFileVariable: 'SSH_KEY'
                    )
                ]) {
                    sh '''
                        scp \
                          -i "$SSH_KEY" \
                          -o StrictHostKeyChecking=no \
                          ${IMAGE_NAME}.tar \
                          ${VM_USER}@${VM_IP}:/tmp/${IMAGE_NAME}.tar
                    '''
                }
            }
        }

        stage('Deploy on Ubuntu') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: "${SSH_CREDS}",
                        keyFileVariable: 'SSH_KEY'
                    )
                ]) {
                    sh '''
                        ssh \
                          -i "$SSH_KEY" \
                          -o StrictHostKeyChecking=no \
                          ${VM_USER}@${VM_IP} "

                            docker stop ${CONTAINER_NAME} || true
                            docker rm ${CONTAINER_NAME} || true

                            docker load -i /tmp/${IMAGE_NAME}.tar

                            docker run -d \
                              --name ${CONTAINER_NAME} \
                              --restart unless-stopped \
                              -p 8080:5000 \
                              ${IMAGE_NAME}:latest

                            rm -f /tmp/${IMAGE_NAME}.tar
                        "
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''
                rm -f ${IMAGE_NAME}.tar
            '''
        }

        success {
            echo 'Deploy realizado correctamente.'
        }

        failure {
            echo 'El pipeline fallo.'
        }
    }
}