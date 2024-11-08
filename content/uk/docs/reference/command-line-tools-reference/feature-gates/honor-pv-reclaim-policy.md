---
title: HonorPVReclaimPolicy
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.23"
    toVersion: "1.30"
  - stage: beta
    defaultValue: true
    fromVersion: "1.31"
---
Дотримуватися політики відновлення постійного тому, коли він має значення `Delete`, незалежно від впорядкування видалення PV-PVC. Докладніші відомості наведено у документації [Завершувач захисту від видалення постійних томів](/uk/docs/concepts/storage/persistent-volumes/#persistentvolume-deletion-protection-finalizer).
