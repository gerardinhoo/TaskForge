pipeline {
  agent any

  options {
    timestamps()
  }

  environment {
    // Jenkins will run docker compose from the repo workspace.
    // run tests in Docker using your backend-tests service.
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Backend Tests (Docker)') {
      steps {
        sh 'docker compose run --rm backend-tests'
      }
    }

    stage('Frontend Build') {
      steps {
        dir('frontend') {
          sh 'npm ci'
          sh 'npm run build'
        }
      }
    }

    stage('Build Images') {
      steps {
        sh 'docker compose build'
      }
    }
  }

  post {
    always {
      sh 'docker compose down --remove-orphans || true'
    }
  }
}
