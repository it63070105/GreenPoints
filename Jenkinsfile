pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS=credentials('dockerhub')
    }

    stages {
        stage('Initialize Stage') {
            steps {
                echo 'Initial : Delete  containers and images'
                echo "Current path is ${pwd()}"
                bat "docker-compose down --rmi all --volumes || true"
            }
        }

        stage('Build Stage') {
            steps {
                echo "Build : Current path is ${pwd()}"
                bat 'dir'
                bat "docker-compose build"
            }
        }
        stage('Login Stage') {
          steps {
            echo "Login : Logging in . . ."
            bat '$DOCKERHUB_CREDENTIALS_PSW'
            bat '$DOCKERHUB_CREDENTIALS_USR'
            bat '$DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
          }
        }

        stage('Push Stage') {
            steps {
                dir('Image_process') { // change directory to Lab_docker_Jenkins
                    echo "Push : Current path is ${pwd()}"
                    bat "docker-compose push"
                }
            }
        }
        
        stage('Trigger Slave job') {
            steps {
                echo "Trigger : calling Slave job . . ."
                bat 'echo "HELLO ${DOCKERHUB_CREDENTIALS_USR}"'
                build job: 'slave', parameters: [string(name: 'DOCKERHUB_CREDENTIALS_USR', value: env.DOCKERHUB_CREDENTIALS_USR), string(name: 'DOCKERHUB_CREDENTIALS_PSW', value: env.DOCKERHUB_CREDENTIALS_PSW)]
            }
        }
    }
}
