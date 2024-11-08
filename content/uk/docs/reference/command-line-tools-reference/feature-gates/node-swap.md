---
title: NodeSwap
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.22"
    toVersion: "1.27"
  - stage: beta
    defaultValue: false
    fromVersion: "1.28"
    toVersion: "1.29"
  - stage: beta
    defaultValue: true
    fromVersion: "1.30"
---
Дозволяє kubelet виділяти памʼять підкачки для робочих навантажень Kubernetes на вузлі. Має використовуватися з `KubeletConfiguration.failSwapOn`, встановленим у false. За більш детальною інформацією зверніться до [swap memory](/uk/docs/concepts/architecture/nodes/#swap-memory)
