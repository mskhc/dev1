---
title: MatchLabelKeysInPodTopologySpread
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.25"
    toVersion: "1.26"
  - stage: beta
    defaultValue: true
    fromVersion: "1.27"
---
Вмикає поле `matchLabelKeys` для [Обмеження поширення топології Podʼів](/docs/concepts/scheduling-eviction/topology-spread-constraints/).