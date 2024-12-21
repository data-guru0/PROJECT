pipeline {
    agent any

    environment {
        VENV_DIR = 'venv' // Directory for the virtual environment
        DOCKERHUB_CREDENTIAL_ID = 'mlops-project'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'dataguru97/mlops-project'
    }

    stages {
        stage('Github Repo Cloning') {
            steps {
                script {
                    echo 'Cloning Github Repository'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops', url: 'https://github.com/data-guru0/PROJECT.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setting up virtual environment'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Linting Code') {
            steps {
                script {
                    echo 'Linting Python Code...'
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate
                        pylint application.py main.py --output=pylint-report.txt --exit-zero || echo "Pylint completed with issues."
                        flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || echo "Flake8 completed with issues."
                        black application.py main.py || echo "Black formatting completed."
                    '''
                }
            }
        }

        stage('Trivy FS Scan') {
            steps {
                // Trivy Filesystem Scan
                script {
                    echo 'Scannning Filesystem with Trivy...'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }  

        stage('Build Docker image') {
            steps {
                // Trivy Filesystem Scan
                script {
                    echo 'Build Docker image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest") 
                }
            }
        }

        stage('Trivy Docker Image Scan') {
            steps {
                // Trivy Docker Image Scan
                script {
                    echo 'Scanning Docker Image with Trivy...'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-report.html"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                // Push Docker Image to DockerHub
                script {
                    echo 'Pushing Docker Image to DockerHub...'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}"){
                        dockerImage.push('latest')
                    }
                }
            }
        }     
    }
}
