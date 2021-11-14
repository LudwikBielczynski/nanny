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
        stage('Deploy') {
            agent {
                dockerfile {
                        filename 'agent_deliver.dockerfile'
                        dir 'dockerfiles'
                        args '--net=host -u root'
                }
            }
            steps {
                sh 'scp -v -i /root/.ssh/id_rsa -o StrictHostKeyChecking=no services/save_audio.service pi@192.168.0.234:/home/pi/services/save_audio.service'
                sh 'ssh -v -i /root/.ssh/id_rsa pi@192.168.0.234 /bin/bash < jenkins/scripts/update_local_git'
                sh 'ssh -v -i /root/.ssh/id_rsa pi@192.168.0.234 /bin/bash < jenkins/scripts/restart_audio_service'
            }
        }
    }
}
