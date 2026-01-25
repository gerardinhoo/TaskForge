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

    stage('Sonar Connectivity Check') {
      steps {
        sh '''
          set -x
          docker run --rm alpine sh -lc "
            apk add --no-cache curl >/dev/null
            echo 'Hitting SonarQube...'
            curl -s -o /dev/null -w 'HTTP=%{http_code}\\n' http://host.docker.internal:9000/api/system/status
            echo
            curl -s http://host.docker.internal:9000/api/system/status
          "
        '''
      }
    }
  
    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('sonarqube-local') {
          sh '''
            set -x
            echo "SONAR_HOST_URL=$SONAR_HOST_URL"
            echo "WORKSPACE=$WORKSPACE"
            ls -la
            ls -la coverage.xml || true

            docker run --rm \
              -e SONAR_HOST_URL="$SONAR_HOST_URL" \
              -e SONAR_TOKEN="$SONAR_AUTH_TOKEN" \
              -v "$WORKSPACE:/usr/src" \
              sonarsource/sonar-scanner-cli:latest \
              -Dsonar.projectKey=taskForge \
              -Dsonar.sources=app \
              -Dsonar.python.coverage.reportPaths=coverage.xml \
              -X

            echo "---- scanner output file check ----"
            ls -la .scannerwork || true
            ls -la .scannerwork/report-task.txt || true
            cat .scannerwork/report-task.txt || true
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

