---
api_metadata:
  apiVersion: "resource.k8s.io/v1alpha2"
  import: "k8s.io/api/resource/v1alpha2"
  kind: "ResourceClaim"
content_type: "api_reference"
description: "ResourceClaim описує які ресурси потрібні споживачу ресурсів."
title: "ResourceClaim v1alpha2"
weight: 15
auto_generated: false
---

`apiVersion: resource.k8s.io/v1alpha2`

`import "k8s.io/api/resource/v1alpha2"`

## ResourceClaim {#ResourceClaim}

ResourceClaim описує які ресурси потрібні споживачу ресурсів. Його статус вказує на те, чи були ресурси виділені та кому вони належать.

Це тип альфа-версії й вимагає увімкнення функціональної можливості DynamicResourceAllocation.

---

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClaim

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Стандартні метадані обʼєкта

- **spec** (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimSpec" >}}">ResourceClaimSpec</a>), обовʼязково

  Специфікація описує бажані атрибути ресурсу, який потім потрібно буде виділити. Її можна встановити лише один раз при створенні ResourceClaim.

- **status** (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimStatus" >}}">ResourceClaimStatus</a>)

  Статус описує, чи доступний ресурс та з якими атрибутами.

## ResourceClaimSpec {#ResourceClaimSpec}

ResourceClaimSpec визначає, як має бути виділений ресурс.

---

- **resourceClassName** (string), обовʼязково

  ResourceClassName посилається на драйвер та додаткові параметри через імʼя ResourceClass, яке було створено в рамках розгортання драйвера.

- **allocationMode** (string)

  Виділення може розпочатися негайно або коли Pod захоче використовувати ресурс. Стандартно використовується "WaitForFirstConsumer".

- **parametersRef** (ResourceClaimParametersReference)

  ParametersRef посилається на окремий обʼєкт із довільними параметрами, які будуть використані драйвером під час виділення ресурсу для запиту.

  Обʼєкт повинен знаходитися в тому ж самому просторі імен, що і ResourceClaim.

  <a name="ResourceClaimParametersReference"></a>
  *ResourceClaimParametersReference містить достатньо інформації, щоб дозволити знайти параметри для ResourceClaim. Обʼєкт повинен знаходитися в тому ж самому просторі імен, що і ResourceClaim.*

  - **parametersRef.kind** (string), обовʼязково

    Kind — це тип ресурсу, на який робиться посилання. Це те саме значення, що і в метаданих обʼєкта параметрів, наприклад "ConfigMap".

  - **parametersRef.name** (string), обовʼязково

    Name — це імʼя ресурсу, на який робиться посилання.

  - **parametersRef.apiGroup** (string)

    APIGroup — це група для ресурсу, на який робиться посилання. Вона порожня для основного API. Це відповідає групі в APIVersion, яка використовується під час створення ресурсів.

## ResourceClaimStatus {#ResourceClaimStatus}

ResourceClaimStatus відстежує, чи було виділено ресурс і які атрибути отримано в результаті.

---

- **allocation** (AllocationResult)

  Allocation встановлюється драйвером ресурсу, коли ресурс або набір ресурсів було успішно виділено. Якщо це поле не вказане, ресурси ще не були виділені.

  <a name="AllocationResult"></a>
  *AllocationResult містить атрибути виділеного ресурсу.*

  - **allocation.availableOnNodes** (NodeSelector)

    Це поле встановлюється драйвером ресурсу після виділення ресурсу, щоб інформувати планувальник, де можна розміщувати Podʼи, що використовують ResourceClaim.

    Встановлення цього поля є необовʼязковим. Якщо воно має значення null, ресурс доступний всюди.

    <a name="NodeSelector"></a>
    *Node selector представляє обʼєднання результатів одного або кількох запитів за мітками по набору вузлів; тобто представляє OR вибірок, представлених термінами вибірки вузлів.*

    - **allocation.availableOnNodes.nodeSelectorTerms** ([]NodeSelectorTerm), обовʼязково

      Обовʼязково. Список термінів вибірки вузлів. Терміни поєднуються логічним OR.

      <a name="NodeSelectorTerm"></a>
      *Нульовий або порожній термін вибірки вузлів не відповідає жодним обʼєктам. Їхні вимоги поєднуються логічним AND. Тип TopologySelectorTerm реалізує підмножину типу NodeSelectorTerm.*

      - **allocation.availableOnNodes.nodeSelectorTerms.matchExpressions** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

        Список вимог вибірки вузлів за мітками вузлів.

      - **allocation.availableOnNodes.nodeSelectorTerms.matchFields** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}

        Список вимог вибірки вузлів за полями вузлів.

  - **allocation.resourceHandles** ([]ResourceHandle)

    *Atomic: буде замінено під час злиття*

    ResourceHandles містять стан, повʼязаний з виділенням, який слід підтримувати протягом усього терміну запиту. Кожен ResourceHandle містить дані, які слід передати певному втулку kubelet після його розміщення на вузлі. Ці дані повертаються драйвером після успішного виділення та є непрозорими для Kubernetes. Документація драйвера може пояснити користувачам, як інтерпретувати ці дані, якщо це необхідно.

    Встановлення цього поля є необовʼязковим. Воно має максимальний розмір у 32 записи. Якщо null (або порожній), припускається, що це виділення буде оброблено одним втулком kubelet без доданих даних ResourceHandle. Імʼя втулка kubelet, що викликається, збігається з DriverName, встановленим у ResourceClaimStatus, у якому вбудовано цей AllocationResult.

    <a name="ResourceHandle"></a>
    *ResourceHandle містить непрозорі дані ресурсу для обробки певним втулком kubelet.*

    - **allocation.resourceHandles.data** (string)

      Data містить непрозорі дані, повʼязані з цим ResourceHandle. Їх встановлює компонент контролера драйвера ресурсу, імʼя якого збігається з DriverName, встановленим у ResourceClaimStatus, у якому вбудовано цей ResourceHandle. Встановлюється під час виділення та призначено для обробки втулком kubelet, імʼя якого збігається з DriverName, встановленим у цьому ResourceHandle.

      Максимальний розмір цього поля становить 16 КіБ. У майбутньому це може бути збільшено, але не зменшено.

    - **allocation.resourceHandles.driverName** (string)

      DriverName вказує імʼя драйвера ресурсу, втулок kubelet якого слід викликати для обробки даних цього ResourceHandle після його розміщення на вузлі. Це може відрізнятися від DriverName, встановленого у ResourceClaimStatus, у якому вбудовано цей ResourceHandle.

  - **allocation.shareable** (boolean)

    Shareable визначає, чи підтримує ресурс одночасне використання більше ніж одним споживачем.

- **deallocationRequested** (boolean)

  DeallocationRequested вказує, що ResourceClaim має бути відкликана.

  Драйвер повинен потім відкликати цей запит і скинути поле разом з очищенням поля Allocation.

  Поки DeallocationRequested встановлено, нові споживачі не можуть бути додані до ReservedFor.

- **driverName** (string)

  DriverName — це копія імені драйвера з ResourceClass на момент початку виділення.

- **reservedFor** ([]ResourceClaimConsumerReference)

  *Map: унікальні значення за ключем uid зберігаються під час злиття*

  ReservedFor вказує, яким обʼєктам наразі дозволено використовувати запит. Pod, який посилається на ResourceClaim, що не зарезервований для цього Pod, не буде запущено.

  Може бути максимум 32 таких резервування. У майбутньому це може бути збільшено, але не зменшено.

  <a name="ResourceClaimConsumerReference"></a>
  *ResourceClaimConsumerReference містить достатньо інформації, щоб знайти споживача ResourceClaim. Споживач має бути ресурсом у тому ж просторі імен, що і ResourceClaim.*

  - **reservedFor.name** (string), обовʼязково

    Name — це імʼя ресурсу, на який робиться посилання.

  - **reservedFor.resource** (string), обовʼязково

    Resource — це тип ресурсу, на який робиться посилання, наприклад "pods".

  - **reservedFor.uid** (string), обовʼязково

    UID однозначно ідентифікує один екземпляр ресурсу.

  - **reservedFor.apiGroup** (string)

    APIGroup — це група для ресурсу, на який робиться посилання. Вона порожня для основного API. Це відповідає групі в APIVersion, яка використовується під час створення ресурсів.

## ResourceClaimList {#ResourceClaimList}

ResourceClaimList — це колекція запитів.

---

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClaimList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Стандартні метадані списку

- **items** ([]<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>), обовʼязково

  Items — це список запитів на ресурси.

## Операції {#operations}

---

### `get` отримати вказаний ResourceClaim {#get-read-the-specified-resourceclaim}

#### HTTP Запит {#http-request}

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### Параметри {#parameters}

- **name** (*в шляху*): string, обовʼязково

  назва ResourceClaim

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

401: Unauthorized

### `get` отримати статус вказаного ResourceClaim {#get-read-the-status-of-the-specified-resourceclaim}

#### HTTP Запит {#http-request-1}

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}/status

#### Параметри {#parameters-1}

- **name** (*в шляху*): string, обовʼязково

  назва ResourceClaim

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-1}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

401: Unauthorized

### `list` перелік або перегляд обʼєктів типу ResourceClaim {#list-read-or-watch-objects-of-kind-resourceclaim}

#### HTTP Запит {#http-request-2}

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims

#### Параметри {#parameters-2}

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### Відповідь {#response-2}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimList" >}}">ResourceClaimList</a>): OK

401: Unauthorized

### `list` перелік або перегляд обʼєктів типу ResourceClaim {#list-read-or-watch-objects-of-kind-resourceclaim-1}

#### HTTP Запит {#http-request-3}

GET /apis/resource.k8s.io/v1alpha2/resourceclaims

#### Параметри {#parameters-3}

- **allowWatchBookmarks** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### Відповідь {#response-3}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimList" >}}">ResourceClaimList</a>): OK

401: Unauthorized

### `create` створення ResourceClaim {#create-create-a-resourceclaim}

#### HTTP Запит {#http-request-4}

POST /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims

#### Параметри {#parameters-4}

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-4}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

202 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Accepted

401: Unauthorized

### `update` заміна вказаного ResourceClaim {#replace-replace-the-specified-resourceclaim}

#### HTTP Запит {#http-request-5}

PUT /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### Параметри {#parameters-5}

- **name** (*в шляху*): string, обовʼязково

  назва ResourceClaim

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-5}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

401: Unauthorized

### `update` заміна статусу вказаного ResourceClaim {#update-replace-of-the-specified-resourceclaim}

#### HTTP Запит {#http-request-6}

PUT /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}/status

#### Параметри {#parameters-6}

- **name** (*в шляху*): string, обовʼязково

  назва ResourceClaim

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-6}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

401: Unauthorized

### `patch` часткое оновлення вказаного ResourceClaim {#patch-partially-update-the-specified-resourceclaim}

#### HTTP Запит {#http-request-7}

PATCH /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### Параметри {#parameters-7}

- **name** (*в шляху*): string, обовʼязково

  назва ResourceClaim

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-parameters/common-parameters#patch" >}}">patch</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-7}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

401: Unauthorized

### `patch` часткове оновлення статусу вказаного ResourceClaim {#patch-partially-update-the-status-of-the-specified-resourceclaim}

#### HTTP Запит {#http-request-8}

PATCH /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}/status

#### Параметри {#parameters-8}

- **name** (*в шляху*): string, обовʼязково

  назва ResourceClaim

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-parameters/common-parameters#patch" >}}">patch</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-8}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

401: Unauthorized

### `delete` видалення ResourceClaim {#delete-delete-a-resourceclaim}

#### HTTP запит {#http-request-9}

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### Параметри {#parameters-9}

- **name** (*в шляху*): string, обовʼязково

  назва ResourceClaim

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### Відповідь {#response-9}

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

202 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): ПAccepted

401: Unauthorized

### `deletecollection` видалення колекції ResourceClaim {#deletecollection-delete-collection-of-resourceclaims}

#### HTTP запит {#http-request-10}

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims

#### Параметри {#parameters-10}

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (*в запиті*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### Відповідь {#response-10}

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
