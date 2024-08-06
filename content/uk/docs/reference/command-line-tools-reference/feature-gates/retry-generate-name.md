---
title: RetryGenerateName
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.30"
---

Дозволяє повторити спробу створення обʼєкта, коли очікується, що {{< glossary_tooltip text="API server" term_id="kube-apiserver" >}} створить [name](/docs/concepts/overview/working-with-objects/names/#names). Коли цю можливість увімкнено, запити з використанням `generateName` автоматично повторюються у випадку, якщо панель управління виявляє конфлікт імен з наявним обʼєктом, до обмеження у 8 спроб.