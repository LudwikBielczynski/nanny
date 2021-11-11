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
                sh 'ls -la'
                sh 'ls -la /'
                sh 'echo $USER'

                // Install all python dependencies
                sh 'pip install --no-cache-dir -r requirements.txt --user'
                sh 'pip install --no-cache-dir -r requirements/dev.txt --user'

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