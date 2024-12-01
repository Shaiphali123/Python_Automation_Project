pipeline {
    agent any

    environment {
        GIT_URL = 'https://github.com/Shaiphali123/Python_Automation_Project.git'  // Replace with your Git repository URL
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull code from Git
                git branch: 'main'
            }
        }
        stage('Install Dependencies') {
            steps {
                // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Unit Tests') {
            steps {
                // Run unit tests and generate coverage reports
                sh 'pytest --cov=app --cov-report=term tests/'
            }
        }
    }
}
