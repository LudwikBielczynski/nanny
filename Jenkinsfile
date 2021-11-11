pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.7'
                    // image 'qnib/pytest'
                }
            }
            steps {
                // Install system level dependencies for pyaudio
                sh 'sudo apt-get update && sudo apt-get install python-all-dev portaudio19-dev'

                // Install all python dependencies
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements/dev.txt'

                sh 'echo trial'
                sh 'ls -la'
                // Run tests
                sh 'python pytest --junit-xml test-reports/results.xml'
                // sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') {
            steps {
                sh 'echo not implemented'
            }
        }
    }
}