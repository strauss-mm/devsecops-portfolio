output "namespaces" {
  value = [
    kubernetes_namespace.app_team.metadata[0].name,
    kubernetes_namespace.database.metadata[0].name,
    kubernetes_namespace.monitoring.metadata[0].name,
  ]
}

output "service_accounts" {
  value = {
    developer       = "${kubernetes_namespace.app_team.metadata[0].name}:${kubernetes_service_account.developer.metadata[0].name}"
    deployer        = "${kubernetes_namespace.app_team.metadata[0].name}:${kubernetes_service_account.deployer.metadata[0].name}"
    security_auditor = "default:${kubernetes_service_account.security_auditor.metadata[0].name}"
  }
}

output "network_policies" {
  value = [
    kubernetes_network_policy.default_deny_app_team.metadata[0].name,
    kubernetes_network_policy.default_deny_database.metadata[0].name,
    kubernetes_network_policy.allow_frontend_to_backend.metadata[0].name,
    kubernetes_network_policy.allow_backend_to_database.metadata[0].name,
  ]
}
