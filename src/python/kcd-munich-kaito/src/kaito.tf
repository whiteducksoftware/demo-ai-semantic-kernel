resource "azurerm_user_assigned_identity" "kaito" {
  name                = "mi-${var.stage}-${var.prefix}-kaito-gpu-provisioner"
  location            = var.location
  resource_group_name = azurerm_resource_group.core.name
  tags                = local.common_tags
}

resource "azurerm_federated_identity_credential" "kaito" {
  name                = "fc-mi-${var.stage}-${var.prefix}-kaito-gpu-provisioner"
  resource_group_name = azurerm_resource_group.core.name
  audience            = ["api://AzureADTokenExchange"]
  issuer              = azurerm_kubernetes_cluster.kaito.oidc_issuer_url
  parent_id           = azurerm_user_assigned_identity.kaito.id
  subject             = "system:serviceaccount:gpu-provisioner:gpu-provisioner"
}

resource "azurerm_role_assignment" "kaito" {
  scope                            = azurerm_kubernetes_cluster.kaito.id
  role_definition_name             = "Contributor"
  principal_id                     = azurerm_user_assigned_identity.kaito.principal_id
  skip_service_principal_aad_check = true
}

output "KAITO_IDENTITY_CLIENT_ID" {
  value = azurerm_user_assigned_identity.kaito.client_id
}
