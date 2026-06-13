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
                    source venv/bin/activate
                    python3 -m pip install -r requirements.txt
                '''
            }
        }
        stage('运行接口测试') {
            steps {
                sh '''
                    source venv/bin/activate
                    mkdir -p reports
                    python3 -m pytest src/ecommerce_api_test/test_cases/ -v --html=reports/api_report.html --self-contained-html
                '''
            }
        }
    }
    post {
        always {
            publishHTML target: [
                reportDir: 'reports',
                reportFiles: 'api_report.html',
                reportName: '接口测试报告'
            ]
        }
    }
}