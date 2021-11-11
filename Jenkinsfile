pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                dockerfile true

            }
            steps {
                // Install all python dependencies
                sh 'pip install --no-cache-dir -r requirements.txt --user'
                sh 'pip install --no-cache-dir -r requirements/dev.txt --user'
                sh 'pip install -e $HOME/workspace/nanny --user'
                // Run tests
                // sh ''
                // sh 'echo $PATH'
                // sh 'ls -la /.local/bin'
                sh 'PATH="$PATH:/.local/bin" && pytest --junit-xml test-reports/results.xml'
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