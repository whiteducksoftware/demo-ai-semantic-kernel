resource "azurerm_kubernetes_cluster" "kaito" {
  name                = "aks-${var.stage}-${var.prefix}"
  location            = var.location
  resource_group_name = azurerm_resource_group.core.name
  dns_prefix          = "aks-${var.stage}-${var.prefix}"
  sku_tier = "Standard"
  image_cleaner_enabled = true
  image_cleaner_interval_hours = 24

  default_node_pool {
    name       = "system"
    vm_size    = "Standard_D4s_v4"
    node_count = 2
  }

  identity {
    type = "SystemAssigned"
  }

  azure_active_directory_role_based_access_control {
    managed                = true
    tenant_id              = data.azurerm_client_config.current.tenant_id
    admin_group_object_ids = ["429bfc0b-dac5-4dd8-862a-831985f20e4d"]
    azure_rbac_enabled     = true
  }

  # Network settings
  network_profile {
    network_plugin      = "azure"
    network_plugin_mode = "overlay"
    ebpf_data_plane     = "cilium"
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true
}
