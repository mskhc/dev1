---
title: InTreePluginOpenStackUnregister
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.21"
---
Припиняє реєстрацію вбудованого втулка OpenStack cinder у kubelet та контролерах томів.
