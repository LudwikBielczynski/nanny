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
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements/dev.txt'
                sh 'echo trial'
                sh 'ls -la'
                sh 'python pytest --junit-xml test-reports/results.xml'
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