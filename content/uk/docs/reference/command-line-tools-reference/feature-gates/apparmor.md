---
title: AppArmor
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: beta
    defaultValue: true
    fromVersion: "1.4"
---
Вмикає використання примусового контролю доступу AppArmor для Podʼів, що працюють на вузлах Linux. Докладнішу інформацію наведено у [Посібнику з AppArmor](/docs/tutorials/security/apparmor/).
