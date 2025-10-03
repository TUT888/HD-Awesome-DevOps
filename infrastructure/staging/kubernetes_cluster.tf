# infrastructure/staging/kubernetes_cluster.tf

resource "azurerm_kubernetes_cluster" "staging_aks" {
  name                = "${var.prefix}-${var.environment}-aks"
  location            = var.location
  resource_group_name = azurerm_resource_group.staging_rg.name
  dns_prefix          = "${var.prefix}-${var.environment}"
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.node_vm_size

    # Enable auto-scaling for cost optimization (optional for cost optimization)
    # enable_auto_scaling = true
    # min_count          = 1
    # max_count          = 3
  }

  # Use a system‐assigned managed identity
  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    GitSHA      = var.git_sha
  }

  # Uncomment if enabling auto-scaling above
  # lifecycle {
  #   ignore_changes = [
  #     default_node_pool[0].node_count
  #   ]
  # }
}

# Grant AKS permission to pull images from your ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.staging_aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = data.azurerm_container_registry.shared_acr.id
  skip_service_principal_aad_check = true
}

# Create staging namespace
resource "kubernetes_namespace" "staging" {
  metadata {
    name = var.environment
    labels = {
      environment = var.environment
      managed-by  = "terraform"
    }
  }

  depends_on = [azurerm_kubernetes_cluster.staging_aks]
}