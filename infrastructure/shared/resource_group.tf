# infrastructure/shared/resource_group.tf

resource "azurerm_resource_group" "shared_rg" {
  name     = "${var.prefix}-shared-rg"
  location = var.location

  tags = {
    Environment = "Shared"
    ManagedBy   = "Terraform"
    Purpose     = "Shared resources across all environments"
  }
}