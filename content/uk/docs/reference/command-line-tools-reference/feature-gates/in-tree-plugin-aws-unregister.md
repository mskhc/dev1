---
title: InTreePluginAWSUnregister
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.21"
---
Припиняє реєстрацію вбудованого втулка aws-ebs у kubelet та контролерах томів.
