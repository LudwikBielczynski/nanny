pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                dockerfile {
                        filename 'agent_test.dockerfile'
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
                dockerfile {
                        filename 'agent_deliver.dockerfile'
                        dir 'dockerfiles'
                        args '-v /home/.ssh:/tmp/.ssh:ro --net=host'
                }
            }
            steps {
                sh 'touch trial.txt'
                sh 'ls -la /tmp/.ssh'
                sh 'ls -la /home'
                sh 'ls -la /home/deploy'
                sh 'scp trial.txt pi@192.168.0.234:/home/pi/trial.txt'
                sh 'echo not implemented'
            }
        }
    }
}
