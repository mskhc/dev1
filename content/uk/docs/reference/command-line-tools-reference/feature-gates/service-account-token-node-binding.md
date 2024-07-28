---
title: ServiceAccountTokenNodeBinding
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.29"
---
Контролює, чи дозволяє apiserver привʼязувати токени службових облікових записів до обʼєктів Node.
