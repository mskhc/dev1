---
title: Життєвий цикл Pod
content_type: concept
weight: 30
---

<!-- overview -->

Ця сторінка описує життєвий цикл Pod. Podʼи слідують визначеному життєвому циклу, починаючи з [фази](#pod-phase) `Pending`, переходячи до фази `Running`, якщо принаймні один з його основних контейнерів запускається добре, а потім до фаз `Succeeded` або `Failed`, залежно від того, чи завершився будь-який контейнер у Pod з помилкою.

Podʼи, подібно окремим контейнерам застосунків, вважаються відносно ефемерними (а не постійними) обʼєктами. Podʼи створюються, отримують унікальний ідентифікатор ([UID](/docs/concepts/overview/working-with-objects/names/#uids)) і призначаються вузлам, де вони залишаються до моменту завершення (відповідно до політики перезапуску) або видалення. Якщо {{< glossary_tooltip term_id="node" text="вузол">}} відмовляє, Podʼи, призначені до цього вузла, [призначаються для видалення](#pod-garbage-collection) після періоду затримки.

<!-- body -->

## Тривалість життя Pod {#pod-lifetime}

Поки Pod працює, kubelet може перезапускати контейнери, щоб вирішити деякі види несправностей. У межах Pod Kubernetes відстежує різні [стани контейнера](#container-states) і визначає дії, які слід вжити, щоб знову забезпечити справність Pod.

В API Kubernetes у Pod є як специфікація, так і фактичний стан. Стан для обʼєкта Pod складається з набору [станів Pod](#pod-conditions). Ви також можете вставляти [власні дані готовності](#pod-readiness-gate) в дані стани для Pod, якщо це корисно для вашого застосунку.

Podʼи плануються лише [один раз](/docs/concepts/scheduling-eviction/) протягом свого життя; призначення Pod до певного вузла називається _привʼязка_, а процес вибору який вузол використовувати, називається _плануванням_. Після того, як Pod було заплановано і привʼязано до вузла, Kubernetes намагається запустити цей Pod на цьому вузлі. Pod працює на цьому вузлі, доки не зупиниться, або доки його не буде не буде [завершено](#pod-termination); якщо Kubernetes не може запустити Pod на вибраному вузлі вузлі (наприклад, якщо вузол аварійно завершить роботу до запуску Pod), то цей конкретний Pod ніколи не запуститься.

Ви можете використати [Готовність до планування подів](/docs/concepts/scheduling-eviction/pod-scheduling-readiness/) щоб затримати планування для Pod, доки не буде видалено всі його _scheduling gates_. Наприклад, ви можете визначити набір Podʼів, але запустити планування лише після того, як всі Podʼи будуть створені.

### Pods та усунення несправностей {#pod-fault-recovery}

Якщо один з контейнерів у Pod виходить з ладу, Kubernetes може спробувати перезапустити саме цей контейнер. Щоб дізнатися більше, прочитайте [Як Pods вирішують проблеми з контейнерами](#container-restarts).

Pods можуть вийти з ладу таким чином, що кластер не зможе відновитися, і в такому випадку Kubernetes не намагається далі відновлювати Pod; замість цього Kubernetes видаляє Pod і покладається на інші компоненти для забезпечення автоматичного відновлення.

Якщо Pod заплановано на {{< glossary_tooltip text="вузол" term_id="node" >}} і цей вузол вийшов з ладу, то цей Pod вважається несправним, і Kubernetes зрештою видаляє його. Pod не переживе {{< glossary_tooltip text="виселення" term_id="eviction" >}} через нестачу ресурсів або обслуговування вузла.

У Kubernetes використовується абстракція вищого рівня, яка називається {{< glossary_tooltip term_id="controller" text="контролео" >}}, яка відповідає за роботу керуванням відносно одноразовими екземплярами Pod.

Даний Pod (визначений UID) ніколи не "переплановується" на інший вузол; замість цього, цей Pod може бути замінений новим, майже ідентичним Podʼом. Якщо ви створюєте новий Pod, він може навіть мати ту саму назву (як у `.metadata.name`), що й старий Pod, але заміна буде мати інший `.metadata.uid`, ніж старий Pod.

Kubernetes не гарантує, що заміну існуючого Pod буде заплановано на на той самий вузол, де був старий Pod, який замінюється.

### Повʼязані терміни служби {#associated-lifetimes}

Коли говорять, що щось має такий самий термін життя, як і Pod, наприклад {{< glossary_tooltip term_id="volume" text="volume" >}}, це означає, що ця річ існує стільки часу, скільки існує цей конкретний Pod (з таким самим UID). Якщо цей Pod буде видалений з будь-якої причини, і навіть якщо буде створений ідентичний замінник, повʼязана річ (у цьому прикладі — том) також буде знищена і створена знову.

{{< figure src="/images/docs/pod.svg" title="Малюнок 1." class="diagram-medium" caption="Багатоконтейнерний Pod, який містить механізм отримання файлів [sidecar] (/docs/concepts/workloads/pods/sidecar-containers/) і веб-сервер. Pod використовує [ефемерний том `emptyDir`](/docs/concepts/storage/volumes/#emptydir) для спільного зберігання між контейнерами.">}}

## Фази Pod {#pod-phase}

Поле `status` обʼєкта [PodStatus](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podstatus-v1-core) Podʼа містить поле `phase`.

Фази Pod — це простий, високорівневий підсумок того, на якому етапі свого життєвого циклу знаходиться Pod. Фаза не призначена бути всеосяжним підсумком спостережень за станом контейнера чи Pod, і бути процесом за спостереженням стану.

Кількість та значення фаз Pod є строго прописаними. Крім того, що зазначено тут, не слід вважати, що щось відомо про Podʼи з певним значенням `phase`.

Ось можливі значення для `phase`:

Значення      | Опис
:------------|:-----------
`Pending`    | Pod прийнятий кластером Kubernetes, але один чи кілька контейнерів ще не було налаштовано та готові до запуску. Це включає час, який Pod витрачає на очікування планування, а також час, який витрачається на завантаження образів контейнерів з мережі.
`Running`    | Pod привʼязаний до вузла, і всі контейнери створені. Принаймні один контейнер все ще працює або перебуває у процесі запуску чи перезапуску.
`Succeeded`  | Всі контейнери в Podʼі завершили роботу успішно і не будуть перезапущені.
`Failed`     | Всі контейнери в Podʼі завершили роботу, і принаймні один контейнер завершився з помилкою. Іншими словами, контейнер вийшов зі статусом, відмінним від нуля, або його завершила система, і контейнер не налаштований на автоматичний перезапуск.
`Unknown`    | З якоїсь причини не вдалося отримати стан Podʼа. Ця фаза, як правило, виникає через помилку в комунікації з вузлом, де повинен виконуватися Pod.

{{< note >}}
Коли Pod видаляється, за деякими командами kubectl він позначається як `Terminating`. Цей статус `Terminating` не є однією з фаз Podʼа. Pod отримує термін на відповідне завершення, який типово становить 30 секунд. Ви можете використовувати прапорець `--force` для [примусового завершення роботи Podʼа](/docs/concepts/workloads/pods/pod-lifecycle/#forced).
{{< /note >}}

Починаючи з Kubernetes 1.27, kubelet переводить видалені Podʼи, крім [статичних Podʼів](/docs/tasks/configure-pod-container/static-pod/) та [примусово видалених Podʼів](/docs/concepts/workloads/pods/pod-lifecycle/#forced) без завершувача, в термінальну фазу (`Failed` або `Succeeded` залежно від статусів exit контейнерів Podʼа) перед їх видаленням із сервера API.

Якщо вузол вмирає або відключається від іншої частини кластера, Kubernetes застосовує політику встановлення `phase` всіх Podʼів на втраченому вузлі у Failed.

## Стани контейнера {#container-states}

Окрім [фаз](#pod-phase) Podʼа загалом Kubernetes відстежує стан кожного контейнера всередині Podʼа. Ви можете використовувати [хуки життєвого циклу контейнера](/docs/concepts/containers/container-lifecycle-hooks/), щоб запускати події на певних етапах життєвого циклу контейнера.

Як тільки {{< glossary_tooltip text="планувальник" term_id="kube-scheduler" >}} призначає Pod вузлу, kubelet починає створювати контейнери для цього Podʼа, використовуючи {{< glossary_tooltip text="середовище виконання контейнерів" term_id="container-runtime" >}}. Існує три можливі стани контейнера: `Waiting` (Очікування), `Running` (Виконання) та `Terminated` (Завершено).

Щоб перевірити стан контейнерів Podʼа, ви можете використовувати `kubectl describe pod <імʼя-пода>`. Вивід показує стан для кожного контейнера в межах цього Podʼа.

Кожен стан має конкретне значення:

### `Waiting` {#container-state-waiting}

Якщо контейнер не перебуває в стані або `Running`, або `Terminated`, то він знаходиться в стані `Waiting` (Очікування). Контейнер в стані `Waiting` все ще виконує операції, які він потребує для завершення запуску: наприклад, витягує образ контейнера із реєстру образів контейнерів або застосовує {{< glossary_tooltip text="Secret" term_id="secret" >}}. Коли ви використовуєте `kubectl` для опитування Podʼа із контейнером, який перебуває в стані `Waiting`, ви також бачите поле Reason, щоб узагальнити причину, чому контейнер знаходиться в цьому стані.

### `Running` {#container-state-running}

Статус `Running` вказує на те, що виконання контейнера відбувається без проблем. Якщо існує налаштований хук `postStart` — його роботу завершено. Коли ви використовуєте `kubectl` для опитування Podʼа із контейнером, який перебуває в стані `Running`, ви також бачите інформацію про те, коли контейнер увійшов в стан `Running`.

### `Terminated` {#container-state-terminated}

Контейнер в стані `Terminated` розпочав виконання і потім або завершив його успішно, або зазнав відмови з певних причин. Коли ви використовуєте `kubectl` для опитування Podʼа із контейнером, який перебуває в стані `Terminated`, ви бачите причину, код виходу та час початку та завершення періоду виконання цього контейнера.

Якщо у контейнера є налаштований хук `preStop`, цей хук запускається перед тим, як контейнер увійде в стан `Terminated`.

## Як Podʼи вирішують проблеми з контейнерами {#container-restarts}

Kubernetes порається з відмовами контейнерів в межах Podʼів за допомогою політики перезапуску, визначеної в `spec` Podʼа. Ця політика визначає, як Kubernetes реагує на виходи контейнерів через помилки або інші причини, які складаються з наступних етапів:

1. **Початковий збій**: Kubernetes намагається негайно перезапустити контейнер на основі політики перезапуску Podʼа.
2. **Повторні збої**: Після початкового збою Kubernetes застосовує експоненційну затримку для наступних перезапусків, описане в [`restartPolicy`](#restart-policy). Це запобігає швидким, повторним спробам перезапуску, що може перенавантажити систему.
3. **Стан `CrashLoopBackOff`**: Це означає, що механізм затримки працює для певного контейнера, який знаходиться в циклі збоїв, невдач і постійного перезапуску.
4. **Скидання затримки**: Якщо контейнер успішно працює протягом певного часу (наприклад, 10 хвилин), Kubernetes скидає затримку, розглядаючи будь-який новий збій як перший.

На практиці, `CrashLoopBackOff` — це стан або подія, яку можна помітити у виводі команди `kubectl`, при описі або перегляді списку Podʼів, коли контейнер в Podʼі не запускається належним чином, а потім безперервно намагається запуститися, але безуспішно.

Іншими словами, коли контейнер увійшов у цикл збоїв, Kubernetes застосовує експоненційну затримку, про яку було згадано в [політиці перезапуску контейнера](#restart-policy). Цей механізм запобігає неправильному контейнеру перевантажувати систему безперервними невдалими спробами запуску.

`CrashLoopBackOff` може бути спричинений проблемами, такими як:

* Помилки застосунків, які призводять до виходу контейнера.
* Помилки конфігурації, такі як неправильні змінні середовища або відсутність конфігураційних файлів.
* Обмеження ресурсів, коли контейнеру може бракувати памʼяті або процесорного часу для правильного запуску.
* Невдалі перевірки готовності, якщо застосунок не починає обслуговувати запити у передбачений час.
* Проблеми контейнерних перевірок готовності або перевірок запуску, що повертають результат `Failure`, як згадано у [розділі про перевірки](#container-probes).

Щоб розібратися у причинах `CrashLoopBackOff` проблеми, користувач може:

1. **Перевірити логи**: Використовуйте `kubectl logs <name-of-pod>`, щоб перевірити логи контейнера. Це часто є безпосереднім способом діагностики проблеми, що викликає збої.
1. **Перевірити події**: Використовуйте `kubectl describe pod <name-of-pod>` для перегляду подій для Podʼа, які можуть надати підказки про проблеми конфігурації або ресурсів.
1. **Перевірити конфігурацію**: Переконайтеся, що конфігурація Podʼа, включаючи змінні середовища та змонтовані томи, є правильною і що всі необхідні зовнішні ресурси доступні.
1. **Перевірити обмеження ресурсів**: Переконайтеся, що контейнер має достатньо CPU та памʼяті. Іноді збільшення ресурсів у визначенні Podʼа може вирішити проблему.
1. **Перевірити застосунок**: Можуть існувати помилки або неправильні конфігурації в коді застосунку. Запуск цього образу контейнера локально або в середовищі розробки може допомогти діагностувати проблеми, специфічні для застосунку.

### Політика перезапуску контейнера {#restart-policy}

У полі `spec` Podʼа є поле `restartPolicy` із можливими значеннями Always, OnFailure та Never. Стандартне значення — Always.

`restartPolicy` для Podʼа застосовується до {{< glossary_tooltip text="контейнер застосунків" term_id="app-container" >}} в Podʼі та до звичайних [контейнерів ініціалізації](/docs/concepts/workloads/pods/init-containers/). [Контейнери Sidecar](/docs/concepts/workloads/pods/sidecar-containers/) не звертають уваги на поле `restartPolicy` на рівні Podʼа: в Kubernetes, sidecar визначається як запис всередині `initContainers`, який має свою політику перезапуску контейнера на рівні контейнера, встановлену на `Always`. Для контейнерів ініціалізації, які завершують роботу із помилкою, kubelet виконує їх перезапуск, якщо політика перезапуску Podʼа встановлена як `OnFailure` або `Always`:

* `Always`: автоматично перезапускає контейнер після його завершення, незалежно від статусу завершення.
* `OnFailure`: перезапускає контейнер тільки після його завершення з помилкою (код виходу відмінний від нуля).
* `Never`: ніколи автоматично не перезапускає контейнер, що завершив роботу.

Коли kubelet обробляє перезапуск контейнера згідно з налаштованою політикою перезапуску, це стосується лише перезапусків, які призводять до заміни контейнерів всередині того ж Podʼа та на тому ж вузлі. Після завершення контейнерів у Podʼі, kubelet перезапускає їх із затримкою, що зростає експоненційно (10 с, 20 с, 40 с, …), і обмеженою пʼятьма хвилинами (300 секунд). Якщо контейнер виконується протягом 10 хвилин без проблем, kubelet скидає таймер затримки перезапуску для цього контейнера. [Контейнери Sidecar та життєвий цикл Podʼа](/docs/concepts/workloads/pods/sidecar-containers/#sidecar-containers-and-pod-lifecycle) пояснює поведінку `контейнерів ініціалізації` при вказанні поля `restartpolicy` для нього.

## Стани Podʼа {#pod-conditions}

У Podʼа є статус, який містить масив [PodConditions](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podcondition-v1-core), через які Pod проходить чи не проходить. Kubelet управляє наступними PodConditions:

* `PodScheduled`: Pod був запланований на вузол.
* `PodReadyToStartContainers`: (бета-функція; типово [увімкнено](#pod-has-network)) Pod sandbox був успішно створений, і була налаштована мережа.
* `ContainersReady`: всі контейнери в Pod готові.
* `Initialized`: всі [контейнери ініціалізації](/docs/concepts/workloads/pods/init-containers/) успішно завершили виконання.
* `Ready`: Pod може обслуговувати запити і його слід додати до балансування навантаження всіх відповідних Services.

Назва поля          | Опис
:--------------------|:-----------
`type`               | Імʼя цього стану Podʼа.
`status`             | Вказує, чи застосовується цей стан, з можливими значеннями "`True`", "`False`" або "`Unknown`".
`lastProbeTime`      | Відмітка часу останнього запиту стану Podʼа.
`lastTransitionTime` | Відмітка часу для останнього переходу Podʼа з одного статусу в інший.
`reason`             | Машиночитаний текст у форматі UpperCamelCase, який вказує причину останньої зміни стану.
`message`            | Повідомлення, яке вказує подробиці щодо останнього переходу стану, яке може розібрати людина.

### Готовність Podʼа {#pod-readiness-gate}

{{< feature-state for_k8s_version="v1.14" state="stable" >}}

Ваш застосунок може внести додатковий зворотний звʼязок або сигнали в PodStatus: _готовність Podʼа_. Щоб використовувати це, встановіть `readinessGates` в `spec` Podʼа, щоб вказати список додаткових станів, які kubelet оцінює для готовності Podʼа.

Стани готовності визначаються поточним станом полів `status.condition` для Podʼа. Якщо Kubernetes не може знайти такий стан в полі `status.conditions` Podʼа, стан подається як "`False`".

Наприклад:

```yaml
kind: Pod
...
spec:
  readinessGates:
    - conditionType: "www.example.com/feature-1"
status:
  conditions:
    - type: Ready                              # вбудований стан Podʼа
      status: "False"
      lastProbeTime: null
      lastTransitionTime: 2018-01-01T00:00:00Z
    - type: "www.example.com/feature-1"        # додатковий стан Podʼа
      status: "False"
      lastProbeTime: null
      lastTransitionTime: 2018-01-01T00:00:00Z
  containerStatuses:
    - containerID: docker://abcd...
      ready: true
...
```

Стани Podʼа, які ви додаєте, повинні мати імена, які відповідають [формату ключа міток](/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set) Kubernetes.

### Стан для готовності Podʼа {#pod-readiness-status}

Команда `kubectl patch` не підтримує зміну статусу обʼєкта накладанням патчів. Щоб встановити ці `status.conditions` для Podʼа, застосунки та {{< glossary_tooltip term_id="operator-pattern" text="оператори">}} повинні використовувати дію `PATCH`. Ви можете використовувати [бібліотеку клієнтів Kubernetes](/docs/reference/using-api/client-libraries/) для написання коду, який встановлює власні стани Podʼа для готовності Podʼа.

Для Podʼа, який використовує власні стани, Pod оцінюється як готовий **тільки** коли застосовуються обидві наступні твердження:

* Всі контейнери в Pod готові.
* Всі стани, вказані в `readinessGates`, рівні `True`.

Коли контейнери Podʼа готові, але принаймні один власний стан відсутній або `False`, kubelet встановлює стан Podʼа [ContainersReady](#pod-conditions) в `True`.

### Готовність мережі Podʼа {#pod-has-network}

{{< feature-state for_k8s_version="v1.29" state="beta" >}}

{{< note >}}
На початкових стадіях створення цей стан називали `PodHasNetwork`.
{{< /note >}}

Після того, як Pod отримує призначення на вузол, йому потрібно бути допущеним до kubelet та мати встановлені всі необхідні томи зберігання. Як тільки ці фази завершаться, kubelet співпрацює з середовищем виконання контейнерів (використовуючи {{< glossary_tooltip term_id="cri" >}}), щоб налаштувати ізольоване середовище виконання та налаштувати мережу для Podʼа. Якщо [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) `PodReadyToStartContainersCondition` увімкнено (є типово увімкненим для Kubernetes {{< skew currentVersion >}}), стан `PodReadyToStartContainers` буде додано до поля `status.conditions` Podʼа.

Стан `PodReadyToStartContainers` встановлюється в `False` Kubelet, коли він виявляє, що у Podʼа немає ізольованого середовища виконання із налаштованою мережею. Це трапляється в
наступних випадках:

* На початковому етапі життєвого циклу Podʼа, коли kubelet ще не почав налаштовувати середовище виконання для Podʼа за допомогою середовища виконання контейнерів.
* Пізніше в життєвому циклі Podʼа, коли sandbox Podʼа був знищений через:
  * перезавантаження вузла без вилучення Podʼа
  * для середовищ виконання контейнерів, які використовують віртуальні машини для ізоляції, Pod sandbox віртуальної машини перезавантажується, що потім вимагає створення нового sandbox та свіжої конфігурації мережі контейнера.

Стан `PodReadyToStartContainers` встановлюється в `True` kubelet після успішного завершення створення і налаштування ізольованого середовища виконання для Podʼа за допомогою втулка виконання. Kubelet може почати витягувати образ контейнера та створювати контейнери після встановлення стану `PodReadyToStartContainers` в `True`.

Для Podʼа з контейнерами ініціалізації kubelet встановлює стан `Initialized` в `True` після успішного завершення контейнерів ініціалізації (що відбувається після успішного створення sandbox та налаштування мережі контейнером втулка виконання). Для Podʼа без контейнерів ініціалізації kubelet встановлює стан `Initialized` в `True` перед початком створення sandbox та налаштування мережі.

## Діагностика контейнера {#container-probes}

Проба (_probe_) — це діагностика, яку періодично виконує [kubelet](/docs/reference/command-line-tools-reference/kubelet/) для контейнера. Для виконання діагностики kubelet або виконує код всередині контейнера, або виконує мережевий запит.

### Механізми перевірки {#probe-check-methods}

Існує чотири різних способи перевірки контейнера за допомогою проб. Кожна проба повинна визначати один з чотирьох цих механізмів:

`exec`
: Виконує вказану команду всередині контейнера. Діагностика вважається успішною, якщо команда виходить з кодом стану 0.

`grpc`
: Виконує віддалений виклик процедури [gRPC](https://grpc.io/). Цільовий обʼєкт повинен мати підтримку [gRPC health checks](https://grpc.io/grpc/core/md_doc_health-checking.html). Діагностика вважається успішною, якщо `status` відповіді рівний `SERVING`.

`httpGet`
: Виконує HTTP-запит `GET` до IP-адреси Podʼа з вказаним портом та шляхом. Діагностика вважається успішною, якщо код стану відповіді більший або рівний 200 і менше ніж 400.

`tcpSocket`
: Виконує перевірку TCP до IP-адреси Podʼа за вказаним портом. Діагностика вважається успішною, якщо порт відкритий. Якщо віддалена система (контейнер) відразу закриває зʼєднання після відкриття, це вважається нормальним.

{{< caution >}} На відміну від інших механізмів, виконання проби `exec` передбачає створення/розгалуження кількох процесів при кожному виконанні. В результаті використання проб з exec на кластерах з високою щільністю Pod, низькими інтервалами `initialDelaySeconds`, `periodSeconds`, конфігуруючи будь-яку пробу з механізмом exec, може виникнути надмірне навантаження на використання центрального процесора вузла. У таких сценаріях розгляньте можливість використання альтернативних механізмів проб, щоб уникнути надмірного навантаження.{{< /caution >}}

### Результат проби {#probe-outcome}

Кожна проба має один із трьох результатів:

`Success`
: Контейнер пройшов діагностику.

`Failure`
: Контейнер не пройшов діагностику.

`Unknown`
: Діагностика не пройшла (не потрібно вживати жодних заходів, і kubelet буде робити подальші перевірки).

### Типи проб {#types-of-probe}

Kubelet може опціонально виконувати та реагувати на три типи проб для робочих контейнерів:

`livenessProbe`
: Вказує, чи контейнер працює. Якщо ця проба не проходить, kubelet припиняє роботу контейнера, і він підлягає перезапуску відповідно до своєї [політики перезапуску](#restart-policy). Якщо контейнер не надає пробу життєздатності, стандартний стан — `Success`.

`readinessProbe`
: Вказує, чи готовий контейнер відповідати на запити. Якщо проба готовності завершиться невдачею, контролер endpoint видаляє IP-адресу Podʼа з endpoint усіх служб, які відповідають Podʼа. Стандартний стан готовності перед початковою затримкою — `Failure`. Якщо контейнер не надає пробу готовності, стандартний стан — `Success`.

`startupProbe`
: Вказує, чи запущено застосунок всередині контейнера. Усі інші проби вимкнено, якщо надана проба запуску, поки вона не стане успішною. Якщо проба запуску завершиться невдачею, kubelet вбиває контейнер, і він підлягає перезапуску відповідно до [політики перезапуску](#restart-policy). Якщо контейнер не надає пробу запуску, стандартний стан — `Success`.

Для отримання докладнішої інформації щодо налаштування проб життєздатності, готовності або запуску дивіться [Налаштування проб життєздатності, готовності та запуску](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

#### Коли слід використовувати пробу життєздатності? {#when-should-you-use-a-liveness-probe}

Якщо процес у вашому контейнері може аварійно завершитися, коли виникає проблема або він стає нездоровим, вам можливо не потрібна проба життєздатності; kubelet автоматично виконає правильну дію згідно з політикою перезапуску Podʼа.

Якщо ви хочете, щоб роботу вашого контейнера було припинено та він був перезапущений у разі невдачі проби, то вказуйте пробу життєздатності та встановлюйте `restartPolicy` на Always або OnFailure.

#### Коли слід використовувати пробу готовності? {#when-should-you-use-a-readiness-probe}

Якщо ви хочете розпочати надсилання трафіку до Podʼа лише після успішної проби, вказуйте пробу готовності. У цьому випадку проба готовності може бути такою самою, як і проба життєздатності, але наявність проби готовності в специфікації означає, що Pod розпочне роботу без отримання будь-якого трафіку і почне отримувати трафік лише після успішності проби.

Якщо ви хочете, щоб ваш контейнер міг вимкнутися для обслуговування, ви можете вказати пробу готовності, яка перевіряє конкретний endpoint для готовності, відмінний від проби життєздатності.

Якщо ваш застосунок залежить від  бекенд сервісів, ви можете реалізувати як пробу життєздатності, так і пробу готовності. Проба життєздатності пройде, коли саме застосунок є справним, але проба готовності додатково перевірить, що кожна необхідна служба доступна. Це допомагає уникнути направлення трафіку до Podʼів, які можуть відповідати лише повідомленнями про помилки.

Якщо вашому контейнеру потрібно працювати з великими даними, файлами конфігурації або міграціями під час запуску, ви можете використовувати [пробу запуску](#when-should-you-use-a-startup-probe). Однак, якщо ви хочете виявити різницю між застосунком, який зазнав невдачі, і щастосунком, який все ще обробляє дані запуску, вам може більше підійти проба готовності.

{{< note >}}
Якщо вам потрібно мати можливість забрати запити при видаленні Podʼа, вам, можливо, не потрібна проба готовності; при видаленні Pod автоматично переводить себе в стан неготовності, незалежно від того, чи існує проба готовності. Pod залишається в стані неготовності, поки контейнери в Podʼі не зупиняться.
{{< /note >}}

#### Коли слід використовувати пробу запуску? {#when-should-you-use-a-startup-probe}

Проби запуску корисні для Podʼів, в яких контейнери потребують багато часу, щоб перейти в режим експлуатації. Замість встановлення довгого інтервалу життєздатності, ви можете налаштувати окрему конфігурацію для спостереження за контейнером при запуску, встановивши час, більший, ніж дозволяв би інтервал життєздатності.

Якщо ваш контейнер зазвичай запускається довше, ніж
`initialDelaySeconds + failureThreshold × periodSeconds`, вам слід вказати пробу запуску, яка перевіряє той самий endpoint, що й проба життєздатності. Типово для `periodSeconds` — 10 секунд. Потім ви повинні встановити його `failureThreshold` настільки великим, щоб дозволити контейнеру запускатися, не змінюючи стандартних значень проби життєздатності. Це допомагає захистити від блокування роботи.

### Завершення роботи Podʼів {#pod-termination}

Оскільки Podʼи представляють процеси, які виконуються на вузлах кластера, важливо дозволити цим процесам завершувати роботу відповідним чином, коли вони більше не потрібні (замість раптового зупинення за допомогою сигналу `KILL` і відсутності можливості завершити роботу).

Дизайн спрямований на можливість запитування видалення та знання про те, коли процеси завершують роботу, а також можливість забезпечення завершення видалень у настанні строки. Коли ви запитуєте видалення Podʼа, кластер реєструє та відстежує призначений строк належного припинення роботи перед тим, як дозволити примусове закінчення роботи Podʼа. З цим відстеженням примусового завершення, {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} намагається виконати належне завершення роботи Podʼа.

Зазвичай, з цим належним завершенням роботи, kubelet робить запити до середовища виконання контейнера з метою спроби зупинити контейнери у Podʼі, спочатку надсилаючи сигнал TERM (також відомий як SIGTERM) основному процесу в кожному контейнері з таймаутом для належного завершення. Запити на зупинку контейнерів обробляються середовищем виконання контейнера асинхронно. Немає гарантії щодо порядку обробки цих запитів. Багато середовищ виконання контейнерів враховують значення `STOPSIGNAL`, визначене в образі контейнера і, якщо воно відрізняється, надсилають значення STOPSIGNAL, визначене в образі контейнера, замість TERM. Після закінчення строку належного завершення роботи сигнал KILL надсилається до будь-яких залишкових процесів, а потім Pod видаляється з {{< glossary_tooltip text="API Server" term_id="kube-apiserver" >}}. Якщо kubelet або служба управління середовищем виконання перезапускається під час очікування завершення процесів, кластер повторює спробу спочатку, включаючи повний початковий строк належного завершення роботи.

Приклад припинення роботи Podʼа проілюстровано у наступному прикладі:

1. Ви використовуєте інструмент `kubectl`, щоб вручну видалити певний Pod, з типовим значення строку належного припинення роботи (30 секунд).

2. В Podʼі в API-сервері оновлюється час, поза яким Pod вважається "мертвим", разом із строком належного припинення роботи. Якщо ви використовуєте `kubectl describe` для перевірки Podʼа, який ви видаляєте, цей Pod показується як "Terminating". На вузлі, на якому виконується Pod: як тільки kubelet бачить, що Pod був позначений як такий, що закінчує роботу (встановлений строк для належного вимкнення), kubelet розпочинає локальний процес вимкнення Podʼа.

   1. Якщо один із контейнерів Podʼа визначає `preStop` [хук](/docs/concepts/containers/container-lifecycle-hooks), і `terminationGracePeriodSeconds` в специфікації Podʼа не встановлено на 0, kubelet виконує цей хук всередині контейнера. Стандартно `terminationGracePeriodSeconds` встановлено на 30 секунд.

      Якщо `preStop` хук все ще виконується після закінчення строку належного припинення роботи, kubelet запитує невелике подовження строку належного припинення роботи в розмірі 2 секунд.

      {{< note >}}
      Якщо `preStop` хук потребує більше часу для завершення, ніж дозволяє стандартний строк належного припинення роботи, вам слід змінити `terminationGracePeriodSeconds` відповідно до цього.
      {{< /note >}}

   2. Kubelet робить виклик до середовища виконання контейнера для надсилання сигналу TERM процесу 1 всередині кожного контейнера.

      Є [спеціальний порядок](#termination-with-sidecars), якщо в Pod визначено будь-які {{< glossary_tooltip text="контейнери sidecar" term_id="sidecar-container" >}}. В іншому випадку контейнери в Pod отримують сигнал TERM у різний час і в довільному порядку. Якщо порядок завершення роботи має значення, розгляньте можливість використання хука `preStop` для синхронізації (або перейдіть на використання контейнерів sidecar).

3. У той же час, коли kubelet розпочинає належне вимкнення Podʼа, панель управління оцінює, чи слід вилучити цей Pod з обʼєктів EndpointSlice (та Endpoints), де ці обʼєкти представляють {{< glossary_tooltip term_id="service" text="Service" >}} із налаштованим {{< glossary_tooltip text="selector" term_id="selector" >}}. {{< glossary_tooltip text="ReplicaSets" term_id="replica-set" >}} та інші ресурси робочого навантаження більше не розглядають такий Pod як дійсний.

   Podʼи, які повільно завершують роботу, не повинні продовжувати обслуговувати звичайний трафік і повинні почати завершення та завершення обробки відкритих зʼєднань. Деякі застосунки потребують більш часу для належного завершення роботи, наприклад, сесії піготовки до обслуговування та завершення.

   Будь-які endpoint, які представляють Podʼи, що закінчують свою роботу, не вилучаються негайно з EndpointSlices, а статус, який вказує на [стан завершення](/docs/concepts/services-networking/endpoint-slices/#conditions), викладається з EndpointSlice API (та застарілого API Endpoints). Endpointʼи, які завершуть роботу, завжди мають статус `ready` як `false` (для сумісності з версіями до 1.26), тому балансувальники навантаження не будуть використовувати його для звичайного трафіку.

   Якщо трафік на завершуючомуся Podʼі ще потрібний, фактичну готовність можна перевірити як стан `serving`. Детальніше про те, як реалізувати очищення зʼєднань, можна знайти в розділі [Порядок завершення роботи Podʼів та Endpointʼів](/docs/tutorials/services/pods-and-endpoint-termination-flow/)

   <a id="pod-termination-beyond-grace-period" />

4. kubelet забезпечує завершення та вимкнення Pod
   1. Коли період очікування закінчується, якщо у Pod все ще працює якийсь контейнер, kubelet ініціює примусове завершення роботи. Середовище виконання контейнера надсилає `SIGKILL` всім процесам, які ще працюють у будь-якому контейнері в Pod. kubelet також очищає прихований контейнер `pause`, якщо цей контейнер використовується.
   1. kubelet переводить Pod у термінальну фазу (`Failed` або `Succeeded` залежно від кінцевого стану його контейнерів).
   1. kubelet ініціює примусове видалення обʼєкта Pod з API-сервера, встановлюючи період очікування на 0 (негайне видалення).
   1. API-сервер видаляє обʼєкт API Pod, який потім більше не доступний для жодного клієнта.

### Примусове завершення Podʼів {#pod-termination-forced}

{{< caution >}}
Примусове завершення може бути потенційно руйнівним для деяких завдань та їх Podʼів.
{{< /caution >}}

Типово всі видалення є належними протягом 30 секунд. Команда `kubectl delete` підтримує опцію `--grace-period=<seconds>`, яка дозволяє вам перевизначити типове значення своїм.

Встановлення належного завершення роботи в `0` примусово та негайно видаляє Pod з API сервера. Якщо Pod все ще працює на вузлі, це примусове видалення спричинює початок негайного прибирання kubelet.

Використовуючи kubectl, ви повинні вказати додатковий прапорець `--force` разом із `--grace-period=0`, щоб виконати примусове видалення.

Під час примусового видалення API-сервер не чекає підтвердження від kubelet, що Pod завершено на вузлі, на якому він працював. Він
негайно видаляє Pod в API, щоб можна було створити новий pod з тим самим імʼям. На вузлі Podʼи, які мають бути видалені негайно, все ще отримують невеликий строк для завершення роботи перед примусовим вимиканням.

{{< caution >}}
Негайне видалення не чекає підтвердження того, що робочий ресурс було завершено. Ресурс може продовжувати працювати в кластері нескінченно.
{{< /caution >}}

Якщо вам потрібно примусово видалити Podʼи, які є частиною StatefulSet, дивіться документацію для [видалення Podʼів з StatefulSet](/docs/tasks/run-application/force-delete-stateful-set-pod/).

### Завершення роботи Pod і контейнери sidecar {##termination-with-sidecars}

Якщо ваш Pod містить один або більше [контейнерів sidecar](/docs/concepts/workloads/pods/sidecar-containers/) (init-контейнерів з політикою перезапуску Always), kubelet затримає надсилання сигналу TERM цим контейнерам sidecar, доки останній основний контейнер повністю не завершить роботу. Контейнери sidecar будуть завершені у зворотному порядку, в якому вони визначені в специфікації Pod. Це забезпечує продовження обслуговування контейнерами sidecar інших контейнерів у Pod, доки вони не стануть непотрібними.

Це означає, що повільне завершення роботи основного контейнера також затримає завершення роботи контейнерів sidecar. Якщо період очікування закінчиться до завершення процесу завершення, Pod може перейти в [примусове завершення](#pod-termination-beyond-grace-period). У цьому випадку всі залишкові контейнери в Pod будуть завершені одночасно з коротким періодом очікування.

Аналогічно, якщо Pod має хук `preStop`, який перевищує період очікування завершення, може статися аварійне завершення. Загалом, якщо ви використовували хуки `preStop` для керування порядком завершення без контейнерів sidecar, тепер ви можете видалити їх і дозволити kubelet автоматично керувати завершенням роботи контейнерів sidecar.

### Збір сміття Podʼів {#pod-garbage-collection}

Для несправних Podʼів обʼєкти API залишаються в API кластера, поки людина чи {{< glossary_tooltip term_id="controller" text="контролер" >}} явно їх не видалять.

Збірник сміття Podʼів (PodGC), який є контролером панелі управління, прибирає завершені Podʼів (із фазою `Succeeded` або `Failed`), коли кількість Podʼів перевищує налаштований поріг (визначений параметром `terminated-pod-gc-threshold` в kube-controller-manager). Це запобігає витоку ресурсів при створенні та завершенні Podʼів з часом.

Крім того, PodGC очищує будь-які Podʼи, які відповідають одній з наступних умов:

1. є осиротілими Podʼів — привʼязаними до вузла, якого вже не існує,
2. є незапланованими Podʼами у стані завершення,
3. є Podʼів у стані завершення, привʼязаними до непрацюючого вузла з позначкою [`node.kubernetes.io/out-of-service`](/docs/reference/labels-annotations-taints/#node-kubernetes-io-out-of-service),    коли ввімкнено функціонал `NodeOutOfServiceVolumeDetach`.

Коли ввімкнено функціонал `PodDisruptionConditions`, разом із прибиранням Podʼів, PodGC також позначає їх як несправнені, якщо вони перебувають в незавершеній фазі. Крім того, PodGC додає стан руйнування Podʼа під час очищення осиротілого Podʼа. Див. [стани руйнування Podʼів](/docs/concepts/workloads/pods/disruptions#pod-disruption-conditions)
для отримання докладніших відомостей.

## {{% heading "whatsnext" %}}

* Отримайте практичний досвід [прикріплення обробників до подій життєвого циклу контейнера](/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/).

* Отримайте практичний досвід [налаштування проб Liveness, Readiness та Startup](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

* Дізнайтеся більше про [обробники життєвого циклу контейнера](/docs/concepts/containers/container-lifecycle-hooks/).

* Дізнайтеся більше про [контейнери sidecar](/docs/concepts/workloads/pods/sidecar-containers/).

* Для докладної інформації про статус Podʼа та контейнера в API, перегляньте документацію API, яка охоплює [`status`](/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodStatus) для Podʼа.