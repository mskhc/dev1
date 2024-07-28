---
reviewers:
- erictune
- foxish
- davidopp
title: Розлади
content_type: concept
weight: 70
---

<!-- overview -->
Цей посібник призначений для власників застосунків, які хочуть створити високодоступні застосунки та, таким чином, повинні розуміти, які типи розладів можуть трапитися з Podʼами.

Також це стосується адміністраторів кластера, які хочуть виконувати автоматизовані дії з кластером, такі як оновлення та автомасштабування кластерів.

<!-- body -->

## Добровільні та невідворотні розлади {#voluntary-and-involuntary-disruptions}

Podʼи не зникають, поки хтось (людина або контролер) не знищить їх, або не трапиться невідворотна помилка обладнання чи системного програмного забезпечення.

Ми називаємо ці невідворотні випадки *невідворотними розладами* застосунку. Приклади:

- відмова обладнання фізичної машини, яка підтримує вузол
- адміністратор кластера видаляє віртуальну машину (екземпляр) помилково
- відмова хмарного провайдера або гіпервізора призводить до зникнення віртуальної машини
- kernel panic
- вузол зникає з кластера через поділ мережі кластера
- виселення Podʼу через [вичерпання ресурсів](/docs/concepts/scheduling-eviction/node-pressure-eviction/) вузла.

Крім умов, повʼязаних із вичерпанням ресурсів, всі ці умови повинні бути знайомими більшості користувачів; вони не є специфічними для Kubernetes.

Ми називаємо інші випадки *добровільними розладами*. До них належать як дії, ініційовані власником застосунку, так і ті, які ініціює адміністратор кластера. Типові дії власника застосунку включають:

- видалення розгортання або іншого контролера, який управляє Podʼом
- оновлення шаблону розгортання Podʼа, що призводить до перезапуску
- безпосереднє видалення Podʼу (наприклад, випадково)

Дії адміністратора кластера включають:

- [Виведення вузла](/docs/tasks/administer-cluster/safely-drain-node/) для ремонту чи оновлення.
- Виведення вузла з кластера для зменшення масштабу кластера (дізнайтеся більше про [автомасштабування кластера](https://github.com/kubernetes/autoscaler/#readme)).
- Видалення Podʼа з вузла, щоб щось інше помістилося на цей вузол.

Ці дії можуть бути виконані безпосередньо адміністратором кластера чи за допомогою автоматизації, запущеної адміністратором кластера, або вашим провайдером хостингу кластера.

Зверніться до адміністратора кластера або проконсультуйтеся з документацією вашого хмарного провайдера або дистрибутиву, щоб визначити, чи увімкнено які-небудь джерела добровільних розладів для вашого кластера. Якщо жодне з них не увімкнено, ви можете пропустити створення бюджетів розладів Podʼів (Pod Disruption Budget).

{{< caution >}}
Не всі добровільні розлади обмежені бюджетами розладів Podʼів. Наприклад, видалення Deployment чи Pod обходить бюджети розладів Podʼів.
{{< /caution >}}

## Управління розладами {#dealing-with-disruptions}

Ось кілька способів помʼякшення невідворотних розладів:

- Переконайтеся, що ваш Pod [звертається по необхідні ресурси](/docs/tasks/configure-pod-container/assign-memory-resource).
- Реплікуйте своє застосунки, якщо вам потрібна вища доступність. (Дізнайтеся про запуск реплікованих [stateless](/docs/tasks/run-application/run-stateless-application-deployment/) та [stateful](/docs/tasks/run-application/run-replicated-stateful-application/) застосунків.)
- Для ще більшої доступності при запуску реплікованих застосунків розподіліть їх по стійках (за допомогою [anti-affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)) чи по зонах (якщо використовуєте
  [кластер з кількома зонами](/docs/setup/multiple-zones).)

Частота добровільних розладів різниться. На базовому кластері Kubernetes немає автоматизованих добровільних розладів (тільки ті, які ініціює користувач). Однак адміністратор кластера або постачальник хостингу може запускати деякі додаткові служби, які призводять до добровільних розладів. Наприклад, розгортання оновлень програмного забезпечення вузла може призвести до добровільних розладів. Також деякі реалізації автомасштабування кластера (вузла) можуть призводити до добровільних розладів для дефрагментації та ущільнення вузлів. Адміністратор кластера або постачальник хостингу повинні документувати, на якому рівні добровільних розладів, якщо такі є, можна розраховувати.
Деякі параметри конфігурації, такі як [використання PriorityClasses](/docs/concepts/scheduling-eviction/pod-priority-preemption/) у вашій специфікації Podʼу, також можуть призводити до добровільних (і невідворотних) розладів.

## Бюджет розладів Podʼів {#pod-disruption-budgets}

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

Kubernetes пропонує функції, що допомагають запускати застосунки з високою доступністю навіть тоді, коли ви вводите часті добровільні розлади.

Як власник застосунку, ви можете створити Бюджет розладів Podʼів (PodDisruptionBudget або PDB) для кожного застосунку. PDB обмежує кількість Podʼів, які можуть бути одночасно вимкнені через добровільні розлади для реплікованого застосунку. Наприклад, застосунок, який працює на основі кворуму, хоче забезпечити, що кількість реплік ніколи не знизиться нижче необхідної для кворуму. Вебінтерфейс, наприклад, може бажати забезпечити, що кількість реплік, які обслуговують навантаження, ніколи не падатиме нижче певного відсотка від загальної кількості.

Менеджери кластерів та постачальники хостингу повинні використовувати інструменти, які дотримуються бюджетів розладів Podʼів, викликаючи [Eviction API](/docs/tasks/administer-cluster/safely-drain-node/#eviction-api) замість прямого видалення Podʼу або Deployment.

Наприклад, команда `kubectl drain` дозволяє вам позначити вузол, як виводиться з експлуатації. Коли ви виконуєте `kubectl drain`, інструмент намагається витіснити всі Podʼи з вузла, який ви виводите з експлуатації. Запит на виселення, який `kubectl` робить від вашого імені, може тимчасово бути відхилено, тому інструмент періодично повторює всі невдалі запити, поки всі Podʼи на цільовому вузлі не будуть завершені, або досягне вказаного тайм-ауту.

PDB визначає кількість реплік, які застосунок може терпіти, порівняно з тим, скільки він має намір мати. Наприклад, Deployment, який має `.spec.replicas: 5`, повинен мати 5 Podʼів в будь-який момент часу. Якщо PDB дозволяє бути 4 Podʼам одночасно, то Eviction API дозволить добровільне відключення одного (але не двох) Podʼів одночасно.

Група Podʼів, з яких складається застосунок, визначається за допомогою селектора міток, такого самого, як і той, який використовується контролером застосунку (deployment, stateful-set і т. д.).

"Очікувана" кількість Podʼів обчислюється з `.spec.replicas` ресурсу робочого навантаження (Workload), який управляє цими Podʼами. Панель управління визначає ресурс робочого навантаження, оглядаючи `.metadata.ownerReferences` Podʼа.

[Невідворотні розлади](#voluntary-and-involuntary-disruptions) не можуть бути усунуті за допомогою PDB; однак вони враховуються в бюджеті.

Podʼи, які видаляються або недоступні через поетапне оновлення застосунку, дійсно враховуються в бюджеті розладів, але ресурси робочого навантаження (такі як Deployment і StatefulSet) не обмежуються PDB під час поетапного оновлення. Замість цього обробка невдач під час оновлення застосунку конфігурується в специфікації конкретного ресурсу робочого навантаження.

Рекомендується встановлювати [політику виселення несправних Podʼів](/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy) `AlwaysAllow` у ваших PodDisruptionBudgets для підтримки виселення неправильно працюючих застосунків під час виведення вузла. Стандартна поведінка полягає в тому, що очікується, коли Podʼи застосунку стануть [справними](/docs/tasks/run-application/configure-pdb/#healthiness-of-a-pod) перед тим, як виведення може продовжитися.

Коли Pod виводиться за допомогою API виселення, він [завершується](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) відповідним чином, з урахуванням налаштувань `terminationGracePeriodSeconds` його [PodSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core).

## Приклад бюджету розладів поди {#pdb-example}

Припустимо, що у кластері є 3 вузли: `node-1` до `node-3`.
Кластер виконує кілька застосунків. Один з них має 3 репліки, які спочатку називаються `pod-a`, `pod-b` і `pod-c`. Інший, неповʼязаний з ними Pod без PDB, називається `pod-x`. Спочатку Podʼи розташовані наступним чином:

|       node-1         |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| pod-a  *доступний*   | pod-b *доступний*   | pod-c *доступний*  |
| pod-x  *доступний*   |                     |                    |

Усі 3 Podʼи є частиною Deployment, і вони разом мають PDB, який вимагає, щоб одночасно було доступними принаймні 2 з 3 Podʼів.

Наприклад, припустимо, що адміністратор кластера хоче запровадити нову версію ядра ОС, щоб виправити помилку в ядрі. Адміністратор кластера спочатку намагається вивести з експлуатації `node-1` за допомогою команди `kubectl drain`. Цей інструмент намагається витіснити `pod-a` і `pod-x`. Це відбувається миттєво. Обидві Podʼа одночасно переходять в стан `terminating`. Це переводить кластер у стан:

|   node-1 *draining*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| pod-a  *terminating* | pod-b *available*   | pod-c *available*  |
| pod-x  *terminating* |                     |                    |

Deployment помічає, що один з Podʼів виводиться, тому він створює заміну під назвою `pod-d`. Оскільки `node-1` закритий, він опиняється на іншому вузлі. Також, щось створило `pod-y` як заміну для `pod-x`.

(Примітка: для StatefulSet, `pod-a`, який міг би мати назву щось на зразок `pod-0`, повинен був би повністю завершити свою роботу,
перш ніж його заміна, яка також має назву `pod-0`, але має інший UID, може бути створений. В іншому випадку приклад застосовується і до StatefulSet.)

Тепер кластер перебуває у такому стані:

|   node-1 *draining*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| pod-a  *terminating* | pod-b *available*   | pod-c *available*  |
| pod-x  *terminating* | pod-d *starting*    | pod-y              |

У якийсь момент Podʼи завершують свою роботу, і кластер виглядає так:

|    node-1 *drained*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
|                      | pod-b *available*   | pod-c *available*  |
|                      | pod-d *starting*    | pod-y              |

На цьому етапі, якщо нетерплячий адміністратор кластера намагається вивести з експлуатації `node-2` або `node-3`, команда виведення буде блокуватися, оскільки доступно тільки 2 Podʼи для Deployment, і його PDB вимагає принаймні 2. Після того, як пройде певний час, `pod-d` стає доступним.

Тепер стан кластера виглядає так:

|    node-1 *drained*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
|                      | pod-b *available*   | pod-c *available*  |
|                      | pod-d *available*   | pod-y              |

Тепер адміністратор кластера намагається вивести з експлуатації `node-2`. Команда drain спробує виселити два Podʼи у деякому порядку, скажімо, спочатку `pod-b`, а потім `pod-d`. Їй вдасться витіснити `pod-b`. Але, коли вона спробує витіснити `pod-d`, отримає відмову через те, що це залишить тільки один доступний Pod для Deployment.

Deployment створює заміну для `pod-b` з назвою `pod-e`. Оскільки в кластері недостатньо ресурсів для планування `pod-e`, виведення знову буде заблоковано. Кластер може опинитися в такому стані:

|    node-1 *drained*  |       node-2        |       node-3       | *no node*          |
|:--------------------:|:-------------------:|:------------------:|:------------------:|
|                      | pod-b *terminating* | pod-c *available*  | pod-e *pending*    |
|                      | pod-d *available*   | pod-y              |                    |

На цьому етапі адміністратор кластера повинен додати вузол назад до кластера, щоб продовжити оновлення.

Ви можете побачити, як Kubernetes змінює частоту випадків розладів відповідно до:

- скільки реплік потрібно для застосунку
- скільки часу потрібно для відповідного вимикання екземпляра
- скільки часу потрібно для запуску нового екземпляра
- типу контролера
- ресурсів кластера

## Умови розладу поду {#pod-disruption-conditions}

{{< feature-state for_k8s_version="v1.26" state="beta" >}}

{{< note >}}
Для використання цієї функціональності слід увімкнути [feature gate](/docs/reference/command-line-tools-reference/feature-gates/)  `PodDisruptionConditions` у вашому кластері.
{{< /note >}}

При увімкненні цієї функціональності для Podʼу додається окрема умова `DisruptionTarget` [condition](/docs/concepts/workloads/pods/pod-lifecycle/#pod-conditions), яка вказує, що Pod має бути видалений через {{<glossary_tooltip term_id="disruption" text="розлад">}}. Поле `reason` умови додатково вказує на одну з наступних причин завершення роботи Podʼу:

`PreemptionByScheduler`
: Pod має бути {{<glossary_tooltip term_id="preemption" text="випереджений">}} планувальником для надання місця новому Podʼу з вищим пріоритетом. Докладніше дивіться [Випередження за пріоритетом Podʼу](/docs/concepts/scheduling-eviction/pod-priority-preemption/).

`DeletionByTaintManager`
: Pod має бути видалений Менеджером Taint (який є частиною контролера життєвого циклу вузла в `kube-controller-manager`) через `NoExecute` taint, який Pod не толерує; див. виселення на основі {{<glossary_tooltip term_id="taint" text="taint">}}.

`EvictionByEvictionAPI`
: Pod був позначений для {{<glossary_tooltip term_id="api-eviction" text="виселення за допомогою Kubernetes API">}}.

`DeletionByPodGC`
: Pod, який повʼязаний із вузлом, якого вже не існує, має бути видалений за допомогою [збирання сміття Podʼів](/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection).

`TerminationByKubelet`
: Pod був примусово завершений kubelet, через {{<glossary_tooltip term_id="node-pressure-eviction" text="виселення через тиск вузла">}} або [відповідне вимикання вузла](/docs/concepts/architecture/nodes/#graceful-node-shutdown).

{{< note >}}
Розлад Podʼу може бути перерваний. Панель управління може повторно намагатися продовжити розлад того ж Podʼу, але це не гарантується. У результаті умова `DisruptionTarget` може бути додана до Podʼу, але цей Pod може фактично не бути видалений. У такій ситуації після певного часу умова розладу Pod буде видалена.
{{< /note >}}

При увімкненні функціональності `PodDisruptionConditions` разом із видаленням Podʼів, збирач сміття подів (PodGC) також відзначатиме їх як неуспішні, якщо вони знаходяться в не фазі завершення роботи (див. також [Збирання сміття Podʼів](/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection)).

При використанні Job (або CronJob) вам може знадобитися використовувати ці умови розладу Podʼу як частину політики невдачі вашого Job [Політики невдачі Podʼу](/docs/concepts/workloads/controllers/job#pod-failure-policy).

## Розділення ролей власника кластера та власника застосунку {#Separating-cluster-owner-and-application-owner-roles}

Часто корисно розглядати Менеджера кластера і Власника застосунку як окремі ролі з обмеженим знанням одне про одного. Це розділення обовʼязків може мати сенс у таких сценаріях:

- коли багато команд розробки застосунків використовують спільний кластер Kubernetes і є природна спеціалізація ролей
- коли використовуються інструменти або сервіси сторонніх розробників для автоматизації управління кластером

Бюджети розладу Podʼів підтримують це розділення ролей, надаючи
інтерфейс між цими ролями.

Якщо у вашій організації немає такого розділення обовʼязків,
вам може не знадобитися використовувати бюджети розладу Podʼів.

## Як виконати дії з розладу у вашому кластері {#how-to-perform-disruptive-actions-on-your-cluster}

Якщо ви є адміністратором кластера і вам потрібно виконати дію розладу на всіх вузлах вашого кластера, таку як оновлення вузла чи системного програмного забезпечення, ось кілька варіантів:

- Примиритись з періодом простою під час оновлення.
- Перемикнутися на іншу повну репліку кластера.
  - Відсутність простою, але може бути дорогою як для дубльованих вузлів, так і для зусиль людей для оркестрування перемикання.
- Розробляти застосунки, що терплять розлади, і використовувати бюджети розладу Podʼів.
  - Відсутність простою.
  - Мінімальне дублювання ресурсів.
  - Дозволяє більше автоматизації адміністрування кластера.
  - Написання застосунків, що терплять розлади, складне, але робота з підтримкою добровільних розладів в основному збігається з роботою з підтримкою автомасштабування і толеруючи інші типи рощладів розлади.

## {{% heading "whatsnext" %}}

- Слідкуйте за кроками для захисту вашого застосунку, [налаштовуючи бюджет розладу Podʼів](/docs/tasks/run-application/configure-pdb/).

- Дізнайтеся більше про [виведення вузлів з експлуатації](/docs/tasks/administer-cluster/safely-drain-node/).

- Дізнайтеся про [оновлення Deployment](/docs/concepts/workloads/controllers/deployment/#updating-a-deployment), включаючи кроки забезпечення його доступності під час впровадження.