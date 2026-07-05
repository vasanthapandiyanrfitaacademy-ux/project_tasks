pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasanthapandiyan/myapp"
    }

    stages {

       stage('Checkout Code') {
            steps {
              deleteDir()   // 🔥 IMPORTANT: clears old workspace

              git branch: 'main',
            url: 'https://github.com/vasanthapandiyanrfitaacademy-ux/project_tasks.git'
           }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
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
                    echo "Fixing old containers..."

                    docker compose down || true
                    docker container prune -f

                    echo "Pulling latest images..."
                    docker compose pull

                    echo "Starting full stack..."
                    docker compose up -d

                    echo "Containers status:"
                    docker ps
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS  FULL CI/CD WORKING"
        }

        failure {
            echo "FAILED  Check logs"
        }

        always {
            sh 'docker logout || true'
        }
    }
}