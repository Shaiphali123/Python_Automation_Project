pipeline {
    agent any

    environment {
        GIT_URL = 'https://github.com/Shaiphali123/Python_Automation_Project.git'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull code from Git
                git branch: 'main', url: "${GIT_URL}"
            }
        }
        stage('Install Dependencies') {
            steps {
                // Install dependencies
                bat ' C:\Users\91912\AppData\Local\Programs\Python\Python312\Scripts\pip.exe install -r requirements.txt'
            }
        }
        stage('Run Unit Tests') {
            steps {
                // Run unit tests and generate coverage reports
                bat 'pytest --cov=app --cov-report=term'
            }
        }
    }
}
