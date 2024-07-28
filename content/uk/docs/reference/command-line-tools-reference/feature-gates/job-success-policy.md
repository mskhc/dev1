---
title: JobSuccessPolicy
content_type: feature_gate

_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.30"
---
Дозволяє користувачам вказувати, коли Job може бути визнаний успішним на основі набору успішних Podʼів.
