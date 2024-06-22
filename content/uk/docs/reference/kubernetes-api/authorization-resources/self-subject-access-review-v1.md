---
api_metadata:
  apiVersion: "authorization.k8s.io/v1"
  import: "k8s.io/api/authorization/v1"
  kind: "SelfSubjectAccessReview"
content_type: "api_reference"
description: "SelfSubjectAccessReview перевіряє, чи може поточний користувач виконати дію."
title: "SelfSubjectAccessReview"
weight: 2
auto_generated: false
---

`apiVersion: authorization.k8s.io/v1`

`import "k8s.io/api/authorization/v1"`

## SelfSubjectAccessReview {#SelfSubjectAccessReview}

SelfSubjectAccessReview перевіряє, чи може поточний користувач виконати дію. Незаповнення spec.namespace означає "в усіх просторах імен". Self є особливим випадком, оскільки користувачі завжди повинні мати змогу перевірити, чи можуть вони виконати дію.

---

- **apiVersion**: authorization.k8s.io/v1

- **kind**: SelfSubjectAccessReview

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Стандартні метадані списку. Докладніше: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../authorization-resources/self-subject-access-review-v1#SelfSubjectAccessReviewSpec" >}}">SelfSubjectAccessReviewSpec</a>), обовʼязково

  Специфікація містить інформацію про запит, який оцінюється. user та groups повинні бути порожніми.

- **status** (<a href="{{< ref "../authorization-resources/subject-access-review-v1#SubjectAccessReviewStatus" >}}">SubjectAccessReviewStatus</a>)

  Статус заповнюється сервером і вказує, чи дозволено запит, чи ні.

## SelfSubjectAccessReviewSpec {#SelfSubjectAccessReviewSpec}

SelfSubjectAccessReviewSpec є описом запиту на доступ. Має бути встановлене щось одне з ResourceAuthorizationAttributes або NonResourceAuthorizationAttributes.

---

- **nonResourceAttributes** (NonResourceAttributes)

  NonResourceAttributes описує інформацію для запиту на доступ до не-ресурсів.

  <a name="NonResourceAttributes"></a>
  *NonResourceAttributes включає атрибути авторизації, доступні для запитів до інтерфейсу Authorizer, які не стосуються ресурсів.*

  - **nonResourceAttributes.path** (string)

    Path — це URL-шлях запиту.

  - **nonResourceAttributes.verb** (string)

    Verb — це стандартне HTTP-дієслово.

- **resourceAttributes** (ResourceAttributes)

  ResourceAuthorizationAttributes описує інформацію для запиту на доступ до ресурсу.

  <a name="ResourceAttributes"></a>
  *ResourceAttributes включає атрибути авторизації, доступні для запитів до інтерфейсу Authorizer, що стосуються ресурсів.*

  - **resourceAttributes.group** (string)

    Group — це API-група ресурсу. "*" означає всі.

  - **resourceAttributes.name** (string)

    Name — це назва ресурсу, який запитується для "отримання" ("get") або видалення для "delete". "" (порожня) означає всі.

  - **resourceAttributes.namespace** (string)

    Namespace — це простір імен дії, що запитується. Наразі немає різниці між відсутністю простору імен та всіма просторами імен "" (порожньо) стандартно встановлюється з для LocalSubjectAccessReviews "" (порожньо) означає відсутність для кластерних ресурсів "" (порожньо) означає "всі" для ресурсів, обмежених простором імен, з SubjectAccessReview або SelfSubjectAccessReview.

  - **resourceAttributes.resource** (string)

    Resource — це один з наявних типів ресурсів. "*" означає всі.

  - **resourceAttributes.subresource** (string)

    Subresource — це один з наявних типів субресурсів. "" означає відсутність.

  - **resourceAttributes.verb** (string)

    Verb — це дієслово API ресурсу Kubernetes, таке як: get, list, watch, create, update, delete, proxy. "*" означає всі.

  - **resourceAttributes.version** (string)

    Version — це версія API ресурсу. "*" означає всі.

## Операції {#Operations}

---

### `create` створення SelfSubjectAccessReview {#create-create-a-selfsubjectaccessreview}

#### HTTP запит {#http-request}

POST /apis/authorization.k8s.io/v1/selfsubjectaccessreviews

#### Параметри {#parameters}

- **body**: <a href="{{< ref "../authorization-resources/self-subject-access-review-v1#SelfSubjectAccessReview" >}}">SelfSubjectAccessReview</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response}

200 (<a href="{{< ref "../authorization-resources/self-subject-access-review-v1#SelfSubjectAccessReview" >}}">SelfSubjectAccessReview</a>): OK

201 (<a href="{{< ref "../authorization-resources/self-subject-access-review-v1#SelfSubjectAccessReview" >}}">SelfSubjectAccessReview</a>): Created

202 (<a href="{{< ref "../authorization-resources/self-subject-access-review-v1#SelfSubjectAccessReview" >}}">SelfSubjectAccessReview</a>): Accepted

401: Unauthorized