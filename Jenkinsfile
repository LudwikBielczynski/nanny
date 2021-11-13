pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                dockerfile {
                        filename 'pytest.dockerfile'
                        dir 'dockerfiles'
                    }
            }
            steps {
                // Install all python dependencies
                sh 'pip install --no-cache-dir -r requirements.txt --user'
                sh 'pip install --no-cache-dir -r requirements/dev.txt --user'
                sh 'pip install -e "/home/workspace/nanny" --user'

                // Run tests

                sh 'PATH="$PATH:/.local/bin" && pytest --junit-xml test-reports/results.xml'
            }
            post {
                always { junit 'test-reports/results.xml' }
            }
            }
        stage('Deliver') {
            agent {
                docker { image 'ubuntu:20.04' }
            }
            steps {
                sh 'echo not implemented'
            }
        }
        }
    }
