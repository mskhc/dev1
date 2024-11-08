---
title: CSIMigrationPortworx
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.23"
    toVersion: "1.24"
  - stage: beta
    defaultValue: false
    fromVersion: "1.25"
---
Вмикає shimʼи та логіку передачі для маршрутизації операцій тому з вбудованого втулка Portworx до втулка Portworx CSI. Вимагає встановлення та налаштування втулка Portworx CSI в кластері.
