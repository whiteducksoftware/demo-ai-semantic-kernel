locals {
  # Common tags to be assigned to all resources
  common_tags = {
    env       = var.stage
    managedBy = data.azurerm_client_config.current.client_id
    project   = var.prefix
  }
}

# get current subscription
data "azurerm_subscription" "current" {
}

# get current client
data "azurerm_client_config" "current" {
}

resource "azurerm_resource_group" "core" {
  name     = "rg-${var.stage}-${var.prefix}"
  location = "West Europe"
}
