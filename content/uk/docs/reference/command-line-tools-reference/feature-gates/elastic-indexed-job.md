---
title: ElasticIndexedJob
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: beta
    defaultValue: true
    fromVersion: "1.27"
---
Дозволяє масштабувати індексовані завдання шляхом зміни параметрів `spec.completions` та `spec.parallelism` таким чином, щоб `spec.completions == spec.parallelism`. Детальніше див. у документації про [еластичні індексовані завдання](/uk/docs/concepts/workloads/controllers/job#elastic-indexed-jobs).
