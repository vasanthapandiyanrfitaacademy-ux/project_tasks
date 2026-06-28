pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasanthapandiyan/myapp"
        CONTAINER_NAME = "myapp"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/vasanthapandiyanrfitaacademy-ux/project_tasks.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
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

        stage('Deploy Container') {
            steps {
                sh """
                    echo "Stopping old container..."
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    echo "Running new container..."
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 8501:8501 \
                        ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage('Cleanup Old Docker Resources') {
            steps {
                sh """
                    echo "Removing stopped containers..."
                    docker container prune -f

                    echo "Removing unused images..."
                    docker image prune -f

                    echo "Removing old images (keeping latest + current build)..."
                    docker images ${IMAGE_NAME} --format "{{.Repository}}:{{.Tag}} {{.ID}}" | \
                    grep -v "${BUILD_NUMBER}" | \
                    grep -v "latest" | \
                    awk '{print \$2}' | \
                    xargs -r docker rmi -f || true
                """
            }
        }
    }

    post {
        success {
            echo ' Pipeline completed successfully.'
        }
        failure {
            echo ' Pipeline failed.'
        }
    }
}