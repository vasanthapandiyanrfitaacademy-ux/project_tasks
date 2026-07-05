pipeline {
agent any

```
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

    stage('Build Image') {
        steps {
            sh '''
                docker build -t ${IMAGE_NAME}:latest .
            '''
        }
    }

    stage('Push Image') {
        steps {
            sh '''
                docker push ${IMAGE_NAME}:latest
            '''
        }
    }

    stage('Deploy') {
        steps {
            sh '''
                cd $WORKSPACE

                echo "FILES:"
                ls -l

                echo "Stopping old container..."
                docker rm -f myapp_container || true

                echo "Pull latest image..."
                docker pull ${IMAGE_NAME}:latest

                echo "Running container..."
                docker run -d \
                  --name myapp_container \
                  -p 8501:8501 \
                  -p 8000:8000 \
                  ${IMAGE_NAME}:latest

                echo "Deployment DONE"
            '''
        }
    }
}

post {
    success {
        echo '✅ SUCCESS'
    }
    failure {
        echo '❌ FAILED'
    }
}
```

}
