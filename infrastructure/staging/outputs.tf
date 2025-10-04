# infrastructure/staging/outputs.tf

output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.staging_rg.name
}

output "aks_cluster_name" {
  description = "AKS cluster name"
  value       = azurerm_kubernetes_cluster.staging_aks.name
}

output "aks_kube_config" {
  description = "AKS kubeconfig"
  value       = azurerm_kubernetes_cluster.staging_aks.kube_config_raw
  sensitive   = true
}

output "acr_login_server" {
  description = "ACR login server"
  value       = data.azurerm_container_registry.shared_acr.login_server
}

output "git_sha" {
  description = "Git commit SHA"
  value       = var.git_sha
}