---
title: JobBackoffLimitPerIndex
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
Дозволяє вказати максимальну кількість повторних спроб для кожного індексу в проіндексованих завданнях.
