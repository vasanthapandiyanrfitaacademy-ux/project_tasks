pipeline {
agent any

```
stages {

    stage('Git Checkout') {
        steps {
            git 'https://github.com/user/myapp.git'
        }
    }

    stage('Build Docker Image') {
        steps {
            sh 'docker build -t myapp:${BUILD_NUMBER} .'
        }
    }

    stage('Push Image') {
        steps {
            sh '''
            docker tag myapp:${BUILD_NUMBER} dockerhubuser/myapp:${BUILD_NUMBER}
            docker push dockerhubuser/myapp:${BUILD_NUMBER}
            '''
        }
    }

    stage('Deploy') {
        steps {
            sh '''
            ssh ubuntu@server "
            docker pull dockerhubuser/myapp:${BUILD_NUMBER}
            docker stop myapp || true
            docker rm myapp || true
            docker run -d --name myapp -p 80:5000 dockerhubuser/myapp:${BUILD_NUMBER}
            "
            '''
        }
    }
}
```

}
