pipeline {
    agent none
    stages {
        // stage('Test') {
        //     agent {
        //         dockerfile {
        //                 filename 'agent_test.dockerfile'
        //                 dir 'dockerfiles'
        //             }
        //     }
        //     steps {
        //         // Install all python dependencies
        //         sh 'pip install --no-cache-dir -r requirements.txt --user'
        //         sh 'pip install --no-cache-dir -r requirements/dev.txt --user'
        //         sh 'pip install -e "/home/workspace/nanny" --user'

        //         // Run tests
        //         sh 'PATH="$PATH:/.local/bin" && pytest --junit-xml test-reports/results.xml'
        //     }
        //     post {
        //         always { junit 'test-reports/results.xml' }
        //     }
        // }
        stage('Deliver') {
            agent {
                dockerfile {
                        filename 'agent_deliver.dockerfile'
                        dir 'dockerfiles'
                        args '-v /home/.ssh:/tmp/.ssh:ro --net=host -u root'
                }
            }
            steps {

                sh 'touch trial.txt'
                sh 'ls -la /'
                sh 'ls -la /bin'
                sh 'ls -la /usr/bin'
                sh 'ls -la /etc/ssh'
                sh 'ls -la /home/.ssh'
                sh 'ls -la /tmp/.ssh'
                sh '/usr/bin/ssh_permissions'
                // sh 'sleep 600'
                // sh 'ls -la /root/.ssh'
                sh 'scp -v -o StrictHostKeyChecking=no trial.txt pi@192.168.0.234:/home/pi/trial.txt'
                sh 'echo not implemented'
            }
        }
    }
}
