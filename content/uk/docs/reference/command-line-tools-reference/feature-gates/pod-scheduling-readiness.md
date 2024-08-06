---
title: PodSchedulingReadiness
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
    toVersion: "1.29"
  - stage: stable
    defaultValue: true
    fromVersion: "1.30"
---
Дозволяє встановлювати поле `SchedulingGates` для керування [готовністю до виселення за розкладом] (/docs/concepts/scheduling-eviction/pod-scheduling-readiness).