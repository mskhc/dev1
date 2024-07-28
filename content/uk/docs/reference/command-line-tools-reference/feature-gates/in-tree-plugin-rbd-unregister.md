---
title: InTreePluginRBDUnregister
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.23"
    toVersion: "1.27"
  - stage: deprecated
    defaultValue: false
    fromVersion: "1.28"  
---
Припиняє реєстрацію вбудованого втулка RBD у kubelet та контролерах томів.
