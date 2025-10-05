# Microsoft Azure - Project with DevOps Feature

This project is a part of HD task for SIT722 - Software Deployment and Operations, focusing on learning DevOps Cycle and pipelines

## Setup

To run this CI/CD project, we must initialize some existing resource (as in real production, these resource always available)
- Initialize shared infrastructure, refer to section [Shared Azure Resource](#shared-existing)
- Initialize production infrastructure, refer to section [Production Azure Resource](#production-existing)


## Azure Infrastructure and Resources
### Staging (Dynamic and Automation) 
The staging resource can either:
- Ephemeral environment where it is created, deploy, test and removed after the staging complete
- Remains active as a 1-1 replica of production for manual testing and troubleshooting

To reduce cost for learning purpose only, this project follows the first approach. The staging infrastructure information can be found at `infrastructure/staging`, resources include:
- Staging resource group
- Staging AKS, with related deployment information (Kubernetes manifest) can be found at `k8s/staging`

### Shared (Existing)
Shared resource is the existing resource on Azure, contains the resources that shared between staging and production. It is not created during CI-CD pipeline, and it requires manual review and manage since it relates to production.

Shared resource setup can be found at `infrastructure/shared`, resources include:
- Shared resource group
- Shared container registry

Commands
```bash
cd infrastructure/shared
tofu init
tofu plan
tofu apply 
```

### Production (Existing)
Production environment is where we deliver the product to the user, it must pass the manual approvals and should only be merge with develop branch, after all tests and check passed.

The production infrastructure information can be found at `infrastructure/production`, resources include:
- Staging resource group
- Staging AKS, with related deployment information (Kubernetes manifest) can be found at `k8s/production`