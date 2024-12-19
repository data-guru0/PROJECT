pipeline {
    agent any
    
    stages {
        stage('Github Repo Cloning') {
            steps {
                // Clone Github repository
                script {
                    echo 'Cloning Github Repository'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops', url: 'https://github.com/data-guru0/PROJECT.git']])
                }
            }
        }
    }
}
