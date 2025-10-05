# infrastructure/shared/outputs.tf

output "resource_group_name" {
  description = "Shared resource group name"
  value       = azurerm_resource_group.shared_rg.name
}

output "acr_name" {
  description = "Azure Container Registry name"
  value       = azurerm_container_registry.acr.name
}

output "acr_login_server" {
  description = "ACR login server"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  description = "ACR admin username"
  value       = azurerm_container_registry.acr.admin_username
  sensitive   = true
}

output "acr_admin_password" {
  description = "ACR admin password"
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
}

# output "tfstate_storage_account_name" {
#   description = "Storage account name for Terraform state"
#   value       = azurerm_storage_account.tfstate.name
# }

# output "tfstate_container_name" {
#   description = "Container name for Terraform state"
#   value       = azurerm_storage_container.tfstate.name
# }