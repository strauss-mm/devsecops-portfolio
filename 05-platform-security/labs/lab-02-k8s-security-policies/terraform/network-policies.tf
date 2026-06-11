resource "kubernetes_network_policy" "default_deny_app_team" {
  metadata {
    name      = "default-deny-all"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  spec {
    pod_selector {}
    policy_types = ["Ingress", "Egress"]
  }
}

resource "kubernetes_network_policy" "default_deny_database" {
  metadata {
    name      = "default-deny-all"
    namespace = kubernetes_namespace.database.metadata[0].name
  }

  spec {
    pod_selector {}
    policy_types = ["Ingress", "Egress"]
  }
}

resource "kubernetes_network_policy" "allow_frontend_to_backend" {
  metadata {
    name      = "allow-frontend-to-backend"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  spec {
    pod_selector {
      match_labels = {
        role = "backend"
      }
    }

    ingress {
      from {
        pod_selector {
          match_labels = {
            role = "frontend"
          }
        }
      }
      ports {
        port     = "8080"
        protocol = "TCP"
      }
    }

    policy_types = ["Ingress"]
  }
}

resource "kubernetes_network_policy" "allow_backend_to_database" {
  metadata {
    name      = "allow-backend-to-db"
    namespace = kubernetes_namespace.database.metadata[0].name
  }

  spec {
    pod_selector {
      match_labels = {
        role = "database"
      }
    }

    ingress {
      from {
        namespace_selector {
          match_labels = {
            "lab" = "02-k8s-security"
          }
        }
        pod_selector {
          match_labels = {
            role = "backend"
          }
        }
      }
      ports {
        port     = "5432"
        protocol = "TCP"
      }
    }

    policy_types = ["Ingress"]
  }
}

resource "kubernetes_network_policy" "allow_dns_egress" {
  metadata {
    name      = "allow-dns-egress"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  spec {
    pod_selector {}

    egress {
      to {
        namespace_selector {
          match_labels = {
            "kubernetes.io/metadata.name" = "kube-system"
          }
        }
      }
      ports {
        port     = "53"
        protocol = "UDP"
      }
      ports {
        port     = "53"
        protocol = "TCP"
      }
    }

    policy_types = ["Egress"]
  }
}
