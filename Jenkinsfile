pipeline {
    agent any

    environment {
        // Replace with your Docker Hub username and repository name
        DOCKER_IMAGE = "your_dockerhub_username/flask-api"
        
        // This is the ID of the credentials you will create in Jenkins for Docker Hub
        DOCKER_CREDENTIALS_ID = "dockerhub-creds"
        
        // The SSH connection string for your second EC2 instance (App Server)
        // e.g., ubuntu@1.2.3.4 or ec2-user@1.2.3.4
        APP_SERVER_IP = "ec2-user@<YOUR_EC2_APP_SERVER_IP>"
        
        // This is the ID of the credentials you will create in Jenkins for the App Server SSH Key
        SSH_CREDENTIALS_ID = "app-server-ssh-key"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image..."
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Image to Docker Hub..."
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to App Server (EC2)') {
            steps {
                echo "Deploying to App Server..."
                sshagent([SSH_CREDENTIALS_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${APP_SERVER_IP} '
                        # Pull the latest image
                        docker pull ${DOCKER_IMAGE}:${env.BUILD_ID}
                        
                        # Stop and remove the existing container if it exists
                        docker stop flask-api || true
                        docker rm flask-api || true
                        
                        # Run the new container
                        docker run -d -p 80:5000 --name flask-api ${DOCKER_IMAGE}:${env.BUILD_ID}
                    '
                    """
                }
            }
        }
    }
}
