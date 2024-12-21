pipeline {
    agent any

    environment {
        VENV_DIR = 'venv' // Directory for the virtual environment
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
                        python3 -m venv ${VENV_DIR}
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
                        pylint application.py main.py --output=pylint-report.txt || echo "Pylint completed with issues."
                        flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || echo "Flake8 completed with issues."
                        black application.py main.py || echo "Black formatting completed."
                    '''
                }
            }
        }

        stage('Trivy FS Scan') {
            steps {
                script {
                    echo 'Scanning Filesystem with Trivy...'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html || echo 'Trivy scan completed with warnings.'"
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    try {
                        docker.build("mlops")
                    } catch (e) {
                        echo "Error during Docker build: ${e.getMessage()}"
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'Cleaning up workspace...'
                sh 'rm -rf ${VENV_DIR}'
            }
        }
        failure {
            echo 'Pipeline failed.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
    }
}
