---
title: RecursiveReadOnlyMounts
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.30"
---
Вмикає підтримку рекурсивних монтувань лише для читання. Докладні відомості наведено у статті [монтування лише для читання](/uk/docs/concepts/storage/volumes/#read-only-mounts).
