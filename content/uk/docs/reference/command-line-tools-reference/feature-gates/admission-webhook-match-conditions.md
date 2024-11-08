---
title: AdmissionWebhookMatchConditions
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
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
Вмикає [умови збігу](/uk/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requestions-matchconditions) для модифікації та перевірки вебхуків допуску.
