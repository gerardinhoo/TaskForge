pipeline {
  agent any

  options {
    timestamps()
  }


  stages {
    stage('Backend Tests (Docker)') {
      steps {
        sh 'docker compose -f docker-compose.ci.yml up --build --abort-on-container-exit'
      }
    }

    stage('SonarQube Analysis') {
    environment {
        SONAR_SCANNER_OPTS = "-Xmx512m"
    }
    steps {
        withSonarQubeEnv('sonarqube-local') {
            sh '''
              docker run --rm \
                --network taskforge_default \
                -e SONAR_HOST_URL="$SONAR_HOST_URL" \
                -e SONAR_TOKEN="$SONAR_AUTH_TOKEN" \
                -v "$WORKSPACE:/usr/src" \
                sonarsource/sonar-scanner-cli:latest \
                -Dsonar.projectKey=taskForge \
                -Dsonar.sources=app \
                -Dsonar.python.coverage.reportPaths=coverage.xml
                  '''
        }
    }
}

    stage('Quality Gate') {
        steps {
            timeout(time: 2, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
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
        sh 'docker compose -f docker-compose.ci.yml build'
      }
    }
  }

  post {
    always {
      sh 'docker compose -f docker-compose.ci.yml down -v --remove-orphans || true'
    }
  }
}
