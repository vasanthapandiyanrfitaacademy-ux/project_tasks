pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasanthapandiyan/myapp"
        COMPOSE_FILE = "docker-compose.yml"
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
                withCredentials([usernamePassword(
                    credentialsId: 'docker-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
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

        stage('Deploy using Docker Compose') {
            steps {
                sh '''
                    echo "Stopping old containers..."
                    docker compose down || true

                    echo "Pull latest image..."
                    docker pull ${IMAGE_NAME}:latest

                    echo "Starting containers..."
                    docker compose up -d --build

                    echo "Deployment completed!"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ SUCCESS: Application deployed successfully!'
        }
        failure {
            echo '❌ FAILURE: Pipeline failed!'
        }
    }
}