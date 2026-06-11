resource "kubernetes_namespace" "falco_system" {
  metadata {
    name = "falco-system"
  }
}

resource "helm_release" "falco" {
  name       = "falco"
  repository = "https://falcosecurity.github.io/charts"
  chart      = "falco"
  namespace  = kubernetes_namespace.falco_system.metadata[0].name
  version    = "4.4.0"

  set {
    name  = "falcosidekick.enabled"
    value = "true"
  }

  set {
    name  = "falcosidekick.webui.enabled"
    value = "true"
  }

  set {
    name  = "driver.kind"
    value = "modern_ebpf"
  }

  set {
    name  = "collectors.docker.enabled"
    value = "false"
  }

  set {
    name  = "collectors.containerd.enabled"
    value = "true"
  }

  values = [
    yamlencode({
      customRules = {
        "custom-rules.yaml" = file("${path.module}/../falco-rules/custom-rules.yaml")
      }
    })
  ]
}

resource "helm_release" "falcosidekick" {
  name       = "falcosidekick"
  repository = "https://falcosecurity.github.io/charts"
  chart      = "falcosidekick"
  namespace  = kubernetes_namespace.falco_system.metadata[0].name
  version    = "0.8.0"

  set {
    name  = "config.webhook.address"
    value = "http://alert-receiver.falco-system:8080"
  }

  depends_on = [helm_release.falco]
}
