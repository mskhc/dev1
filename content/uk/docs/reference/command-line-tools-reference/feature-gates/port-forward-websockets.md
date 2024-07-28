---
title: PortForwardWebsockets
content_type: feature_gate
_build:
  list: never
  render: false

stages:
  - stage: alpha
    defaultValue: false
    fromVersion: "1.30"
---
Дозволити потокове передавання WebSocket підпротоколу portforward (`port-forward`) від клієнтів, які запитують версію v2 (`v2.portforward.k8s.io`) підпротоколу.
