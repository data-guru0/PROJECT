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
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                    '''
                }
            }
        }

        stage('Installing Packages') {
            steps {
                script {
                    echo 'Installing packages in virtual environment'
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pip install -e .
                    '''
                }
            }
        }

        stage('Training Pipeline') {
            steps {
                script {
                    echo 'Running training pipeline in virtual environment'
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        python main.py
                    '''
                }
            }
        }

        stage('App running') {
            steps {
                script {
                    echo 'Running training pipeline in virtual environment'
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        python application.py
                    '''
                }
            }
        }
    }
}
