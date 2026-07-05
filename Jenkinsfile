pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasanthapandiyan/myapp"
        CONTAINER_NAME = "myapp_container"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git(
                    branch: 'main',
                    url: 'https://github.com/vasanthapandiyanrfitaacademy-ux/project_tasks.git'
                )
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    echo "Stopping existing container..."
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    echo "Pulling latest image..."
                    docker pull ${IMAGE_NAME}:latest

                    echo "Starting new container..."
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 8501:8501 \
                        -p 8000:8000 \
                        --restart always \
                        ${IMAGE_NAME}:latest

                    echo "Deployment completed successfully."
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS: Application deployed successfully."
        }

        failure {
            echo "FAILURE: Pipeline execution failed."
        }

        always {
            echo "Pipeline execution finished."
        }
    }
}