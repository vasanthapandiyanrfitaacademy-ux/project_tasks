pipeline {
agent any

```
environment {
    IMAGE_NAME = "vasanthapandiyan/myapp"
    CONTAINER_NAME = "myapp"
}

stages {

    stage('Checkout Code') {
        steps {
            git 'https://github.com/vasanthapandiyanrfitaacademy-ux/project_tasks.git'
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
            docker build -t $IMAGE_NAME:${BUILD_NUMBER} .
            '''
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
                echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                '''
            }
        }
    }

    stage('Push Image to Docker Hub') {
        steps {
            sh '''
            docker tag $IMAGE_NAME:${BUILD_NUMBER} $IMAGE_NAME:latest
            docker push $IMAGE_NAME:${BUILD_NUMBER}
            docker push $IMAGE_NAME:latest
            '''
        }
    }

    stage('Deploy Locally') {
        steps {
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true

            docker run -d \
            --name $CONTAINER_NAME \
            -p 8501:8501 \
            $IMAGE_NAME:${BUILD_NUMBER}
            '''
        }
    }
}
```

}
