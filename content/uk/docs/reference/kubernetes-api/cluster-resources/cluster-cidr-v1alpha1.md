---
api_metadata:
  apiVersion: "networking.k8s.io/v1alpha1"
  import: "k8s.io/api/networking/v1alpha1"
  kind: "ClusterCIDR"
content_type: "api_reference"
description: "ClusterCIDR представляє єдину конфігурацію для розподілу CIDR для кожного вузла, коли ввімкнено MultiCIDRRangeAllocator (див. конфігурацію для kube-controller-manager)."
title: "ClusterCIDR v1alpha1"
weight: 11
auto_generated: false
---

`apiVersion: networking.k8s.io/v1alpha1`

`import "k8s.io/api/networking/v1alpha1"`

## ClusterCIDR {#ClusterCIDR}

ClusterCIDR являє собою єдину конфігурацію для виділення CIDR для кожного вузла, коли увімкнено MultiCIDRRangeAllocator (див. конфігурацію для kube-controller-manager). Кластер може мати будь-яку кількість ресурсів ClusterCIDR, всі з яких будуть розглядатися при виділенні CIDR для вузла. ClusterCIDR може бути використаний для даного вузла, коли селектор вузлів відповідає відповідному вузлу та має вільні CIDR для виділення. У разі кількох ресурсів ClusterCIDR, що відповідають умовам, розподільник спробує вирішити конфлікти за допомогою внутрішніх евристик, але може використовуватися будь-який ClusterCIDR, чий селектор вузла відповідає вузлу.

---

- **apiVersion**: networking.k8s.io/v1alpha1

- **kind**: ClusterCIDR

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Стандартні метадані обʼєкта. Докладніше: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDRSpec" >}}">ClusterCIDRSpec</a>)

  spec — це бажаний стан ClusterCIDR. Додаткова інформація: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## ClusterCIDRSpec {#ClusterCIDRSpec}

ClusterCIDRSpec визначає бажаний стан ClusterCIDR.

---

- **perNodeHostBits** (int32), обовʼязкове

  perNodeHostBits визначає кількість хостових бітів, які потрібно налаштувати для кожного вузла. Маска підмережі визначає, яка частина адреси використовується для мережевих бітів і хостових бітів. Наприклад, адреса IPv4 192.168.0.0/24 розділяє адресу на 24 біти для мережевої частини та 8 бітів для хостової частини. Для виділення 256 IP-адрес встановіть це поле на 8 (маска /24 для IPv4 або /120 для IPv6). Мінімальне значення — 4 (16 IP-адрес). Це поле незмінне.

- **ipv4** (string)

  ipv4 визначає IPv4 IP-блок у нотації CIDR (наприклад, "10.0.0.0/8"). Потрібно вказати принаймні одне з полів ipv4 або ipv6. Це поле незмінне.

- **ipv6** (string)

  ipv6 визначає IPv6 IP-блок у нотації CIDR (наприклад, "2001:db8::/64"). Потрібно вказати принаймні одне з полів ipv4 або ipv6. Це поле незмінне.

- **nodeSelector** (NodeSelector)

  nodeSelector визначає, до яких вузлів застосовується конфігурація. Порожній або nil nodeSelector вибирає всі вузли. Це поле незмінне.

  <a name="NodeSelector"></a>
  *Селектор вузлів представляє обʼєднання результатів одного або декількох запитів за мітками над набором вузлів; тобто він представляє OR селекторів, представлених термінами селектора вузлів.*

  - **nodeSelector.nodeSelectorTerms** ([]NodeSelectorTerm), обовʼязкове

    Обовʼязкове. Список термінів селектора вузлів. Терміни обʼєднуються за допомогою OR.

    <a name="NodeSelectorTerm"></a>
    *Нульовий або порожній термін селектора вузлів не відповідає жодним обʼєктам. Їхні вимоги обʼєднуються за допомогою AND. Тип TopologySelectorTerm реалізує підмножину NodeSelectorTerm.*

    - **nodeSelector.nodeSelectorTerms.matchExpressions** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

      Список вимог селектора вузлів за мітками вузла.

    - **nodeSelector.nodeSelectorTerms.matchFields** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

      Список вимог селектора вузлів за полями вузла.

## ClusterCIDRList {#ClusterCIDRList}

ClusterCIDRList містить список ClusterCIDR.

---

- **apiVersion**: networking.k8s.io/v1alpha1

- **kind**: ClusterCIDRList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Стандартні метадані обʼєкта. Докладніше: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>), обов'язкове

  items — це список ClusterCIDR.

## Операції {#Operations}

---

### `get` отримати вказаний ClusterCIDR {#get-read-the-specified-clustercidr}

#### HTTP запит {#http-request}

GET /apis/networking.k8s.io/v1alpha1/clustercidrs/{name}

#### Параметри {#parameters}

- **name** (*в шляху*): string, обовʼязково

  імʼя ClusterCIDR

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response}

200 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): OK

401: Unauthorized

### `list` перелік або перегляд обʼєктів типу ClusterCIDR {#list-list-objects-of-kind-clustercidr}

#### HTTP запит {#http-request-1}

GET /apis/networking.k8s.io/v1alpha1/clustercidrs

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

200 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDRList" >}}">ClusterCIDRList</a>): OK

401: Unauthorized

### `create` створення ClusterCIDR {#create-create-a-clustercidr}

#### HTTP запит {#http-request-2}

POST /apis/networking.k8s.io/v1alpha1/clustercidrs

#### Параметри {#parameters-2}

- **body**: <a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-2}

200 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): OK

201 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): Created

202 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): Accepted

401: Unauthorized

### `update` заміна вказаного ClusterCIDR {#update-replace-the-specified-clustercidr}

#### HTTP запит {#http-request-3}

PUT /apis/networking.k8s.io/v1alpha1/clustercidrs/{name}

#### Параметри {#parameters-3}

- **name** (*в шляху*): string, обовʼязково

  імʼя ClusterCIDR

- **body**: <a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-3}

200 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): OK

201 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): Created

401: Unauthorized

### `patch` часткове оновлення вказаного ClusterCIDR {#patch-partially-update-the-specified-clustercidr}

#### HTTP запит {#http-request-4}

PATCH /apis/networking.k8s.io/v1alpha1/clustercidrs/{name}

#### Параметри {#parameters-4}

- **name** (*в шляху*): string, обовʼязково

  імʼя ClusterCIDR

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

200 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): OK

201 (<a href="{{< ref "../cluster-resources/cluster-cidr-v1alpha1#ClusterCIDR" >}}">ClusterCIDR</a>): Created

401: Unauthorized

### `delete` видалення ClusterCIDR {#delete-delete-a-clustercidr}

#### HTTP запит {#http-request-5}

DELETE /apis/networking.k8s.io/v1alpha1/clustercidrs/{name}

#### Параметри {#parameters-5}

- **name** (*в шляху*): string, обовʼязково

  імʼя ClusterCIDR

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

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` видалення колекції ClusterCIDR {#deletecollection-delete-collection-of-clustercidr}

#### HTTP запит {#http-request-6}

DELETE /apis/networking.k8s.io/v1alpha1/clustercidrs

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
