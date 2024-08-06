---
title: ServiceTrafficDistribution
content_type: feature_gate

_build:
  list: never
  render: false

stages:
- stage: alpha 
  defaultValue: false
  fromVersion: "1.30"
---
Дозволяє використовувати необовʼязкове поле `spec.trafficDistribution` у сервісах. У цьому полі можна вказати параметри розподілу трафіку між точками доступу Service.
