resource "kubernetes_service_account" "developer" {
  metadata {
    name      = "developer"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }
}

resource "kubernetes_service_account" "deployer" {
  metadata {
    name      = "deployer"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }
}

resource "kubernetes_service_account" "security_auditor" {
  metadata {
    name      = "security-auditor"
    namespace = "default"
  }
}

# Developer: read pods/logs/exec in app-team, NO secrets
resource "kubernetes_role" "developer" {
  metadata {
    name      = "developer"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  rule {
    api_groups = [""]
    resources  = ["pods", "pods/log", "services", "configmaps"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = [""]
    resources  = ["pods/exec"]
    verbs      = ["create"]
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments", "replicasets"]
    verbs      = ["get", "list", "watch"]
  }
}

resource "kubernetes_role_binding" "developer" {
  metadata {
    name      = "developer"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.developer.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.developer.metadata[0].name
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }
}

# Deployer: create/update deployments, NO RBAC or secrets
resource "kubernetes_role" "deployer" {
  metadata {
    name      = "deployer"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments"]
    verbs      = ["get", "list", "watch", "create", "update", "patch"]
  }

  rule {
    api_groups = [""]
    resources  = ["services", "configmaps"]
    verbs      = ["get", "list", "create", "update"]
  }

  rule {
    api_groups = [""]
    resources  = ["pods"]
    verbs      = ["get", "list", "watch"]
  }
}

resource "kubernetes_role_binding" "deployer" {
  metadata {
    name      = "deployer"
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.deployer.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.deployer.metadata[0].name
    namespace = kubernetes_namespace.app_team.metadata[0].name
  }
}

# Security Auditor: cluster-wide read-only
resource "kubernetes_cluster_role" "security_auditor" {
  metadata {
    name = "security-auditor"
  }

  rule {
    api_groups = ["", "apps", "batch", "networking.k8s.io", "rbac.authorization.k8s.io"]
    resources  = ["*"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = ["policy"]
    resources  = ["podsecuritypolicies", "poddisruptionbudgets"]
    verbs      = ["get", "list", "watch"]
  }
}

resource "kubernetes_cluster_role_binding" "security_auditor" {
  metadata {
    name = "security-auditor"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.security_auditor.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.security_auditor.metadata[0].name
    namespace = "default"
  }
}
