---
title: Контейнери
weight: 40
description: Технологія для упаковки застосунку разом з його залежностями оточення виконання.
reviewers:
- erictune
- thockin
content_type: concept
card:
  name: concepts
  weight: 50
---

<!-- overview -->

Кожен контейнер, який ви запускаєте, є повторюваним; стандартизація завдяки включеним залежностям означає, що ви отримуєте однакову поведінку, де б ви його не запускали.

Контейнери відокремлюють застосунки від базової інфраструктури хоста Це полегшує розгортання в різних хмарних або ОС-середовищах.

Кожен {{< glossary_tooltip text="вузол" term_id="node" >}} в кластері Kubernetes запускає контейнери, які формують
[Podʼи](/docs/concepts/workloads/pods/), призначені цьому вузлу. Контейнери розташовуються та плануються разом, щоб запускатися на тому ж вузлі.

<!-- body -->

## Образи контейнерів {#container-images}

[Образ контейнера](/docs/concepts/containers/images/) — це готовий до запуску пакунок програмного забезпечення, який містить все необхідне для запуску застосунку: код та будь-яке середовище виконання, яке він вимагає, бібліотеки застосунку та системи, та типові значення для будь-яких важливих налаштувань.

Контейнери призначені для того, щоб бути stateless та [незмінними](https://glossary.cncf.io/immutable-infrastructure/): ви не повинні змінювати код контейнера, який вже працює. Якщо у вас є контейнеризований застосунок та ви хочете внести зміни, правильний процес полягає в тому, щоб побудувати новий образ, який включає зміни, а потім перебудувати контейнер, щоб запустити оновлений образ.

## Середовище виконання контейнерів {#container-runtimes}

{{< glossary_definition term_id="container-runtime" length="all" >}}

Зазвичай, ви можете дозволити вашому кластеру обрати стандартне середовище виконання для Podʼа. Якщо вам потрібно використовувати більше одного середовища виконання контейнерів у вашому кластері, ви можете вказати [RuntimeClass](/docs/concepts/containers/runtime-class/) для Podʼа, щоб переконатися, що Kubernetes запускає ці контейнери за допомогою певного середовища виконання.

Ви також можете використовувати RuntimeClass для запуску різних Podʼів з однаковим контейнером, але з різними налаштуваннями.