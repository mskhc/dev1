---
title: NetworkPolicyStatus
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.24"
    toVersion: "1.27"

removed: true
---
Вмикає субресурс `status` для обʼєктів NetworkPolicy.