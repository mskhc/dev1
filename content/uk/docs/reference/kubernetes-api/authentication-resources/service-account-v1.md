---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "ServiceAccount"
content_type: "api_reference"
description: >
  ServiceAccount повʼязує разом:

    - імʼя, зрозуміле користувачам і, можливо, периферійним системам, для ідентифікації;
    - головну діючу особу, яка може бути автентифікована і авторизована;
    - набір секретів.
title: "ServiceAccount"
weight: 1
auto_generated: false
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`

## ServiceAccount {#ServiceAccount}

ServiceAccount повʼязує разом

- імʼя, зрозуміле користувачам і, можливо, периферійним системам, для ідентифікації;
- головну діючу особу, яка може бути автентифікована і авторизована;
- набір секретів.

---

- **apiVersion**: v1

- **kind**: ServiceAccount

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Стандартні метадані обʼєкта. Докладніше: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **automountServiceAccountToken** (boolean)

  automountServiceAccountToken вказує, чи повинні Podʼи, які працюють від імені цього службового облікового запису, автоматично мати змонтований API токен. Може бути перевизначено на рівні Podʼа.

- **imagePullSecrets** ([]<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

  imagePullSecrets — це список посилань на Sercretʼи в тому ж просторі імен для використання при завантаженні будь-яких образів у Podʼах, які використовують цей службовий обліковий запис. ImagePullSecrets відрізняються від Secrets тим, що Secrets можуть бути змонтовані в Pod, а ImagePullSecrets доступні лише для kubelet. Докладніше: [https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod](/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod)

- **secrets** ([]<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

  *Patch strategy: обʼєднання за ключем `name`*

  secrets — це список секретів у тому ж просторі імен, які Podʼи, що використовують цей службовий обліковий запис, можуть використовувати. Podʼи обмежуються цим списком лише у випадку, якщо цей службовий обліковий запис має анотацію "kubernetes.io/enforce-mountable-secrets" зі значенням "true". Це поле не слід використовувати для пошуку автоматично створених секретів токенів службових облікових записів для використання поза межами Podʼів. Натомість токени можна запитувати безпосередньо за допомогою API TokenRequest або секрети токенів службових облікових записів можна створювати вручну. Докладніше: [https://kubernetes.io/docs/concepts/configuration/secret](/docs/concepts/configuration/secret)

## ServiceAccountList {#ServiceAccountList}

ServiceAccountList — це список обʼєктів ServiceAccount.

---

- **apiVersion**: v1

- **kind**: ServiceAccountList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Стандартні метадані списку. Докладніше: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>), обовʼязково

  Список обʼєктів ServiceAccount. Докладніше: [https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/](/docs/tasks/configure-pod-container/configure-service-account/)

## Операції {#operations}

---

### `get` отримати вказаний ServiceAccount {#get-read-the-specified-serviceaccount}

#### HTTP запит {#http-request}

GET /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### Параметри {#parameters}

- **name** (*в шляху*): string, обовʼязково

  імʼя ServiceAccount

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response}

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

401: Unauthorized

### `list` перелік або перегляд обʼєктів типу ServiceAccount {#list-list-or-watch-objects-of-kind-serviceaccount}

#### HTTP запит {#http-request-1}

GET /api/v1/namespaces/{namespace}/serviceaccounts

#### Параметри {#parameters-1}

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### Відповідь {#response-1}

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccountList" >}}">ServiceAccountList</a>): OK

401: Unauthorized

### `list` перелік або перегляд обʼєктів типу ServiceAccount {#list-list-or-watch-objects-of-kind-serviceaccount-1}

#### HTTP запит {#http-request-2}

GET /api/v1/serviceaccounts

#### Параметри {#parameters-2}

- **allowWatchBookmarks** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### Відповідь {#response-2}

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccountList" >}}">ServiceAccountList</a>): OK

401: Unauthorized

### `create` створення ServiceAccount {#create-create-a-serviceaccount}

#### HTTP запит {#http-request-3}

POST /api/v1/namespaces/{namespace}/serviceaccounts

#### Параметри {#parameters-3}

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>, обовʼязково

- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-3}

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

201 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Created

202 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Accepted

401: Unauthorized

### `update` заміна вказаного ServiceAccount {#update-replace-the-specified-serviceaccount}

#### HTTP запит {#http-request-4}

PUT /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### Параметри {#parameters-4}

- **name** (*в шляху*): string, обовʼязково

  імʼя ServiceAccount

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>, обовʼязково

- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-4}

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

201 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Created

401: Unauthorized

### `patch` часткове оновлення вказаного ServiceAccount {#patch-partially-update-the-specified-serviceaccount}

#### HTTP запит {#http-request-5}

PATCH /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### Параметри {#parameters-5}

- **name** (*в шляху*): string, обовʼязково

  імʼя ServiceAccount

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, обовʼязково

- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response-5}

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

201 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Created

401: Unauthorized

### `delete` видалення ServiceAccount {#delete-delete-a-serviceaccount}

#### HTTP запит {#http-request-6}

DELETE /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### Параметри {#parameters-6}

- **name** (*в шляху*): string, обовʼязково

  імʼя ServiceAccount

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### Відповідь {#response-6}

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

202 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Accepted

401: Unauthorized

### `deletecollection` видалення колекції ServiceAccount {#deletecollection-delete-collection-of-serviceaccount}

#### HTTP запит {#http-request-7}

DELETE /api/v1/namespaces/{namespace}/serviceaccounts

#### Параметри {#parameters-7}

- **namespace** (*в шляху*): string, обовʼязково

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### Відповідь {#response-7}

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
