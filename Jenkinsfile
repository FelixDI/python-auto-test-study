pipeline {
    agent any
    environment {
        API_BASE_URL = 'http://api:8000'
        MYSQL_HOST = 'db'
        MYSQL_PASSWORD = 'root123'
    }
    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }
        stage('安装依赖') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python3 -m pip install -r requirements.txt
                '''
            }
        }
        stage('运行接口测试') {
            steps {
                sh '''
                . venv/bin/activate

                pytest src/stage2_api_test \
                    --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            )
        }
    }
}