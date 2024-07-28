---
title: KubeletSeparateDiskGC
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.29"
---
Дозволити kubelet видаляти образи контейнерів та контейнери, навіть якщо вони знаходяться у окремій файловій системі.
