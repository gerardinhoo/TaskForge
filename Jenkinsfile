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
          set -eux
          docker run --rm --network taskforge_default alpine sh -lc "
            apk add --no-cache curl >/dev/null
            echo 'Hitting SonarQube...'
            curl -s -o /dev/null -w 'HTTP=%{http_code}\\n' http://sonarqube:9000/api/system/status
            echo
            curl -s http://sonarqube:9000/api/system/status
          "
        '''
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          sh '''
            set -eux
            docker run --rm \
              --network taskforge_default \
              -e SONAR_TOKEN="$SONAR_TOKEN" \
              -v "$PWD:/usr/src" \
              -w /usr/src \
              sonarsource/sonar-scanner-cli \
              -Dsonar.projectKey=taskforge \
              -Dsonar.sources=app \
              -Dsonar.host.url=http://sonarqube:9000 \
              -Dsonar.python.coverage.reportPaths=coverage.xml \
              -Dsonar.login="$SONAR_TOKEN"
          '''
        }
      }
    }



    stage('Quality Gate') {
      steps {
        timeout(time: 5, unit: 'MINUTES') {
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
