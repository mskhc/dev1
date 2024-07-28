---
title: APIServerTracing
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.22"
    toVersion: "1.26"
  - stage: beta
    defaultValue: true
    fromVersion: "1.27"  
---
Додає підтримку розподіленого трасування у сервері API. Докладні відомості наведено у статті [Трасування системних компонентів Kubernetes](/docs/concepts/cluster-administration/system-traces).