pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.8-alpine'
                    // image 'qnib/pytest'
                }
            }
            steps {
                sh 'echo trial'
                sh 'ls -la'
                // sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
                // sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                // sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                // stash(name: 'compiled-results', includes: 'sources/*.py*')
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