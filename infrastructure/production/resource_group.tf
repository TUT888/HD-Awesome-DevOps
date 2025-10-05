# infrastructure/production/resource_group.tf

resource "azurerm_resource_group" "production_rg" {
  name     = "${var.prefix}-${var.environment}-rg"
  location = var.location

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    GitSHA      = var.git_sha
    Critical    = "true"
  }
}