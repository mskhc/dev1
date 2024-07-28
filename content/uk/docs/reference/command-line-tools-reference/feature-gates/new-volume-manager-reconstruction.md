---
title: NewVolumeManagerReconstruction
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: beta
    defaultValue: false
    fromVersion: "1.27"
    toVersion: "1.27"
  - stage: beta
    defaultValue: true
    fromVersion: "1.28"
    toVersion: "1.29"
  - stage: stable
    defaultValue: true
    fromVersion: "1.30"
---
Дозволяє покращити виявлення змонтованих томів під час запуску kubelet. Оскільки відповідний код було суттєво перероблено, у версіях Kubernetes від 1.25 до 1.29 можна було вимкнути цю функцію у випадку, якщо kubelet застряг під час запуску або не розмонтував томи з завершених Podʼів.

Цей рефакторинг лежав в основі функції `SELinuxMountReadWriteOncePod` у версіях Kubernetes 1.25 та 1.26.