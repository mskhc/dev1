---
title: "Планування, Випередження та Виселення"
weight: 95
content_type: concept
description: >
  У Kubernetes планування означає забезпечення відповідності робочих навантажень (Pods) вузлам (Nodes), щоб kubelet міг їх запустити. Випередження — це процес припинення роботи Podʼів з низьким пріоритетом, щоб Podʼи з вищим пріоритетом могли розміщуватися на вузлах. Виселення — це процес проактивного припинення роботи одного або кількох Podʼів на вузлах з нестачею ресурсів.
no_list: true
---

У Kubernetes планування означає забезпечення відповідності {{< glossary_tooltip text="Podʼів" term_id="pod" >}} вузлам ({{< glossary_tooltip text="Nodes" term_id="node" >}}), щоб {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} міг їх запустити. Випередження — це процес припинення роботи Podʼів з низьким {{< glossary_tooltip text="пріоритетом" term_id="pod-priority" >}}, щоб Podʼи з вищим пріоритетом могли розміщуватися на вузлах. Виселення — це процес проактивного припинення роботи одного або кількох Podʼів на вузлах.

## Планування {#scheduling}

* [Планувальник Kubernetes](/uk/docs/concepts/scheduling-eviction/kube-scheduler/)
* [Призначення Podʼів вузлам](/uk/docs/concepts/scheduling-eviction/assign-pod-node/)
* [Витрати ресурсів на Pod](/uk/docs/concepts/scheduling-eviction/pod-overhead/)
* [Обмеження поширення топології Podʼів](/uk/docs/concepts/scheduling-eviction/topology-spread-constraints/)
* [Заплямованість та Толерантність](/uk/docs/concepts/scheduling-eviction/taint-and-toleration/)
* [Фреймворк планування](/uk/docs/concepts/scheduling-eviction/scheduling-framework)
* [Динамічне виділення ресурсів](/uk/docs/concepts/scheduling-eviction/dynamic-resource-allocation)
* [Налаштування продуктивності планувальника](/uk/docs/concepts/scheduling-eviction/scheduler-perf-tuning/)
* [Пакування ресурсів для розширених ресурсів](/uk/docs/concepts/scheduling-eviction/resource-bin-packing/)
* [Готовність планування Pod](/uk/docs/concepts/scheduling-eviction/pod-scheduling-readiness/)
* [Descheduler](https://github.com/kubernetes-sigs/descheduler#descheduler-for-kubernetes)

## Переривання роботи Podʼа {#pod-disruption}

{{<glossary_definition term_id="pod-disruption" length="all">}}

* [Пріоритет та Випередження Podʼів](/uk/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* [Виселення внаслідок тиску на вузол](/uk/docs/concepts/scheduling-eviction/node-pressure-eviction/)
* [Виселення, ініційоване API](/uk/docs/concepts/scheduling-eviction/api-eviction/)
