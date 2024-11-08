---
title: DisableCloudProviders
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.22"
    toVersion: "1.28"
  - stage: beta 
    defaultValue: true
    fromVersion: "1.29"    
---
Вимикає будь-яку функціональність у `kube-apiserver`, `kube-controller-manager` та `kubelet`, повʼязаних з прапорцем компонента `--cloud-provider`. прапором компонента.
