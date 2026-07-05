pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasanthapandiyan/myapp"
        CONTAINER_NAME = "python_project"
    }

    stages {
        stage('Checkout code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/vasanthapandiyanrfitaacademy-ux/project_tasks.git'
            }
        }

        stage('Old Container Remove') {
            steps {
                sh """
                    echo "Removing old container"
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker container prune -f || true
                """
            }
        }

        stage('Old Images Remove') {
            steps {
                sh """
                    echo "Removing old images"
                    docker images ${IMAGE_NAME} -q | xargs -r docker rmi -f
                    docker image prune -af || true
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build --no-cache -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy a Container') {
            steps {
                sh """
                    echo "Running New Container...."
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 8501:8501 \
                        ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}