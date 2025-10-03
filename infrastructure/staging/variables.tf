# Specify the environment
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "staging"
}

# Specify the prefix, ensuring all resources have unique naming
variable "prefix" {
  description = "Prefix for all resource names"
  type        = string
  default     = "sit722alice"
}

# Resource configuration variables
variable "location" {
  description = "Azure region"
  type        = string
  default     = "australiaeast"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.31.7"
}

variable "node_count" {
  description = "Number of AKS nodes"
  type        = number
  default     = 1
}

variable "node_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "git_sha" {
  description = "Git commit SHA for tagging"
  type        = string
  default     = "manual"
}