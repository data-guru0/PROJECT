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
                        # Create a virtual environment
                        python -m venv ${VENV_DIR}
                        
                        # Activate the virtual environment
                        source ${VENV_DIR}/bin/activate

                        # Upgrade pip in the virtual environment
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
                        # Activate the virtual environment
                        source ${VENV_DIR}/bin/activate
                        
                        # Install required packages
                        pip install -e .
                        pip install dvc
                    '''
                }
            }
        }

        stage('Training Pipeline') {
            steps {
                script {
                    echo 'Running training pipeline in virtual environment'
                    sh '''
                        # Activate the virtual environment
                        source ${VENV_DIR}/bin/activate
                        
                        # Run DVC commands
                        dvc repro
                    '''
                }
            }
        }
    }
}
