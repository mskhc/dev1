---
title: CustomResourceFieldSelectors
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.30"  
---
Вмикає `selectableFields` в API {{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinition" >}}, щоб дозволити фільтрацію запитів **list**, **watch** та **deletecollection** для власних ресурсів.
