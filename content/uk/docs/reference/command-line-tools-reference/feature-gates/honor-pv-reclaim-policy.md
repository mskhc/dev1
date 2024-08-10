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
---
Дотримуватися політики відновлення постійного тому, коли він має значення `Delete`, незалежно від впорядкування видалення PV-PVC. Докладніші відомості наведено у документації [Фіналізатор захисту від видалення постійних томів](/uk/docs/concepts/storage/persistent-volumes/#persistentvolume-deletion-protection-finalizer).
