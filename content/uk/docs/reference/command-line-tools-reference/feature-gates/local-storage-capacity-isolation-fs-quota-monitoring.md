---
title: LocalStorageCapacityIsolationFSQuotaMonitoring
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.15"
---
Якщо `LocalStorageCapacityIsolation` увімкнено для [локального ефемерного сховища](/docs/concepts/configuration/manage-resources-containers/) і резервна файлова система для [томів emptyDir](/docs/concepts/storage/volumes/#emptydir) підтримує квоти проєктів і їх увімкнено, використовуйте квоти проєктів для моніторингу споживання місця у сховищі [emptyDir volume](/docs/concepts/storage/volumes/#emptydir), а не обхід файлової системи для кращої продуктивності і точності.
