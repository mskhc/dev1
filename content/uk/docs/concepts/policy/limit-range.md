---
reviewers:
- nelvadas
title: Обмеження діапазонів
api_metadata:
- apiVersion: "v1"
  kind: "LimitRange"
content_type: concept
weight: 10
---

<!-- overview -->

Типово контейнери запускаються з необмеженими [обчислювальними ресурсами](/docs/concepts/configuration/manage-resources-containers/) у кластері Kubernetes. Використовуючи [квоти ресурсів Kubernetes](/docs/concepts/policy/resource-quotas/), адміністратори (_оператори кластера_) можуть обмежити споживання та створення ресурсів кластера (таких як час ЦП, памʼять та постійне сховище) у визначеному {{< glossary_tooltip text="namespace" term_id="namespace" >}}. У межах простору імен Pod може використовувати стільки ЦП та памʼяті, скільки дозволяють ResourceQuotas, що застосовуються до цього простору імен. Як оператору кластера або адміністратору на рівні простору імен вам також може бути важливо переконатися, що один обʼєкт не може монополізувати всі доступні ресурси у просторі імен.

LimitRange — це політика обмеження виділення ресурсів (ліміти та запити), яку можна вказати для кожного відповідного типу обʼєкта (такого як Pod або {{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}}) у просторі імен.

<!-- body -->

_LimitRange_ надає обмеження, які можуть:

- Застосовувати мінімальні та максимальні витрати обчислювальних ресурсів на Pod або Контейнер у просторі імен.
- Застосовувати мінімальний та максимальний запит на сховище для {{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}} у просторі імен.
- Застосовувати співвідношення між запитом та лімітом для ресурсу у просторі імен.
- Встановлювати стандартний запит/ліміт для обчислювальних ресурсів у просторі імен та автоматично вставляти їх у контейнери під час виконання.

Обмеження діапазону діє в певному просторі імен, коли існує обʼєкт LimitRange у цьому просторі імен.

Назва обʼєкта LimitRange повинна бути дійсним [піддоменом DNS](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

## Обмеження на ліміти ресурсів та запити {#constraints-on-resource-limits-and-requests}

- Адміністратор створює обмеження діапазону у просторі імен.
- Користувачі створюють (або намагаються створити) обʼєкти у цьому просторі імен, такі як Podʼи або PersistentVolumeClaims.
- По-перше, контролер допуску LimitRange застосовує типове значення запиту та ліміту для всіх Podʼів (та їхніх контейнерів), які не встановлюють вимоги щодо обчислювальних ресурсів.
- По-друге, `LimitRange` відстежує використання, щоб забезпечити, що воно не перевищує мінімальне, максимальне та співвідношення ресурсів, визначених в будь-якому `LimitRange`, присутньому у просторі імен.
- Якщо ви намагаєтеся створити або оновити обʼєкт (Pod або PersistentVolumeClaim), який порушує обмеження `LimitRange`, ваш запит до сервера API буде відхилено з HTTP-кодом стану `403 Forbidden` та повідомленням, що пояснює порушене обмеження.
- Якщо додати `LimitRange` в простір імен, який застосовується до обчислювальних ресурсів, таких як `cpu` та `memory`, необхідно вказати запити або ліміти для цих значень. В іншому випадку система може відхилити створення Podʼа.
- Перевірка `LimitRange` відбувається тільки на етапі надання дозволу Podʼу, а не на працюючих Podʼах. Якщо ви додаєте або змінюєте `LimitRange`, Podʼи, які вже існують у цьому просторі імен, залишаються без змін.
- Якщо у просторі імен існує два або більше обʼєкти `LimitRange`, то не визначено, яке типове значення буде застосовано.

## LimitRange та перевірки допуску для Podʼів {#limitrange-and-admission-checks-for-pods}

`LimitRange` **не** перевіряє типово послідовність застосованих значень. Це означає, що стандартні значення для _limit_, встановлене `LimitRange`, може бути меншим за значення _request_, вказане для контейнера в специфікації, яку клієнт надсилає на сервер API. Якщо це станеться, Pod не буде запланованим.

Наприклад, ви визначаєте `LimitRange` цим маніфестом:

{{% code_sample file="concepts/policy/limit-range/problematic-limit-range.yaml" %}}

разом з Podʼом, який вказує на запит ресурсу ЦП `700m`, але не на ліміт:

{{% code_sample file="concepts/policy/limit-range/example-conflict-with-limitrange-cpu.yaml" %}}

тоді цей Pod не буде запланованим, і він відмовиться з помилкою, схожою на:

```none
Pod "example-conflict-with-limitrange-cpu" is invalid: spec.containers[0].resources.requests: Invalid value: "700m": must be less than or equal to cpu limit
```

Якщо ви встановите як `request`, так і `limit`, то цей новий Pod буде успішно запланований, навіть з тим самим `LimitRange`:

{{% code_sample file="concepts/policy/limit-range/example-no-conflict-with-limitrange-cpu.yaml" %}}

## Приклади обмежень ресурсів {#example-resource-constraints}

Приклади політик, які можна створити за допомогою `LimitRange`, такі:

- У кластері з 2 вузлами з місткістю 8 ГБ ОЗП та 16 ядрами обмежте Podʼи в просторі імен на роботу з 100m CPU з максимальним лімітом 500m для CPU та запит 200Mi для памʼяті з максимальним лімітом 600Mi для памʼяті.
- Визначте стандартний ліміт та запит CPU на 150m та стандартний запит памʼяті на 300Mi для контейнерів, що запускаються без запитів ЦП та памʼяті у своїх специфікаціях.

У випадку, коли загальні ліміти простору імен менше суми лімітів Podʼів/Контейнерів, може виникнути конфлікт для ресурсів. У цьому випадку контейнери або Podʼи не будуть створені.

Ні конфлікт, ні зміни LimitRange не впливають на вже створені ресурси.

## {{% heading "whatsnext" %}}

Для прикладів використання обмежень дивіться:

- [як налаштувати мінімальні та максимальні обмеження CPU на простір імен](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/).
- [як налаштувати мінімальні та максимальні обмеження памʼяті на простір імен](/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/).
- [як налаштувати стандартні запити та ліміти CPU на простір імен](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/).
- [як налаштувати стандартні запити та ліміти памʼяті на простір імен](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/).
- [як налаштувати мінімальні та максимальні обмеження використання сховища на простір імен](/docs/tasks/administer-cluster/limit-storage-consumption/#limitrange-to-limit-requests-for-storage).
- [детальний приклад налаштування квот на простір імен](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/).

Звертайтеся до [документа проєкту LimitRanger](https://git.k8s.io/design-proposals-archive/resource-management/admission_control_limit_range.md) для контексту та історичної інформації.