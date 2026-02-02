# TaskForge — Cloud, DevOps & SRE Portfolio Project

## Overview

**TaskForge** is a full-stack application used as a hands-on portfolio project to demonstrate real-world **Cloud**, **DevOps**, **CI/CD**, and **Site Reliability Engineering (SRE)** practices on AWS.

The project was built incrementally across multiple phases to reflect how production systems evolve over time, focusing on practical engineering decisions, infrastructure automation, and operational readiness.

---

## High-Level Architecture

- Frontend: Static web application served by NGINX (Dockerized)
- Backend: Python API (FastAPI + Uvicorn, Dockerized)
- Infrastructure: AWS EC2 provisioned with CloudFormation
- Container Registry: Amazon ECR
- CI/CD: GitHub Actions
- Observability: AWS CloudWatch

**Screenshot placeholder:**
`docs/screenshots/architecture-overview.png`

---

## Technology Stack

### Application
- Frontend: JavaScript (Vite)
- Backend: Python (FastAPI)

### Cloud & DevOps
- AWS EC2
- AWS ECR
- AWS CloudFormation
- AWS IAM
- Docker & Docker Compose
- GitHub Actions
- Jenkins

### SRE / Monitoring
- AWS CloudWatch Agent
- EC2 system metrics
- Log collection

---

## Project Phases

### Phase 1 — Application Baseline
- Established frontend and backend services
- Verified local functionality

### Phase 2 — Docker & Local Containerization
- Dockerized frontend and backend
- Multi-stage Docker builds
- Docker Compose orchestration

**Screenshot:**
`docs/screenshots/docker-compose-local.png`

### Phase 3 — CI/CD Pipelines
- GitHub Actions for CI
- Jenkins pipelines
- Linting, testing, and build validation

**Screenshot:**
`docs/screenshots/ci-pipeline-success.png`

### Phase 4 — EC2 Deployment with ECR
- CloudFormation-provisioned EC2
- Docker images pushed to ECR
- Containers deployed via Docker Compose
- IAM roles and security groups configured

**Screenshots:**
- `docs/screenshots/cloudformation-stack.png`
- `docs/screenshots/ecr-images.png`
- `docs/screenshots/ec2-running-containers.png`

### Phase 5 — SRE & Monitoring
- CloudWatch Agent installed on EC2
- CPU, memory, and disk metrics collected
- Log ingestion validated

**Screenshots:**
- `docs/screenshots/cloudwatch-metrics.png`
- `docs/screenshots/cloudwatch-logs.png`

---

## Security Practices

- No hard-coded credentials
- IAM roles attached to EC2
- Least-privilege access
- Environment variables managed securely

---

## Deployment Flow

1. Provision infrastructure via CloudFormation
2. Build Docker images
3. Push images to Amazon ECR
4. Pull images on EC2
5. Run containers using Docker Compose
6. Monitor using CloudWatch

---

## Portfolio Talking Points

- Infrastructure as Code (CloudFormation)
- CI/CD pipeline safety
- Secure container image handling
- AWS IAM role-based access
- SRE fundamentals with CloudWatch
- Pragmatic engineering tradeoffs

---

## Future Enhancements

- ECS or EKS migration
- Application Load Balancer
- Blue/green deployments
- Centralized logging
- Distributed tracing

---

## Screenshot Directory Structure

```
docs/
└── screenshots/
    ├── architecture-overview.png
    ├── docker-compose-local.png
    ├── ci-pipeline-success.png
    ├── cloudformation-stack.png
    ├── ecr-images.png
    ├── ec2-running-containers.png
    ├── cloudwatch-metrics.png
    └── cloudwatch-logs.png
```

---

**Project complete — Phase 5 finalized.**

