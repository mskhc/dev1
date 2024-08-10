---
title: StatefulSetStartOrdinal
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.26"
    toVersion: "1.26"
  - stage: beta
    defaultValue: true
    fromVersion: "1.27"
---
Дозволити налаштування порядкового номера старту у StatefulSet. Дивіться [Start ordinal](/uk/docs/concepts/workloads/controllers/statefulset/#start-ordinal) для більш детальної інформації.
