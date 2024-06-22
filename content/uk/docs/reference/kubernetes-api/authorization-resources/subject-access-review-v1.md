---
api_metadata:
  apiVersion: "authorization.k8s.io/v1"
  import: "k8s.io/api/authorization/v1"
  kind: "SubjectAccessReview"
content_type: "api_reference"
description: "SubjectAccessReview перевіряє, чи може користувач або група виконати дію."
title: "SubjectAccessReview"
weight: 4
auto_generated: false
---

`apiVersion: authorization.k8s.io/v1`

`import "k8s.io/api/authorization/v1"`

## SubjectAccessReview {#SubjectAccessReview}

SubjectAccessReview перевіряє, чи може користувач або група виконати дію.

---

- **apiVersion**: authorization.k8s.io/v1

- **kind**: SubjectAccessReview

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Стандартні метадані списку. Докладніше: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../authorization-resources/subject-access-review-v1#SubjectAccessReviewSpec" >}}">SubjectAccessReviewSpec</a>), обовʼязково

  Специфікація містить інформацію про запит, який оцінюється

- **status** (<a href="{{< ref "../authorization-resources/subject-access-review-v1#SubjectAccessReviewStatus" >}}">SubjectAccessReviewStatus</a>)

  Статус заповнюється сервером і вказує, чи дозволено запит, чи ні

## SubjectAccessReviewSpec {#SubjectAccessReviewSpec}

SubjectAccessReviewSpec — це опис запиту на доступ. Має бути встановлено одне з ResourceAuthorizationAttributes або NonResourceAuthorizationAttributes

---

- **extra** (map[string][]string)

  Extra відповідає методу user.Info.GetExtra() з автентифікатора. Оскільки це вхідні дані для авторизатора, це потребує відображення тут.

- **groups** ([]string)

  Groups — це групи, для яких ви проводите тестування.

- **nonResourceAttributes** (NonResourceAttributes)

  NonResourceAttributes описує інформацію для запиту на доступ до не-ресурсів

  <a name="NonResourceAttributes"></a>
  *NonResourceAttributes включає атрибути авторизації, доступні для запитів на не-ресурси до інтерфейсу Authorizer*

  - **nonResourceAttributes.path** (string)

    Path — це URL шлях запиту

  - **nonResourceAttributes.verb** (string)

    Verb — це стандартне HTTP дієслово

- **resourceAttributes** (ResourceAttributes)

  ResourceAuthorizationAttributes описує інформацію для запиту на доступ до ресурсу

  <a name="ResourceAttributes"></a>
  *ResourceAttributes включає атрибути авторизації, доступні для запитів на ресурси до інтерфейсу Authorizer*

  - **resourceAttributes.group** (string)

    Group — це API група ресурсу. "*" означає всі.

  - **resourceAttributes.name** (string)

    Name — це імʼя ресурсу, який запитується для "отримання" ("get") або видаляється для "видалення" ("delete"). "" (порожньо) означає всі.

  - **resourceAttributes.namespace** (string)

    Namespace — це простір імен дії, яка запитується. Зараз немає різниці між відсутністю простору імен та всіма просторами імен "" (порожньо) змінюється на стандартне значення для LocalSubjectAccessReviews, "" (порожньо) є порожнім для кластерних ресурсів, "" (порожньо) означає "всі" для ресурсів з простором імен у SubjectAccessReview або SelfSubjectAccessReview

  - **resourceAttributes.resource** (string)

    Resource — це один з наявних типів ресурсів. "*" означає всі.

  - **resourceAttributes.subresource** (string)

    Subresource - це один з наявних типів субресурсів. "" означає жоден.

  - **resourceAttributes.verb** (string)

    Verb — це дієслово API ресурсу Kubernetes, таке як: get, list, watch, create, update, delete, proxy. "*" означає всі.

  - **resourceAttributes.version** (string)

    Version — це версія API ресурсу. "*" означає всі.

- **uid** (string)

  UID — інформація про користувача, який робить запит.

- **user** (string)

  User — це користувач, для якого проводиться тестування. Якщо ви вказуєте "User", але не "Groups", то це інтерпретується як "Що, якщо User не є членом жодної групи?"

## SubjectAccessReviewStatus {#SubjectAccessReviewStatus}

SubjectAccessReviewStatus

---

- **allowed** (boolean), обовʼязково

  Allowed є обовʼязковим. True, якщо дія буде дозволена, false в іншому випадку.

- **denied** (boolean)

  Denied є необовʼязковим. True, якщо дія буде заборонена, в іншому випадку false. Якщо як allowed є false, так і denied є false, тоді авторизатор не має думки щодо дозволу дії. Denied не може бути true, якщо Allowed є true.

- **evaluationError** (string)

  EvaluationError — це вказівка на те, що під час перевірки авторизації сталася якась помилка. Цілком можливо отримати помилку і мати можливість продовжити визначення статусу авторизації, не зважаючи на це. Наприклад, RBAC може не мати ролі, але достатньо ролей все ще присутні та привʼязані для розгляду запиту.

- **reason** (string)

  Reason є необовʼязковим. Він вказує, чому запит був дозволений або відхилений.

## Операції {#Operations}

---

### `create` створення SubjectAccessReview {#create-create-a-subjectaccessreview}

#### HTTP запит {#http-request}

POST /apis/authorization.k8s.io/v1/subjectaccessreviews

#### Параметри {#parameters}

- **body**: <a href="{{< ref "../authorization-resources/subject-access-review-v1#SubjectAccessReview" >}}">SubjectAccessReview</a>, обовʼязково

- **dryRun** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (*в запиті*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### Відповідь {#response}

200 (<a href="{{< ref "../authorization-resources/subject-access-review-v1#SubjectAccessReview" >}}">SubjectAccessReview</a>): OK

201 (<a href="{{< ref "../authorization-resources/subject-access-review-v1#SubjectAccessReview" >}}">SubjectAccessReview</a>): Created

202 (<a href="{{< ref "../authorization-resources/subject-access-review-v1#SubjectAccessReview" >}}">SubjectAccessReview</a>): Accepted

401: Unauthorized
