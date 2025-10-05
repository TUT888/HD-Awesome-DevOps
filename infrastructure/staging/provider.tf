terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
  required_version = ">= 1.1.0"
}

provider "azurerm" {
  # Allow resource delete on staging environment
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Configure Kubernetes provider to manage namespace
provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.staging_aks.kube_config[0].host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.staging_aks.kube_config[0].client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.staging_aks.kube_config[0].client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.staging_aks.kube_config[0].cluster_ca_certificate)
}