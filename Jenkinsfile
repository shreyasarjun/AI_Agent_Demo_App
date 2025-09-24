pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'shreyasarjun/ai-agent-demo777'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        GIT_REPO = 'https://github.com/shreyasarjun/AI_Agent_Demo_App.git'
        GIT_BRANCH = 'main'
        PATH = "/opt/homebrew/bin:$PATH"
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Clean workspace before cloning
                cleanWs()
                echo 'Cloning repository...'
                git branch: env.GIT_BRANCH, url: env.GIT_REPO
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        echo 'Building Docker image...'
                        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                    } catch (Exception e) {
                        error "Failed to build Docker image: ${e.message}"
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    try {
                        echo 'Pushing to Docker Hub...'
                        withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                            sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                            sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                            sh "docker push ${DOCKER_IMAGE}:latest"
                        }
                    } catch (Exception e) {
                        error "Failed to push Docker image: ${e.message}"
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    try {
                        echo 'Deploying to Kubernetes...'
                            // Update deployment image
                            sh """
                                sed -i '' 's|image: shreyasarjun/ai-agent-demo777:.*|image: shreyasarjun/ai-agent-demo777:${DOCKER_TAG}|' k8s/deployment.yaml
                            
                                # Apply Kubernetes configurations
                                kubectl apply -f k8s/deployment.yaml
                                kubectl apply -f k8s/service.yaml
                            
                                # Wait for deployment to complete
                                kubectl rollout status deployment/ai-agent-demo -n default --timeout=300s
                            """
                    } catch (Exception e) {
                        error "Failed to deploy to Kubernetes: ${e.message}"
                    }
                }
            }
        }

            // stage('Sanity Testing') {
            //     steps {
            //         script {
            //             try {
            //                 echo 'Running sanity tests...'
            //                     // ...existing code...
            //                 // Get service URL from Minikube
            //                 def serviceUrl = sh(script: "minikube service ai-agent-cicd-service --url", returnStdout: true).trim()
            //                 echo "Service URL: ${serviceUrl}"
            //                 // Print only the IP part
            //                 def ip = serviceUrl.replaceAll(/http?:\/\/(.*):\d+/, '$1')
            //                 echo "Service IP: ${ip}"
            //             } catch (Exception e) {
            //                 error "Sanity tests failed: ${e.message}"
            //             }
            //         }
            //     }
            // }
        
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Please check the logs for details.'
        }
        always {
            // Clean up Docker images
            script {
                try {
                    sh """
                        docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker rmi ${DOCKER_IMAGE}:latest
                    """
                } catch (Exception e) {
                    echo "Warning: Cleanup of Docker images failed: ${e.message}"
                }
            }
            // Clean workspace
            cleanWs()
        }
    }
}