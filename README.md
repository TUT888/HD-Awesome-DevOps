# Microsoft Azure - Project with DevOps Features

This project is part of the HD task for SIT722 - Software Deployment and Operations, focusing on learning and applying the DevOps cycle and CI/CD pipelines.

## Table of Contents
- [About This Project](#about-this-project)
  - [Tech Stack](#tech-stack)
  - [Tools & Libraries](#tools--libraries)
- [CI/CD Workflows](#cicd-workflows)
  - [Feature Branches](#feature-branches-feature-or-fix)
  - [Develop Branch (Staging)](#develop-branch-staging)
  - [Main Branch (Production)](#main-branch-production)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Azure Infrastructure and Resources](#azure-infrastructure-and-resources)
  - [Staging (Dynamic and Automated)](#staging-dynamic-and-automated)
  - [Shared (Existing)](#shared-existing)
  - [Production (Existing)](#production-existing)

## About this project
### Tech stack
- Frontend: Static HTML/CSS/JavaScript served by Nginx
- Backend: Two Python microservices (Notes Service + Users Service)
- Database: PostgreSQL
- Cloud Platform: Microsoft Azure

### Tools & libraries
- IaC (Infrastructure as Code): OpenTofu
- Container Security Scan: Trivy
- Unit & Integration Tests: `pytest`
- Coverage Report: `pytest-cov`
- Code Quality Check: `pylint`
- Code Vulnerability Scan: `bandit`
- Acceptance Testing (End-to-End): `playwright-python`

### CI/CD workflows

#### Feature Branches (`feature/*` or `fix/*`)
- Run unit tests, integration tests, and code coverage checks (> 80%)
- Run code quality checks (> 8.0/10)
- Perform code security scans

#### Develop Branch (staging):
- Pull request to `develop`:
  - Runs the same tests as feature branches
  - Includes additional acceptance tests to validate cross-service workflows
- Merge to `develop`:
  - Build: Build images, scan them, tag with Git SHA, and push to ACR
  - Deploy: Provision infrastructure and deploy services to AKS
  - Test: Run smoke tests to verify service connectivity
  - Cleanup: Destroy staging infrastructure to reduce cost (cost saving for learning purposes)

#### Main Branch (production):
- Pull request to `main`: Re-runs all tests similar to the develop branch
- After merge to `main` (manual trigger):
  - Build: Build images, scan them, tag with version tags, and push to ACR
  - Deploy: Deploy services to the existing production AKS
  - Test: Run smoke tests to verify service connectivity

## Project Structure
```bash
.
├── .github/
│   ├── scripts/ # Scripts to be used in CD process
│   │   ├── backend_smoke_tests.sh # Test backend service 
│   │   ├── frontend_smoke_tests.sh # Test frontend service
│   │   ├── get_backend_ip.sh # Get the backend external IP 
│   │   └── get_frontend_ip.sh # Get the frontend external IP 
│   └── workflows/ # CI/CD workflow files
│       ├── _reusable_quality_check_workflow.yml # Code quality & security scan
│       ├── _reusable_test_workflow.yml # Unit + integration test & coverage
│       ├── acceptance_test_cd.yml # End-to-end user flow testing
│       ├── cd-production-deploy.yml # Production deployment (branch main)
│       ├── cd-staging-deploy.yml # Staging deployment (branch develop)
│       ├── feature_test_notes_service.yml # Call 2 reusable workflow 
│       └── feature_test_users_service.yml # Call 2 reusable workflow
├── backend/ # Code for backend
│   ├── notes_service/
│   │   ├── app/ # Source code
│   │   ├── tests/ # Testing
│   │   │   ├── unit/ # Unit testing 
│   │   │   ├── integration/ # Integratio testing
│   │   │   └── ...
│   │   └── ...
│   └── users_service/ # Similar to notes_service
│       └── ...
├── frontend # Code for frontend
├── infrastructure # Infrastructure provisioning with OpenTofu
│   ├── production/ # Real production
│   ├── shared/ # Shared between production and staging
│   └── staging/ # Staging
├── k8s/ # Kubernetes manifest
│   ├── docker-desktop/ # Local machine testing
│   ├── production/ # For production
│   └── staging/ # For staging
├── playwright-python/ # For acceptance testing
└── docker-compose.yml
```

## Prerequisites

Before running this CI/CD project, some existing resources must be initialized (as in a real production setup, these resources are pre-existing):
- Initialize shared infrastructure, refer to section [Shared Azure Resource](#shared-existing)
- Initialize production infrastructure, refer to section [Production Azure Resource](#production-existing)


## Azure Infrastructure and Resources
### Staging (Dynamic and Automated) 
The staging environment can be either:
- **Ephemeral**: Created, deployed, tested, and removed after completion
- **Persistent**: A 1:1 replica of production for manual testing and troubleshooting

To minimize costs for learning purposes, this project follows the ephemeral approach.

Staging infrastructure details can be found in `infrastructure/staging`. Resources include::
- Staging resource group
- Staging AKS cluster (deployment manifests in `k8s/staging`)

### Shared (Existing)
The shared resources are existing Azure resources that are used by both staging and production environments.
They are **not created automatically** in the CI/CD pipeline and require **manual management and review**, as they are related to production.

Setup instructions can be found in `infrastructure/shared`. Resources include:
- Shared resource group
- Shared container registry

Commands:
```bash
cd infrastructure/shared
tofu init
tofu plan
tofu apply 
```

### Production (Existing)
The production environment is the final delivery stage for users.
It must pass manual approval and can only be merged from the `develop` branch after all tests and checks have passed.

Production infrastructure details can be found in `infrastructure/production`. Resources include:
- Production resource group
- Production AKS cluster (deployment manifests in `k8s/production`)