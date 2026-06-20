# 06 · CI/CD Pipelines

> CI/CD is the bridge between code and production. Master it, and you master automated software delivery.
> This module covers GitHub Actions, GitLab CI, Jenkins, and modern GitOps tools.

---

## 🎯 Learning Objectives

After completing this module, you should be able to:

- [ ] Understand CI/CD concepts (Continuous Integration / Continuous Delivery / Continuous Deployment)
- [ ] Write GitHub Actions workflows (build/test/deploy)
- [ ] Write GitLab CI pipelines (.gitlab-ci.yml)
- [ ] Configure Jenkins pipelines (Jenkisfile)
- [ ] Implement deployment strategies: Blue-Green / Canary / Rolling
- [ ] Use Argo CD / Flux for GitOps
- [ ] Secure CI/CD: secrets management, SBOM, vulnerability scanning
- [ ] Optimize CI/CD: caching, artifact reuse, parallel jobs
- [ ] Troubleshoot failed pipelines
- [ ] Design a complete CI/CD system for microservices

**After this module, you can automate any deployment workflow.**

---

## 📺 Recommended Video Tutorials

| Tutorial | Instructor | Link | Views | Rating |
|----------|-------------|------|-------|--------|
| GitHub Actions Full Course | TechWorld with Nana | [YouTube](https://www.youtube.com/watch?v=R8_veQiYBh) | 1.5M+ | ⭐⭐⭐⭐⭐ |
| GitLab CI/CD Complete | GitLab | [YouTube](https://www.youtube.com/watch?v=8PmhCF0kxs) | 200K+ | ⭐⭐⭐⭐ |
| Jenkins Pipeline | Kunal Kushwaha | [YouTube](https://www.youtube.com/watch?v=7KCS70sCoK0) | 300K+ | ⭐⭐⭐⭐ |
| Argo CD & GitOps | Codefresh | [YouTube](https://www.youtube.com/watch?v=MeU5_kOTzaY) | 400K+ | ⭐⭐⭐⭐⭐ |
| CI/CD Best Practices | AWS | [YouTube](https://www.youtube.com/watch?v=Qh9sS-Mjoy) | 100K+ | ⭐⭐⭐⭐ |

---

## 📖 Recommended Books

| Book | Author | Level | Comment |
|------|--------|-------|---------|
| *Continuous Delivery* | Jez Humble & David Farley | Advanced | The bible of CI/CD. |
| *Effective DevOps* | Jennifer Davis | Intermediate | CI/CD in DevOps context. |
| *Jenkins 2: Up & Running* | Brent Laster | Intermediate | Jenkins modern practices. |
| *GitOps with Argo CD* | O'Reilly | Advanced | GitOps deep dive. |

---

## 🌐 Online Resources

| Resource | Link | Features |
|----------|------|----------|
| GitHub Actions Docs | https://docs.github.com/actions/ | Official, comprehensive. |
| GitLab CI/CD Docs | https://docs.gitlab.com/ee/ci/ | Excellent examples. |
| Jenkins User Handbook | https://www.jenkins.io/doc/ | Complete reference. |
| Argo CD Docs | https://argo-cd.readthedocs.io/ | GitOps practice. |
| Awesome CI/CD | https://github.com/ligurio/awesome-ci | ⭐3k, curated tools list. |
| CICD Dragon | https://github.com/cicd-dragon/cicd-dragon | ⭐2k, CI/CD patterns. |

---

## 📝 Core Knowledge Checklist

### Phase 1: CI/CD Concepts (3-5 days)

#### What is CI/CD?
```
Traditional:  Code → Build (manual) → Test (manual) → Deploy (manual)
CI/CD:     Code → Build (auto)    → Test (auto)   → Deploy (auto)
```

- **CI (Continuous Integration)**: Merge code frequently, build & test automatically.
- **CD (Continuous Delivery)**: Auto-deploy to staging, manual approval for production.
- **CD (Continuous Deployment)**: Auto-deploy to production (no manual approval).

#### CI/CD Pipeline Stages
```
1. Code commit (trigger)
2. Build (compile/package)
3. Test (unit/integration/e2e)
4. Static analysis (lin, sonarqube)
5. Security scan (SAST/DAST/SCA)
6. Package (Docker image / JAR)
7. Push artifact (registry)
8. Deploy (staging/production)
9. Notify (Slack/Email)
```

---

### Phase 2: GitHub Actions (1 week)

#### Basic Workflow
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pul_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build & push Docker image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
      
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /app
            docker compose pul
            docker compose up -d
```

#### GitHub Actions Best Practices
```yaml
# 1. Use specific versions (not @main)
uses: actions/checkout@v4   # ✅ Good
uses: actions/checkout@main  # ❌ Risk: breaking changes

# 2. Cache dependencies
- uses: actions/setup-node@v4
  with:
    cache: 'npm'

# 3. Use secrets for sensitive data
env:
  API_KEY: ${{ secrets.API_KEY }}   # ✅ Good
  API_KEY: "hardcoded"             # ❌ NEVER

# 4. Limit permissions
permissions:
  contents: read
  packages: write

# 5. Use concurrency groups (cancel duplicate runs)
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

### Phase 3: GitLab CI (1 week)

#### Basic Pipeline
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

test:
  stage: test
  image: node:18-alpine
  script:
    - npm ci
    - npm run lint
    - npm test
  cache:
    paths:
      - node_modules/
  only:
    - merge_requests
    - main

build:
  stage: build
  image: docker:24-cli
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy_staging:
  stage: deploy
  script:
    - ssh deploy@staging "cd /app && docker compose pul && docker compose up -d"
  only:
    - main
  environment:
    name: staging
    url: https://staging.example.com

deploy_production:
  stage: deploy
  script:
    - ssh deploy@prod "cd /app && docker compose pul && docker compose up -d"
  only:
    - main
  when: manual   # Requires manual approval
  environment:
    name: production
    url: https://example.com
```

---

### Phase 4: Jenkins Pipeline (3-5 days)

#### Declarative Pipeline (Jenkisfile)
```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'myregistry.azurecr.io'
        IMAGE_NAME = 'myapp'
        DOCKER_CREDS = 'docker-registry-creds'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/myorg/myrepo.git'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm ci'
                sh 'npm run lint'
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }
        
        stage('Build & Push Docker') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", DOCKER_CREDS) {
                        def app = docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                        app.push()
                        app.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh "ssh deploy@staging 'cd /app && docker compose pul && docker compose up -d'"
            }
        }
        
        stage('Approve for Production') {
            steps {
                input message: 'Deploy to production?', ok: 'Yes'
            }
        }
        
        stage('Deploy to Production') {
            steps {
                sh "ssh deploy@prod 'cd /app && docker compose pul && docker compose up -d'"
            }
        }
    }
    
    post {
        success {
            slackSend(channel: '#devops', message: 'Pipeline succeeded!')
        }
        failure {
            slackSend(channel: '#devops', message: 'Pipeline failed!')
        }
    }
}
```

---

### Phase 5: GitOps with Argo CD (1 week)

#### What is GitOps?
```
Traditional CI/CD:  CI pushs to production
GitOps:            Git is the single source of truth → Argo CD puls from Git → sync to cluster
```

#### Install Argo CD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access UI
kubectl port-forward svc/argo-cd-server -n argocd 8080:443
# Visit: https://localhost:8080 (username: admin, password: from secret)
```

#### Application Manifest
```yaml
# app-of-apps.yaml (Argo CD Application)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: main
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true        # Delete resources removed from Git
      selfHeal: true   # Correct drift
    syncOptions:
      - CreateNamespace=true
```

#### Argo CD Best Practices
```
- Use "App of Apps" pattern (manage Argo CD apps via Git)
- Enable RBAC (don't give everyone admin access)
- Use Projects to isolate teams
- Configure notifications (Slack/PagerDuty)
- Regularly backup Argo CD state (etcd snapshot)
```

---

## 🔧 Hands-On: Build a Complete Pipeline

### Scenario: Node.js App → Docker → K8s

#### Step 1: GitHub Actions (CI)
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      
  build:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha
            type=ref,event=branch
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          
  update-helm:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          repository: myorg/myrepo-helm
          token: ${{ secrets.PAT }}
      - name: Update image tag in Helm values
        run: |
          sed -i "s/tag: .*/tag: ${{ github.sha }}/" charts/myapp/values.yaml
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add charts/myapp/values.yaml
          git commit -m "Update image tag to ${{ github.sha }}"
          git push
```

#### Step 2: Argo CD (CD)
- Argo CD watches `myrepo-helm` repo
- When `values.yaml` changes, Argo CD auto-syncs to K8s cluster

---

## 🚨 Common Troubleshooting

### Pipeline fails at "docker push" (authentication error)

```bash
# GitHub Actions: Use GITHUB_TOKEN (auto-provided)
- name: Log in to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

# GitLab CI: Use CI_JOB_TOKEN (auto-provided)
# Or define CI_REGISTRY_USER / CI_REGISTRY_PASSWORD in Settings → CI/CD → Variables
```

### Tests pass locally but fail in CI

```bash
# Common causes:
# 1. Node version mismatch
# → Pin node-version in workflow

# 2. Missing environment variables
# → Add to GitHub Secrets, then reference in workflow

# 3. Timing issues (async tests)
# → Increase timeout: jest.setTimeout(10000)
```

### Deployment fails (K8s cluster unreachable)

```bash
# GitHub Actions: Use kubeconfig action
- name: Set up kubectl
  uses: azure/setup-kubectl@v3
  
- name: Deploy to K8s
  run: |
    echo "${{ secrets.KUBECONFIG }}" > kubeconfig
    export KUBECONFIG=kubeconfig
    kubectl apply -f k8s/
```

---

## 🏭 Production Best Practices

### 1. Secret Management
```yaml
# ❌ DON'T: Hardcode secrets
env:
  API_KEY: "sk-abc123"

# ✅ DO: Use vault/secrets manager
env:
  API_KEY: ${{ secrets.API_KEY }}

# Even better: Use HashiCorp Vault / AWS Secrets Manager
- name: Retrieve secret from Vault
  uses: hashicorp/vault-action@v2
  with:
    url: https://vault.example.com
    tken: ${{ secrets.VAULT_TOKEN }}
    secrets: |
      secret/data/api API_KEY;
```

### 2. Deployment Strategies
```yaml
# Blue-Green (zero-downtime)
# 1. Deploy new version (green) alongside old (blue)
# 2. Test green
# 3. Switch load balancer to green
# 4. Keep blue for rollback

# Canary (gradual rollout)
# Argo CD: Use trafic weighting
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 20    # 20% traffic to new version
        - pause: { duration: 30m }
        - setWeight: 50
        - pause: { duration: 30m }
        - setWeight: 100
```

### 3. Pipeline Security (Supply Chain)
```yaml
# Generate SBOM (Software Bil of Materials)
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    format: spdx-json

# Scan for vulnerabilities
- name: Scan image
  uses: aquasecurity/trivy-action@0.11.0
  with:
    image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
    format: 'table'
    exit-code: '1'   # Fail pipeline if vulnerabilities found
```

---

## 📊 Comparison: CI/CD Tools

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **GitHub Actions** | GitHub-hosted projects | Tight integration, huge marketplace | Vendor lock-in |
| **GitLab CI** | GitLab-hosted projects | Built-in, powerful, free CI minutes | Steep learning curve |
| **Jenkins** | On-premise, complex pipelines | Extensible, mature | Hard to maintain, XML hell |
| **Argo CD** | K8s GitOps | Declarative, Git as single source of truth | Requires K8s knowledge |
| **CircleCI** | Fast builds | Speed, simplicity | Expensive at scale |
| **Buildkite** | Custom runners | Flexible, hybrid cloud | Setup overhead |

---

## ✅ Self-Check Quiz

After learning, try to answer these:

- [ ] What's the difference between Continuous Delivery and Continuous Deployment?
- [ ] How does GitHub Actions cache work? How to optimize it?
- [ ] How do you secure secrets in CI/CD pipelines?
- [ ] What's GitOps? How does Argo CD implement it?
- [ ] How do you implement Blue-Green deployment?
- [ ] What's the difference between `stage`, `step`, and `job` in Jenkins?
- [ ] How do you troubleshoot a failed pipeline?
- [ ] What's an SBOM? Why is it important?
- [ ] How do you configure multi-environment deployments (staging/production)?
- [ ] What's the "Detached HEAD" problem in CI/CD?

---

> CI/CD is the heart of modern DevOps. Master it, and you become the engineer who bridges development and production.
> Next recommended: [08_Monitoring_Observability](../08_Monitoring_Observability/) — Learn to monitor what you deploy.
