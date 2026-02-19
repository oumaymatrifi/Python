pipeline {
    agent any 

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/oumaymatrifi/Python.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest httpx==0.27.2
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }
    }
}
