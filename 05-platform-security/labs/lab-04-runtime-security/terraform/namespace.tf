resource "kubernetes_namespace" "lab_runtime" {
  metadata {
    name = "lab-runtime"
    labels = {
      "lab" = "04-runtime-security"
    }
  }
}

resource "kubernetes_deployment" "target_app" {
  metadata {
    name      = "target-app"
    namespace = kubernetes_namespace.lab_runtime.metadata[0].name
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "target-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "target-app"
        }
      }
      spec {
        container {
          name  = "app"
          image = "ubuntu:22.04"
          command = ["/bin/bash", "-c", "apt-get update && apt-get install -y curl netcat-openbsd && sleep infinity"]

          resources {
            limits = {
              memory = "256Mi"
              cpu    = "200m"
            }
          }
        }
      }
    }
  }
}
