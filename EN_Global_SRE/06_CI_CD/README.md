# 06 · CI/CD Pipelines

> Automation is the heart of DevOps. If you're still deploying manually, you're not doing DevOps.
> This module covers the full pipeline: from code commit to production deployment.

---

## 🎯 Learning Objectives

By the end of this module, you should be able to:

- [ ] Understand CI vs CD and why both matter
- [ ] Set up a Jenkins pipeline from scratch
- [ ] Configure GitLab CI with `.gitlab-ci.yml`
- [ ] Use GitHub Actions for CI/CD
- [ ] Write a multi-stage pipeline (build → test → deploy)
- [ ] Implement environment promotion (dev → staging → production)
- [ ] Use artifacts and caching to speed up builds
- [ ] Implement deployment strategies: rolling, blue-green, canary
- [ ] Secure your pipeline (secrets management, supply chain security)
- [ ] Monitor pipeline health and failure rates

---

## 📺 Recommended Video Courses

| Course | Instructor | Platform | Duration | Rating |
|--------|-----------|----------|----------|--------|
| **GitHub Actions Full Course** | TechWorld with Nana | YouTube | 2h | ⭐⭐⭐⭐⭐ |
| **Jenkins Full Course** | FreeCodeCamp | YouTube | 4h | ⭐⭐⭐⭐⭐ |
| **CI/CD with GitLab** | Sander van Vugt | O'Reilly | 3h | ⭐⭐⭐⭐ |
| **ArgoCD Tutorial** | Codefresh | YouTube | 1.5h | ⭐⭐⭐⭐ |

---

## 📖 Recommended Books

| Book | Author | Stage | Comment |
|------|--------|-------|---------|
| **Continuous Delivery** | Jez Humble | Advanced | The foundation. Every concept here is still relevant. |
| **Accelerate** | Nicole Forsgren | Advanced | Data-driven DevOps. DORA metrics explained. |
| **CI/CD with Docker and Kubernetes** | O'Reilly | Advanced | Practical, hands-on. |
| **GitHub Actions in Action** | Manning | Intermediate | If you use GitHub, this is the one. |
| **Jenkins 2: Up and Running** | O'Reilly | Intermediate | Jenkinsfile, shared libraries, pipelines. |

---

## 🌐 Online Resources

| Resource | Link | Features |
|----------|------|----------|
| **GitHub Actions Docs** | https://docs.github.com/en/actions | Official, comprehensive |
| **GitLab CI/CD Docs** | https://docs.gitlab.com/ee/ci/ | Excellent examples |
| **Jenkins User Documentation** | https://www.jenkins.io/doc/ | Huge, search for specifics |
| **Awesome CI/CD** | https://github.com/ligurio/awesome-ci | Curated tools list |
| **DORA Metrics** | https://cloud.google.com/blog/products/devops-sre/ | What to measure |
| **ArgoCD Docs** | https://argo-cd.readthedocs.io/ | GitOps deployment |

---

## 📝 Core Knowledge Checklist

### Phase 1: CI/CD Fundamentals (1 week)

- What CI/CD solves: manual errors, slow releases, no rollback
- CI vs CD vs CD (Continuous Delivery vs Continuous Deployment)
- The typical pipeline stages:
  ```
  code commit → build → test → package → deploy to staging → deploy to prod
  ```
- Key metrics: lead time, deployment frequency, MTTR, change failure rate
- DORA metrics explained (Google research)

### Phase 2: Jenkins — The Classic Choice (2 weeks)

#### Installing and configuring Jenkins
- Run Jenkins in Docker (easiest way to start):
  ```bash
  docker run -d -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
  ```
- Unlock Jenkins (find initial admin password in logs)
- Install suggested plugins
- Create your first Freestyle job

#### Jenkinsfile — Declarative Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
    post {
        failure {
            mail to: 'team@example.com', subject: 'Build Failed'
        }
    }
}
```

#### Key Jenkins concepts
- **agent**: where the pipeline runs (any, label, docker)
- **stage**: logical division of work
- **steps**: actual commands
- **post**: actions after pipeline (always, success, failure)
- **environment**: environment variables
- **parameters**: user input at build time
- **credentials**: storing secrets in Jenkins

#### Jenkins best practices
- Store `Jenkinsfile` in the repo (versioned with code)
- Use **shared libraries** for reusable logic
- Use **agentless** pipelines when possible (offload to Kubernetes)
- Set up **role-based access control** (RBAC)
- Back up `JENKINS_HOME` regularly

### Phase 3: GitLab CI/CD (1-2 weeks)

#### `.gitlab-ci.yml` structure
```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  image: node:18
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

test_job:
  stage: test
  image: node:18
  script:
    - npm test
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

deploy_staging:
  stage: deploy
  script:
    - kubectl apply -f k8s/staging/
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main

deploy_prod:
  stage: deploy
  script:
    - kubectl apply -f k8s/prod/
  environment:
    name: production
    url: https://example.com
  when: manual  # Requires manual click to deploy to prod
  only:
    - main
```

#### Key GitLab CI features
- **Runners**: shared, group, or specific runners
- **Artifacts**: pass files between jobs
- **Caching**: speed up jobs (node_modules, pip cache)
- **Environments**: track deployments per environment
- **Review Apps**: auto-deploy PR branches to temporary environments
- **Container Registry**: built-in Docker registry

### Phase 4: GitHub Actions (1 week)

#### Basic workflow file
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
  
  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: myapp:${{ github.sha }}
```

#### Key GitHub Actions concepts
- **Workflow**: the YAML file (lives in `.github/workflows/`)
- **Event**: what triggers the workflow (push, PR, schedule, manual)
- **Job**: a set of steps, runs on a runner
- **Step**: individual task (run command or use an action)
- **Action**: reusable unit (can be from the Marketplace)
- **Runner**: the VM that runs the job (GitHub-hosted or self-hosted)
- **Secret**: encrypted environment variable

### Phase 5: Deployment Strategies (1 week)

| Strategy | How it works | Pros | Cons |
|----------|--------------|------|------|
| **Rolling** | Replace pods gradually | Zero downtime | Slow rollback |
| **Blue-Green** | Two identical environments, switch traffic | Instant rollback | Double resource cost |
| **Canary** | Route small % of traffic to new version | Low risk | Complex setup |
| **Shadow** | Mirror traffic to new version, don't serve | Test with real traffic | Complex |

#### Implementing blue-green with K8s
```yaml
# Service points to "blue" by default
# Deploy "green" with new version
# Test green
# Switch service selector to green
# Keep blue running for quick rollback
```

### Phase 6: Pipeline Security (1 week)

- **Never commit secrets**: use Vault, AWS Secrets Manager, or GitHub Secrets
- **Pin action versions**: `actions/checkout@v4` not `@main`
- **Supply chain security**: SBOM (Software Bill of Materials), sigstore/cosign
- **Least privilege**: pipeline should only have permissions it needs
- **Scan dependencies**: `npm audit`, Snyk, OWASP Dependency-Check
- **Container scanning**: Trivy, Clair
- **SAST/DAST**: SonarQube, OWASP ZAP

---

## 🔧 Hands-on Projects

| Project | Difficulty | What you'll learn |
|---------|-------------|-------------------|
| **Set up Jenkins on K8s** | ⭐⭐⭐ | Jenkins operator, persistence, agents |
| **Multi-stage pipeline with GitLab** | ⭐⭐⭐ | Environments, review apps, manual gates |
| **GitHub Actions + Docker + K8s** | ⭐⭐⭐⭐ | Full automation from commit to prod |
| **Canary deployment with Flagger** | ⭐⭐⭐⭐⭐ | Progressive delivery, metrics-based rollout |
| **Pipeline security audit** | ⭐⭐⭐ | Secret scanning, supply chain security |

---

## ⚠️ Common Pitfalls

| Pitfall | Why it happens | How to avoid |
|---------|----------------|---------------|
| Long-running tests block pipeline | Tests are too slow or too many | Parallelize tests, run only affected tests |
| Secrets in pipeline logs | Printing env vars for debugging | Never `echo $SECRET`, use masked variables |
| "It works on my machine" | Inconsistent build environments | Use Docker for build steps (same image everywhere) |
| Fragile pipelines | Too many manual steps, tight coupling | Make pipelines idempotent and self-contained |
| No rollback plan | Assumes deployment always succeeds | Always have a rollback strategy (and test it!) |
| Ignoring flaky tests | "It's just a flaky test, merge it" | Fix flaky tests immediately, they erode trust |

---

## ✅ Self-Check: Can you...

- [ ] Write a `Jenkinsfile` that builds, tests, and deploys to K8s?
- [ ] Set up a GitHub Actions workflow that triggers on PR and runs tests?
- [ ] Explain the difference between rolling, blue-green, and canary deployments?
- [ ] Secure a pipeline: where do you store secrets?
- [ ] Set up a multi-stage pipeline with manual approval for production?
- [ ] Measure DORA metrics for your team's pipeline?

> 💡 **Next step**: After this module, move on to **09 · Monitoring & Observability** to close the loop: deploy → monitor → improve.
