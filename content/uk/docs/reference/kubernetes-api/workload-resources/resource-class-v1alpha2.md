---
api_metadata:
  apiVersion: "resource.k8s.io/v1alpha2"
  import: "k8s.io/api/resource/v1alpha2"
  kind: "ResourceClass"
content_type: "api_reference"
description: "ResourceClass використовується адміністраторами для впливу на розподіл ресурсів."
title: "ResourceClass v1alpha2"
weight: 17
auto_generated: false
---

`apiVersion: resource.k8s.io/v1alpha2`

`import "k8s.io/api/resource/v1alpha2"`

## ResourceClass {#ResourceClass}

ResourceClass використовується адміністраторами для впливу на розподіл ресурсів.

Це тип альфа-версії та вимагає увімкнення функціональних можливостей DynamicResourceAllocation.

---

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClass

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Стандартні метадані обʼєкта.

- **driverName** (string), обовʼязково

  DriverName визначає імʼя динамічного драйвера ресурсів, який використовується для виділення ResourceClaim, що використовує цей клас.

  Ресурсні драйвери мають унікальне імʼя у прямому порядку домену (acme.example.com).

- **parametersRef** (ResourceClassParametersReference)

  ParametersRef посилається на довільний окремий обʼєкт, який може містити параметри, які будуть використані драйвером при виділенні ресурсу, що використовує цей клас. Динамічний драйвер ресурсів може відрізняти параметри, збережені тут, від тих, що зберігаються в ResourceClaimSpec.

  <a name="ResourceClassParametersReference"></a>
  *ResourceClassParametersReference містить достатньо інформації для пошуку параметрів ResourceClass.*

  - **parametersRef.kind** (string), обовʼязково

    Kind — це тип ресурсу, на який робиться посилання. Це те саме значення, що й у метаданих обʼєкта параметрів.

  - **parametersRef.name** (string), обовʼязково

    Name — це назва ресурсу, на який робиться посилання.

  - **parametersRef.apiGroup** (string)

    APIGroup — це група для ресурсу, на який робиться посилання. Вона порожня для основного API. Це відповідає групі в APIVersion, яке використовується при створенні ресурсів.

  - **parametersRef.namespace** (string)

    Namespace — це простір імен, який містить ресурс, на який робиться посилання. Для ресурсів з областю видимості на рівні кластера повинно бути порожнім, а для ресурсів з іменованою областю видимості — непорожнім.

- **suitableNodes** (NodeSelector)

  Тільки вузли, що відповідають селектору, будуть враховані планувальником при спробі знайти вузол, який підходить для Pod, коли цей Pod використовує ResourceClaim, який ще не був виділений.

  Налаштування цього поля є необовʼязковим. Якщо воно null, всі вузли є кандидатами.

  <a name="NodeSelector"></a>
  *Селектор вузла представляє обʼєднання результатів одного або декількох запитів міток на заданий набір вузлів; іншими словами, він представляє OR селекторів, які представлені термінами селектора вузла.*

  - **suitableNodes.nodeSelectorTerms** ([]NodeSelectorTerm), обовʼязково

    Обовʼязково. Список термінів селектора вузла. Терміни є обʼєднані за допомогою OR.

    <a name="NodeSelectorTerm"></a>
    *Null або порожній термін селектора вузла не відповідає жодному обʼєкту. Вимоги є AND. Тип TopologySelectorTerm реалізує підмножину NodeSelectorTerm.*

    - **suitableNodes.nodeSelectorTerms.matchExpressions** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

      Список вимог селектора вузла за мітками вузлів.

    - **suitableNodes.nodeSelectorTerms.matchFields** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

      Список вимог селектора вузла за полями вузлів.

## ResourceClassList {#ResourceClassList}

ResourceClassList є колекцією класів.

---

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClassList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Стандартні метадані списку

- **items** ([]<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>), обовʼязково

  Список класів ресурсів.

## Операції {#operations}

---

### `get` отримати вказаний ResourceClass {#get-read-the-specified-resourceclass}

#### HTTP запит {#http-request}

GET /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### Параметри {#parameters}

- **name** (*в шляху*): string, обовʼязково

  імʼя ResourceClass

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response}

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

401: Unauthorized

### `list` перелік або перегляд обʼєктів типу ResourceClass {#list-or-watch-objects-of-kind-resourceclass}

#### HTTP запит {#http-request-1}

GET /apis/resource.k8s.io/v1alpha2/resourceclasses

#### Параметри {#parameters-1}

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

#### Відповідь {#response-1}

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClassList" >}}">ResourceClassList</a>): OK

401: Unauthorized

### `create` створення ResourceClass {#create-a-new-resourceclass}

#### HTTP запит {#http-request-2}

POST /apis/resource.k8s.io/v1alpha2/resourceclasses

#### Параметри {#parameters-2}

- **body**: <a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-2}

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Created

202 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Accepted

401: Unauthorized

### `update` заміна вказаного ResourceClass {#update-replace-the-specified-resourceclass}

#### HTTP запит {#http-request-3}

PUT /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### Параметри {#parameters-3}

- **name** (*в шляху*): string, обовʼязково

  імʼя ResourceClass

- **body**: <a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-3}

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Created

401: Unauthorized

### `patch` часткове оновлення вказаного ResourceClass {#patch-partially-update-the-specified-resourceclass}

#### HTTP запит {#http-request-4}

PATCH /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### Параметри {#parameters-4}

- **name** (*в шляху*): string, обовʼязково

  імʼя ResourceClass

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, обовʼязково

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

#### Відповідь {#response-4}

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Created

401: Unauthorized

### `delete` видалення ResourceClass {#delete-delete-a-resourceclass}

#### HTTP запит {#http-request-5}

DELETE /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### Параметри {#parameters-5}

- **name** (*в шляху*): string, обовʼязково

  імʼя ResourceClass

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (*в запиті*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### Відповідь {#response-5}

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

202 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Accepted

401: Unauthorized


### `deletecollection` видалення колекції ResourceClass {#deletecollection-delete-collection-of-resourceclass}

#### HTTP запит {#http-request-6}

DELETE /apis/resource.k8s.io/v1alpha2/resourceclasses

#### Параметри {#parameters-6}

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

#### Відповідь {#response-6}

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
