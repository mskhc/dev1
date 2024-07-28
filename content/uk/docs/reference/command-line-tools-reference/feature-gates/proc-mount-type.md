---
title: ProcMountType
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.12"
---
Дозволяє керувати типом монтування proc для контейнерів, встановлюючи поле `procMount` у SecurityContext.
