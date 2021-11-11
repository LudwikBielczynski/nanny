pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:3.8-alpine'
                }
            }
            steps {
                sh 'echo trial'
                // sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                // sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                // stash(name: 'compiled-results', includes: 'sources/*.py*')
            }
        }
    }
}