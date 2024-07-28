---
title: ZeroLimitedNominalConcurrencyShares
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: beta 
    defaultValue: false
    fromVersion: "1.29"
---
Дозволити [Priority & Fairness](/docs/concepts/cluster-administration/flow-control/) на сервері API використовувати нульове значення для поля `nominalConcurrencyShares` секції `limited` рівня пріоритету.
