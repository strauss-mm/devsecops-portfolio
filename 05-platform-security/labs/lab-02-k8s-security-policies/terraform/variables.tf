variable "kube_context" {
  description = "Kubernetes context to use"
  type        = string
  default     = "minikube"
}

variable "lab_name" {
  description = "Lab identifier for resource labeling"
  type        = string
  default     = "02-k8s-security"
}
