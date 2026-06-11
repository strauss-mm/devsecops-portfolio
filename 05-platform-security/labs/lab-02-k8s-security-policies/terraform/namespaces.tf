resource "kubernetes_namespace" "app_team" {
  metadata {
    name = "app-team"
    labels = {
      "pod-security.kubernetes.io/enforce" = "restricted"
      "pod-security.kubernetes.io/warn"    = "restricted"
      "pod-security.kubernetes.io/audit"   = "restricted"
      "lab"                                = "02-k8s-security"
    }
  }
}

resource "kubernetes_namespace" "database" {
  metadata {
    name = "database"
    labels = {
      "pod-security.kubernetes.io/enforce" = "restricted"
      "pod-security.kubernetes.io/warn"    = "restricted"
      "lab"                                = "02-k8s-security"
    }
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
    labels = {
      "pod-security.kubernetes.io/enforce" = "baseline"
      "pod-security.kubernetes.io/warn"    = "restricted"
      "lab"                                = "02-k8s-security"
    }
  }
}
