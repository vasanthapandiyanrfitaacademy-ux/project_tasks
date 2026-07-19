pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasanthapandiyan/myapp"
    }

    stages {

        stage('Checkout Code') {
            steps {
                deleteDir()
                git branch: 'main',
                    url: 'https://github.com/vasanthapandiyanrfitaacademy-ux/project_tasks.git'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-creds',
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {
                    sh '''
                        echo "$PASS" | docker login -u "$USER" --password-stdin
                    '''
                }
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Push Image') {
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
                    echo "Stopping old containers..."
                    docker compose down --remove-orphans || true

                    echo "Removing unused containers..."
                    docker container prune -f

                    echo "Removing old unused images..."
                    docker image prune -a -f

                    echo "Pull latest image..."
                    docker pull ${IMAGE_NAME}:latest

                    echo "Starting new containers..."
                    docker compose up -d --force-recreate

                    echo "Cleaning dangling images..."
                    docker image prune -f

                    echo "Running containers:"
                    docker ps

                    echo "Available images:"
                    docker images
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS - Full CI/CD Working"
        }

        failure {
            echo "FAILED - Check Logs"
        }

        always {
            sh 'docker logout || true'
        }
    }
}