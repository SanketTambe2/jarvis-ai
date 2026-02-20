pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh 'docker build -t jarvis-ai .'
      }
    }

    stage('Deploy') {
      steps {
        sh 'kubectl apply -f k8s/'
      }
    }
  }
}

