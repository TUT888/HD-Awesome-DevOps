# infrastructure/shared/variables.tf

variable "prefix" {
  description = "Prefix for all resource names"
  type        = string
  default     = "sit722alicestd"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "australiaeast"
}
