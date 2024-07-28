---
title: PersistentVolumeLastPhaseTransitionTime
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.28"
    toVersion: "1.28"
  - stage: beta
    defaultValue: true
    fromVersion: "1.29"
---
Додає нове поле до PersistentVolume, яке містить мітку часу, коли том востаннє змінював свою фазу.