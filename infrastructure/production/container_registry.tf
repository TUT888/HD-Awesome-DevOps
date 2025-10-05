# infrastructure/production/container_registry.tf

# Reference the shared ACR from the shared resource group
data "azurerm_container_registry" "shared_acr" {
  name                = "${var.prefix}acr"
  resource_group_name = "${var.prefix}-shared-rg"
}
