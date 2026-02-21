pipeline {
    agent any

    environment {
        // Your Docker Hub image name
        IMAGE = "sankettambe/jarvis-ai"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls the latest code from your GitHub
                git branch: 'main', 
                    url: 'https://github.com/SanketTambe2/jarvis-ai.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Builds the local image from your Dockerfile
                sh 'docker build -t $IMAGE:latest .'
            }
        }

        stage('Sideload to Minikube') {
            steps {
                // IMPORTANT: This pushes the image directly into Minikube's 
                // internal registry so it doesn't get stuck "Pulling"
                sh 'minikube image load $IMAGE:latest'
            }
        }

        stage('Login & Push to DockerHub') {
            steps {
                // Backup push to Docker Hub
                withCredentials([usernamePassword(credentialsId: 'dockerhub', 
                                 usernameVariable: 'USER', 
                                 passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $IMAGE:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                # Apply your YAML configurations
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                
                # Force Kubernetes to restart the pods with the NEW image
                kubectl rollout restart deployment jarvis
                '''
            }
        }
    }

    post {
        success {
            script {
                echo "------------------------------------------------------------"
                echo "SUCCESS: Jarvis AI is deployed!"
                echo "1. Ensure your port-forward is running: kubectl port-forward svc/jarvis-service 8000:80"
                echo "2. Open your index.html and start chatting!"
                echo "------------------------------------------------------------"
            }
        }
        failure {
            echo "Deployment failed. Check Jenkins console logs for errors."
        }
    }
}
