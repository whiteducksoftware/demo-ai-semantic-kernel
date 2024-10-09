################################
############ Common ############
################################

variable "stage" {
  description = "(Required) The stage."
  type        = string
  default     = "kcd"
}

variable "prefix" {
  description = "(Required) The prefix for the resources created in the specified Azure Resource Group"
  type        = string
  default     = "kaito"
}

# resource location
variable "location" {
  description = "The location used for all resources"
  type        = string
  default     = "northeurope"
}
