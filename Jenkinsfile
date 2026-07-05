pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasanthapandiyan/myapp"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/vasanthapandiyanrfitaacademy-ux/project_tasks.git'
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

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                    echo "Stopping existing containers..."
                    docker compose down || true

                    echo "Removing old application image (optional)..."
                    docker rmi ${IMAGE_NAME}:latest || true

                    echo "Pulling latest image..."
                    docker pull ${IMAGE_NAME}:latest || true

                    echo "Starting all services..."
                    docker compose up -d --build

                    echo "Running containers:"
                    docker ps
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Docker Compose deployment completed.'
        }

        failure {
            echo 'FAILURE: Pipeline failed.'
        }

        always {
            sh 'docker logout || true'
        }
    }
}