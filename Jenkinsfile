pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                dockerfile true
                // docker {
                //     // image 'python:3.7'

                // }
            }
            steps {
                sh 'cat /etc/os-release'
                // sh 'apt-get install sudo'
                // Install system level dependencies for pyaudio
                // sh 'sudo apt-get update && sudo apt-get install python-all-dev portaudio19-dev'

                // Install all python dependencies
                sh 'pip install --no-cache-dir -r requirements.txt --user'
                sh 'pip install --no-cache-dir -r requirements/dev.txt --user'

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