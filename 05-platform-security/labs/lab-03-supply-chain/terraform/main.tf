terraform {
  required_version = ">= 1.5"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.13"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = var.kube_context
}

provider "helm" {
  kubernetes {
    config_path    = "~/.kube/config"
    config_context = var.kube_context
  }
}

resource "kubernetes_namespace" "supply_chain" {
  metadata {
    name = "supply-chain"
    labels = {
      "pod-security.kubernetes.io/enforce" = "restricted"
      "lab"                                = "03-supply-chain"
    }
  }
}

resource "helm_release" "kyverno" {
  name             = "kyverno"
  repository       = "https://kyverno.github.io/kyverno/"
  chart            = "kyverno"
  namespace        = "kyverno"
  create_namespace = true
  version          = "3.2.0"

  set {
    name  = "replicaCount"
    value = "1"
  }
}

resource "kubernetes_secret" "cosign_pub" {
  metadata {
    name      = "cosign-pub-key"
    namespace = "supply-chain"
  }

  data = {
    "cosign.pub" = file("${path.module}/../cosign.pub")
  }

  depends_on = [kubernetes_namespace.supply_chain]
}
