---
reviewers:
- klueska
- pohly
title: Динамічне виділення ресурсів
content_type: concept
weight: 65
---

<!-- overview -->

{{< feature-state feature_gate_name="DynamicResourceAllocation" >}}

Динамічне виділення ресурсів — це API для запиту та спільного використання ресурсів між Podʼами та контейнерами всередині Podʼа. Це узагальнення API постійних томів для загальних ресурсів. Драйвери ресурсів від сторонніх розробників відповідають за відстеження та виділення ресурсів, з додатковою підтримкою, що надається Kubernetes через _структуровані параметри_ (з Kubernetes 1.30). Коли драйвер використовує структуровані параметри, Kubernetes виконує обробку та виділення ресурсів без потреби спілкування з драйвером. Різні види ресурсів підтримують довільні параметри для визначення вимог та ініціалізації.

## {{% heading "prerequisites" %}}

Kubernetes v{{< skew currentVersion >}} включає підтримку API на рівні кластера для динамічного виділення ресурсів, але це [потрібно](#enabling-dynamic-resource-allocation) включити явно. Ви також повинні встановити драйвер ресурсів для конкретних ресурсів, які мають бути керовані за допомогою цього API. Якщо ви не використовуєте Kubernetes v{{< skew currentVersion>}}, перевірте документацію для цієї версії Kubernetes.

<!-- body -->

## API

{{< glossary_tooltip text="Група API" term_id="api-group" >}} `resource.k8s.io/v1alpha2` надає наступні типи:

ResourceClass
: Визначає, який драйвер ресурсу обробляє певний вид ресурсу та надає загальні параметри для нього. ResourceClasses створюються адміністратором кластера при встановленні драйвера ресурсів.

ResourceClaim
: Визначає певний екземпляр ресурсу, який потрібний для робочого навантаження. Створюється користувачем (життєвий цикл керується вручну, може бути спільним для різних Podʼів) або для окремих Podʼів панеллю управління на основі ResourceClaimTemplate (автоматичне управління життєвим циклом, зазвичай використовується лише одним Podʼом).

ResourceClaimTemplate
: Визначає специфікацію та деякі метадані для створення ResourceClaims. Створюється користувачем під час розгортання робочого навантаження.

PodSchedulingContext
: Використовується внутрішньо панеллю управління та драйверами ресурсів для координації планування Podʼів, коли для Podʼа потрібно розподілити ResourceClaims.

ResourceSlice
: Використовується зі структурованими параметрами для публікації інформації про ресурси, які доступні у кластері.

ResourceClaimParameters
: Містять параметри для ResourceClaim, які впливають на планування, у форматі, зрозумілому Kubernetes (модель структурованих параметрів). Додаткові параметри можуть бути вбудовані у непрозоре розширення для використання драйвером вендора при налаштуванні базового ресурсу.

ResourceClassParameters
: Аналогічно до ResourceClaimParameters, ResourceClassParameters надає тип параметрів ResourceClass, який зрозумілий Kubernetes.

Параметри для ResourceClass та ResourceClaim зберігаються у різних обʼєктах, зазвичай використовуючи тип, визначений {{< glossary_tooltip term_id="CustomResourceDefinition" text="CRD" >}}, який був створений при встановленні драйвера ресурсів.

Розробники ресурсного драйвера вирішують, чи вони хочуть обробляти ці параметри у власному зовнішньому контролері, чи натомість сподіваються на те, що Kubernetes обробить їх за допомогою структурованих параметрів. Власний контролер надає більшу гнучкість, але автоматичне масштабування кластера не буде надійно працювати для ресурсів, які є локальними для вузлів. Структуровані параметри дозволяють автоматичне масштабування кластера, але можуть не задовольнити всі випадки використання.

Коли драйвер використовує структуровані параметри, все ще можна дозволити кінцевому користувачеві вказувати параметри за допомогою CRD, специфічні для постачальника. У такому випадку драйвер повинен перетворювати ці користувацькі параметри у внутрішні типи. Альтернативно, драйвер також може документувати, як використовувати внутрішні типи безпосередньо.

`PodSpec` `core/v1` визначає ResourceClaims, які потрібні для Podʼа в полі `resourceClaims`. Записи в цьому списку посилаються або на ResourceClaim, або на ResourceClaimTemplate. При посиланні на ResourceClaim всі Podʼи, які використовують цей PodSpec (наприклад, всередині Deployment або StatefulSet), спільно використовують один екземпляр ResourceClaim. При посиланні на ResourceClaimTemplate, кожен Pod отримує свій власний екземпляр.

Список `resources.claims` для ресурсів контейнера визначає, чи отримує контейнер доступ до цих екземплярів ресурсів, що дозволяє спільне використання ресурсів між одним або кількома контейнерами.

Нижче наведено приклад для умовного драйвера ресурсів. Для цього Podʼа буде створено два обʼєкти ResourceClaim, і кожен контейнер отримає доступ до одного з них.

```yaml
apiVersion: resource.k8s.io/v1alpha2
kind: ResourceClass
name: resource.example.com
driverName: resource-driver.example.com
---
apiVersion: cats.resource.example.com/v1
kind: ClaimParameters
name: large-black-cat-claim-parameters
spec:
  color: black
  size: large
---
apiVersion: resource.k8s.io/v1alpha2
kind: ResourceClaimTemplate
metadata:
  name: large-black-cat-claim-template
spec:
  spec:
    resourceClassName: resource.example.com
    parametersRef:
      apiGroup: cats.resource.example.com
      kind: ClaimParameters
      name: large-black-cat-claim-parameters
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-cats
spec:
  containers:
  - name: container0
    image: ubuntu:20.04
    command: ["sleep", "9999"]
    resources:
      claims:
      - name: cat-0
  - name: container1
    image: ubuntu:20.04
    command: ["sleep", "9999"]
    resources:
      claims:
      - name: cat-1
  resourceClaims:
  - name: cat-0
    source:
      resourceClaimTemplateName: large-black-cat-claim-template
  - name: cat-1
    source:
      resourceClaimTemplateName: large-black-cat-claim-template
```

## Планування {#scheduling}

### Без структурованих параметрів {#without-structured-parameters}

На відміну від вбудованих ресурсів (CPU, RAM) та розширених ресурсів (керованих пристроєм драйвера, оголошуваних kubelet), без структурованих параметрів планувальник не має знань про те, які динамічні ресурси доступні в кластері та як вони можуть бути розподілені для задоволення вимог певного ResourceClaim. За це відповідальні драйвери ресурсів. Вони відмічають ResourceClaims як "allocated", як тільки для них зарезервовано ресурси. Це також показує планувальнику, де в кластері доступний ResourceClaim.

ResourceClaims можуть бути виділені відразу після їх створення ("негайне виділення"), без урахування того, які Podʼи їх використовують. Типово виділення затримується до тих пір, поки Pod не буде запланований, який потребує ResourceClaim (тобто "очікування першого споживача").

У цьому режимі планувальник перевіряє всі ResourceClaims, які потрібні для Podʼа, та створює обʼєкт PodScheduling, через який він повідомляє драйвери ресурсів, відповідальні за ці ResourceClaims, про вузли, які планувальник вважає придатними для Podʼа. Драйвери ресурсів відповідають, виключаючи вузли, які не мають достатньо ресурсів драйвера. Як тільки планувальник має цю інформацію, він вибирає один вузол та зберігає цей вибір в обʼєкті PodScheduling. Потім драйвери ресурсів виділяють свої ResourceClaims так, щоб ресурси були доступні на цьому вузлі. Після завершення цього процесу Pod стає запланованим.

У рамках цього процесу також для Podʼа резервуються ResourceClaims. Наразі ResourceClaims можуть використовуватися або ексклюзивно одним Podʼом, або необмеженою кількістю Podʼів.

Одна з ключових особливостей полягає в тому, що Podʼи не заплановані на вузол, поки всі їх ресурси не будуть виділені та зарезервовані. Це дозволяє уникати сценарію, коли Pod запланований на один вузол, а потім не може працювати там, що погано, оскільки такий очікуючий Pod також блокує всі інші ресурси, такі як RAM або CPU, які були відведені для нього.

{{< note >}}

Планування Podʼів, які використовують ResourceClaims, буде повільнішим через додаткову комунікацію, яка потрібна. Зверніть увагу, що це також може вплинути на Podʼи, які не використовують ResourceClaims, оскільки під час обробки Podʼа з ResourceClaims робиться лише один виклик API, що блокується, і тому планування наступного Podʼа затримується.

{{< /note >}}

### Зі структурованими параметрами {#with-structured-parameters}

Коли драйвер використовує структуровані параметри, планувальник бере на себе відповідальність за виділення ресурсів для ResourceClaim, кожного разу, коли Pod потребує їх. Він робить це, отримуючи повний список доступних ресурсів з обʼєктів ResourceSlice, відстежуючи, які з цих ресурсів вже були виділені наявним ResourceClaim, а потім вибираючи з тих ресурсів, що залишилися. Вибрані ресурси піддаються обмеженням, наданим в будь-яких параметрах ResourceClaimParameters або ResourceClassParameters, повʼязаних з ResourceClaim.

Обраний ресурс фіксується у статусі ResourceClaim разом з будь-якими вендор-специфічними параметрами, тому коли Pod збирається запуститися на вузлі, драйвер ресурсу на вузлі має всю необхідну інформацію для підготовки ресурсу.

За допомогою структурованих параметрів планувальник може приймати рішення без спілкування з будь-якими драйверами ресурсів DRA. Він також може швидко планувати кілька Podʼів, зберігаючи інформацію про виділення ресурсів для ResourceClaim у памʼяті та записуючи цю інформацію в обʼєкти ResourceClaim у фоні, одночасно з привʼязкою Podʼа до вузла.

## Моніторинг ресурсів {#monitoring-resources}

Kubelet надає службу gRPC для забезпечення виявлення динамічних ресурсів запущених Podʼів. Для отримання додаткової інформації про точки доступу gRPC дивіться [звіт про виділення ресурсів](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources).

## Попередньо заплановані Podʼи {#pre-scheduled-pods}

Коли ви, або інший клієнт API, створюєте Pod із вже встановленим `spec.nodeName`, планувальник пропускається. Якщо будь-який ResourceClaim, потрібний для цього Podʼа, ще не існує, не виділений або не зарезервований для Podʼа, то kubelet не зможе запустити Pod і періодично перевірятиме це, оскільки ці вимоги можуть бути задоволені пізніше.

Така ситуація також може виникнути, коли підтримка динамічного виділення ресурсів не була увімкнена в планувальнику на момент планування Podʼа (різниця версій, конфігурація, feature gate і т. д.). kube-controller-manager виявляє це і намагається зробити Pod працюючим, провокуючи виділення та/або резервування потрібних ResourceClaims.

{{< note >}}
Це працює лише для ресурсів драйверів, які не використовують структуровані параметри.
{{< /note >}}

Краще уникати цього оминаючи планувальник, оскільки Pod, який призначений для вузла, блокує нормальні ресурси (ОЗП, ЦП), які потім не можуть бути використані для інших Podʼів, поки Pod є застряглим. Щоб запустити Pod на певному вузлі, при цьому проходячи через звичайний потік планування, створіть Pod із селектором вузла, який точно відповідає бажаному вузлу:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-cats
spec:
  nodeSelector:
    kubernetes.io/hostname: назва-призначеного-вузла
  ...
```

Можливо, ви також зможете змінити вхідний Pod під час допуску, щоб скасувати поле `.spec.nodeName` і використовувати селектор вузла замість цього.

## Увімкнення динамічного виділення ресурсів {#enabling-dynamic-resource-allocation}

Динамічне виділення ресурсів є *альфа-функцією* та увімкнуто лише тоді, коли увімкнуто [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) `DynamicResourceAllocation` та {{< glossary_tooltip text="групу API" term_id="api-group" >}} `resource.k8s.io/v1alpha2`. Для отримання деталей щодо цього дивіться параметри [kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/) `--feature-gates` та `--runtime-config`. Також варто увімкнути цю функцію в kube-scheduler, kube-controller-manager та kubelet.

Швидка перевірка того, чи підтримує кластер Kubernetes цю функцію, полягає у виведенні обʼєктів ResourceClass за допомогою наступної команди:

```shell
kubectl get resourceclasses
```

Якщо ваш кластер підтримує динамічне виділення ресурсів, відповідь буде або список обʼєктів ResourceClass, або:

```none
No resources found
```

Якщо це не підтримується, буде виведено помилку:

```none
error: the server doesn't have a resource type "resourceclasses"
```

Типова конфігурація kube-scheduler вмикає втулок "DynamicResources" лише в разі увімкнення feature gate та при використанні конфігурації API v1. Налаштування конфігурації може змінюватися, щоб включити його.

Крім увімкнення функції в кластері, також потрібно встановити драйвер ресурсів. Для отримання додаткової інформації звертайтеся до документації драйвера.

## {{% heading "whatsnext" %}}

- Для отримання додаткової інформації про дизайн дивіться [Dynamic Resource Allocation KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/3063-dynamic-resource-allocation/README.md) та [Structured Parameters KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/4381-dra-structured-parameters).