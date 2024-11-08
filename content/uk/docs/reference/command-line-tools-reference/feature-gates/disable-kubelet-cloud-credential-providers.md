---
title: DisableKubeletCloudCredentialProviders
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.23"
    toVersion: "1.28"    
  - stage: beta 
    defaultValue: true
    fromVersion: "1.29"     
---
Вмикає вбудовану функціональність kubelet для автентифікації в реєстрі контейнерів хмарного постачальника для отримання облікових даних для отримання образів.
