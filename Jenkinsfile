pipeline {
    agent any

    environment {
        IMAGE_NAME = "resume-analyzer"
        IMAGE_TAG  = "build-${BUILD_NUMBER}"
        VENV_DIR   = ".venv"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "Creating virtual environment and installing dependencies..."
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m spacy download en_core_web_sm
                '''
            }
        }

        stage('Lint & Format Check') {
            parallel {
                stage('flake8') {
                    steps {
                        echo "Running flake8..."
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            flake8 app/ tests/
                        '''
                    }
                }
                stage('pylint') {
                    steps {
                        echo "Running pylint..."
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            pylint app/ --fail-under=9.0
                        '''
                    }
                }
                stage('black') {
                    steps {
                        echo "Checking black formatting..."
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            black --check app/ tests/
                        '''
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running pytest unit tests..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest tests/ -v --tb=short --junitxml=reports/junit.xml
                '''
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -f docker/Dockerfile -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Docker Health Check') {
            steps {
                echo "Starting container and verifying health..."
                sh '''
                    docker run -d --name resume-test -p 8502:8501 ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 15
                    curl -f http://localhost:8502/_stcore/health || (docker logs resume-test && exit 1)
                    docker stop resume-test
                    docker rm resume-test
                '''
            }
        }

        stage('Selenium Tests') {
            steps {
                echo "Starting app for UI tests..."
                sh '''
                    docker run -d --name resume-selenium -p 8503:8501 ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 20
                    . ${VENV_DIR}/bin/activate
                    pytest selenium_tests/ -v --tb=short
                    docker stop resume-selenium
                    docker rm resume-selenium
                '''
            }
        }

    }

    post {
        success {
            echo "Pipeline passed! Image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed. Check the logs above."
            sh '''
                docker stop resume-test resume-selenium 2>/dev/null || true
                docker rm resume-test resume-selenium 2>/dev/null || true
            '''
        }
        always {
            echo "Cleaning up virtual environment..."
            sh "rm -rf ${VENV_DIR}"
        }
    }
}
