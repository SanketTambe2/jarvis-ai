pipeline {
  agent any

  environment {
    IMAGE = "sankettambe/jarvis-ai"
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: 'main',
        url: 'https://github.com/SanketTambe2/jarvis-ai.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE:latest .'
      }
    }

    stage('Login DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
        usernameVariable: 'USER',
        passwordVariable: 'PASS')]) {

          sh 'echo $PASS | docker login -u $USER --password-stdin'
        }
      }
    }

    stage('Push Image') {
      steps {
        sh 'docker push $IMAGE:latest'
      }
    }

    stage('Deploy Kubernetes') {
      steps {
        sh '''
        kubectl apply -f k8s/deployment.yaml
        kubectl apply -f k8s/service.yaml
        '''
      }
    }
  }

  post {
    success {
      echo "Jarvis AI deployed successfully"
    }
  }
}

