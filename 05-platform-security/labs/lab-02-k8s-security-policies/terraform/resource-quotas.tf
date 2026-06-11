resource "kubernetes_resource_quota" "app_team" {
  metadata {
    name      = "app-team-quota"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  spec {
    hard = {
      "requests.cpu"    = "2"
      "requests.memory" = "2Gi"
      "limits.cpu"      = "4"
      "limits.memory"   = "4Gi"
      "pods"            = "20"
      "services"        = "10"
    }
  }
}

resource "kubernetes_limit_range" "app_team" {
  metadata {
    name      = "app-team-limits"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  spec {
    limit {
      type = "Container"
      default = {
        cpu    = "200m"
        memory = "256Mi"
      }
      default_request = {
        cpu    = "100m"
        memory = "128Mi"
      }
      max = {
        cpu    = "1"
        memory = "1Gi"
      }
      min = {
        cpu    = "50m"
        memory = "32Mi"
      }
    }
  }
}
