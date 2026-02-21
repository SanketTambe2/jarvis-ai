pipeline {
  agent any
  environment {
    IMAGE = "sankettambe/jarvis-ai"
  }
  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/SanketTambe2/jarvis-ai.git'
      }
    }
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE:latest .'
      }
    }
    stage('Login & Push') {
      steps {
        sh 'minikube image load $IMAGE:latest' 
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'echo $PASS | docker login -u $USER --password-stdin'
          sh 'docker push $IMAGE:latest'
        }
      }
    }
    stage('Deploy Kubernetes') {
      steps {
        sh '''
        kubectl apply -f k8s/deployment.yaml
        kubectl apply -f k8s/service.yaml
        kubectl rollout restart deployment jarvis
        '''
      }
    }
  }
  post {
    success {
      script {
        // This prints the link in your Jenkins console log so you can just click it
        echo "------------------------------------------------------------"
        echo "JARVIS IS LIVE!"
        echo "To open your app, run this in your terminal:"
        echo "minikube service jarvis-service"
        echo "OR use this local link after port-forwarding:"
        echo "http://localhost:8000"
        echo "------------------------------------------------------------"
      }
    }
  }
}
