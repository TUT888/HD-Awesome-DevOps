# infrastructure/staging/resource_group.tf

resource "azurerm_resource_group" "staging_rg" {
  name     = "${var.prefix}-${var.environment}-rg"
  location = var.location

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    GitSHA      = var.git_sha
    AutoDestroy = "true"
  }
}