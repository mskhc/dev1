---
title: JobPodFailurePolicy
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.25"
    toVersion: "1.25"
  - stage: beta
    defaultValue: true
    fromVersion: "1.26"
---
Дозволяє користувачам визначати обробку несправностей контейнерів на основі кодів виходу з контейнера та стану контейнерів.