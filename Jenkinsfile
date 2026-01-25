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
                set -e
                echo "Workspace: $WORKSPACE"
                ls -la || true
                ls -la coverage.xml || true

                docker run --rm \
                  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
                  -e SONAR_TOKEN="$SONAR_AUTH_TOKEN" \
                  -v "$WORKSPACE:/usr/src" \
                  sonarsource/sonar-scanner-cli:latest \
                  -Dsonar.projectKey=taskForge \
                  -Dsonar.sources=app \
                  -Dsonar.python.coverage.reportPaths=coverage.xml

                echo "---- report-task.txt (if generated) ----"
                find . -maxdepth 3 -type f -name report-task.txt -print -exec cat {} \\; || true
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
