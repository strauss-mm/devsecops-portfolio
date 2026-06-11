resource "kubernetes_manifest" "verify_images_policy" {
  depends_on = [helm_release.kyverno]

  manifest = {
    apiVersion = "kyverno.io/v1"
    kind       = "ClusterPolicy"
    metadata = {
      name = "verify-image-signatures"
      annotations = {
        "policies.kyverno.io/title"       = "Verify Image Signatures"
        "policies.kyverno.io/category"    = "Supply Chain Security"
        "policies.kyverno.io/severity"    = "high"
        "policies.kyverno.io/description" = "Only allow images that have been signed with our cosign key."
      }
    }
    spec = {
      validationFailureAction = "Enforce"
      background              = true
      rules = [
        {
          name = "verify-signature"
          match = {
            any = [
              {
                resources = {
                  kinds      = ["Pod"]
                  namespaces = ["supply-chain"]
                }
              }
            ]
          }
          verifyImages = [
            {
              imageReferences = ["lab03-app:*"]
              attestors = [
                {
                  count = 1
                  entries = [
                    {
                      keys = {
                        publicKeys = "cosign.pub"
                        secret = {
                          name      = "cosign-pub-key"
                          namespace = "supply-chain"
                        }
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
