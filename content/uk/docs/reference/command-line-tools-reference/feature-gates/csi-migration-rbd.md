---
title: CSIMigrationRBD
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha 
    defaultValue: false
    fromVersion: "1.23"
    toVersion: "1.27"
  - stage: deprecated
    defaultValue: false
    fromVersion: "1.28"  
---
Вмикає shimʼи та логіку передачі для маршрутизації операцій тому з вбудованого втулка RBD до втулка Ceph RBD CSI. Вимагає увімкнення прапорця функції CSIMigration та встановлення та налаштування втулка Ceph CSI в кластері. Цей прапорець було відзначено як застарілий на користь прапорця функції `InTreePluginRBDUnregister`, який запобігає реєстрації вбудованого втулка RBD.
