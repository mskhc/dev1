---
title: Розширення можливостей Kubernetes
weight: 999 # this section should come last
description: Різні способи зміни поведінки вашого кластера Kubernetes.
reviewers:
- erictune
- lavalamp
- cheftako
- chenopis
feature:
  title: Створенно щоб розширюватись
  description: >
    Додавайте можливості до свого кластеру Kubernetes без зміни сирців.
content_type: concept
no_list: true
---

<!-- overview -->

Kubernetes добре налаштовується та розширюється. Тому випадки, коли вам потрібно робити форки та накладати патчі на Kubernetes, щоб змінити його поведінку, дуже рідкісні.

Цей розділ описує різні способи зміни поведінки вашого кластера Kubernetes. Він призначений для {{< glossary_tooltip text="операторів" term_id="cluster-operator" >}}, які хочуть зрозуміти, як адаптувати кластер до своїх потреб свого робочого оточення. Розробники, які є потенційними {{< glossary_tooltip text="розробниками платформ" term_id="platform-developer" >}} чи {{< glossary_tooltip text="учасники" term_id="contributor" >}} проєкту Kubernetes, також знайдуть цей розділ корисним як вступ до того, які точки та шаблони розширення існують, а також їх компроміси та обмеження.

Підходи до налаштувань можна взагалі розділити на [конфігурацію](#configuration), яка включає лише зміну аргументів командного рядка, локальних конфігураційних файлів або ресурсів API; та [розширення](#extensions), яке передбачає виконання додаткових програм, додаткових мережевих служб або обох. Цей документ в основному присвячений _розширенням_.

<!-- body -->

## Конфігурація {#configuration}

*Конфігураційні файли* та _аргументи командного рядка_ описані в розділі [Довідник](/docs/reference/) онлайн-документації, де кожен  файл має свою сторінку:

* [`kube-apiserver`](/docs/reference/command-line-tools-reference/kube-apiserver/)
* [`kube-controller-manager`](/docs/reference/command-line-tools-reference/kube-controller-manager/)
* [`kube-scheduler`](/docs/reference/command-line-tools-reference/kube-scheduler/)
* [`kubelet`](/docs/reference/command-line-tools-reference/kubelet/)
* [`kube-proxy`](/docs/reference/command-line-tools-reference/kube-proxy/)

Аргументи команд та файли конфігурації не завжди можуть бути змінені в службі Kubernetes, що надається постачальником, або дистрибутиві з керованою установкою. Коли їх можна змінювати, вони, як правило, змінюються лише оператором кластера. Крім того, вони можуть бути змінені в майбутніх версіях Kubernetes, і для їх налаштування може знадобитися перезапуск процесів. З цих причин їх слід використовувати лише тоді, коли немає інших варіантів.

Вбудовані _API політики_, такі як [ResourceQuota](/docs/concepts/policy/resource-quotas/), [NetworkPolicy](/docs/concepts/services-networking/network-policies/) та доступ на основі ролей ([RBAC](/docs/reference/access-authn-authz/rbac/)), є вбудованими API Kubernetes, які надають можливості декларативного налаштування політик. API є доступними та в кластерах, які надаються провайдером, і в кластерах, якими ви керуєте самостійно. Вбудовані API політик використовують ті ж самі конвенції, що й інші ресурси Kubernetes, такі як Podʼи. Коли ви використовуєте [стабільний](/docs/reference/using-api/#api-versioning) API політик, ви отримуєте зиск від [визначеної підтримки політик](/docs/reference/using-api/deprecation-policy/) так само як й інші API Kubernetes. З цих причин використання API політик рекомендується на перевагу до _конфігураційних файлів_ та _аргументів командного рядка_, де це можливо.

## Розширення {#extensions}

Розширення — це компонент програмного забезпечення, який глибоко інтегрується з Kubernetes. Вони використовуються для додавання нових типів ресурсів та видів апаратного забезпечення.

Багато адміністраторів класів Kubernetes використовують кластери, що надаються провайдерами, чи встановленими з дистрибутивів. Ці кластери вже йдуть з розширеннями. В результаті, більшість користувачів Kubernetes не потребують встановлення розширень та дуже невелика частка потребує їх створення.

## Шаблони розширень {#extension-patterns}

Kubernetes спроєктовано так, щоб він був автоматизований шляхом створення клієнтських застосунків. Будь-яка програма, яка може писати та читати з API Kubernetes, може надавати корисні функції автоматизації. Ці функції можуть працювати як всередині кластера, так і ззовні. Слідуючи настановам з цього посібника, ви зможете створити надійні та високопродуктивні розширення. Автоматизація, як правило, працює з будь-яким кластером Kubernetes, незалежно від того, як він був встановлений.

Існує конкретний патерн написання клієнтських програм, які ефективно взаємодіють із Kubernetes, відомий як {{< glossary_tooltip term_id="controller" text="патерн контролера" >}}. Зазвичай контролери читають `.spec` обʼєкта, можливо виконують певні операції, а потім оновлюють `.status` обʼєкта. 

Контролери є клієнтами API Kubernetes. Коли Kubernetes сам є клієнтом та звертається до віддаленого сервісу, виклики Kubernetes є *вебхуками*. Віддалений сервіс називається *вебхук-бекендом*. Так само як і стороні контролери, вебхуки додають ще одну точку вразливості.

{{< note >}}
Поза Kubernetes, термін «вебхук» зазвичай означає механізм асинхронного сповіщення, де вебхук звертається до сервісу з одностороннім сповіщенням до іншої системи чи компонента. В екосистемі Kubernetes, навіть асинхронний HTTP-запит часто описується як «вебхук».
{{< /note >}}

В моделі вебхуків, Kubernetes надсилає мережеві запити до віддалених сервісів. Альтернативою є модель *бінарних втулків*, коли Kubernetes виконує бінарник (застосунок). Бінарні втулки використовуються в kublet (наприклад, [втулок зберігання CSI](https://kubernetes-csi.github.io/docs/) та [втулок мережі CNI](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)), а також в kubeсtl (дивітьс [розширення kubectl за допомогою втулків](/docs/tasks/extend-kubectl/kubectl-plugins/)).

### Точки розширення {#extension-points}

На цій діаграмі показано точки розширення в кластері Kubernetes та клієнти з доступом до них.

<!-- image source: https://docs.google.com/drawings/d/1k2YdJgNTtNfW7_A8moIIkij-DmVgEhNrn3y2OODwqQQ/view -->

{{< figure src="/docs/concepts/extend-kubernetes/extension-points.png" alt="Символічне представлення семи пронумерованих точок розширення для Kubernetes." class="diagram-large" caption="Точки розширення Kubernetes" >}}

#### Пояснення до діаграми {#key-to-the-figure}

1. Користувачі часто взаємодіють з API Kubernetes через `kubectl`. [Втулки](#clent-extensions) підлаштовують поведінку клієнтів. Існують загальні розширення, які можна використовувати з будь-якими клієнтами, так само як і специфічні розширення для `kubectl`.

1. API сервер обробляє запити. Різні типи точок розширення на сервері API дозволяють автентифікувати запити або блокувати їх на основі їх вмісту, редагувати вміст та обробляти видалення. Про це в розділі [розширення API доступу](#api-access-extensions).

1. API сервер також обслуговує різні типи ресурсів. *Вбудовані типи ресурсі*, такі як `Pod`, визначені проєктом Kubernetes та не можуть бути змінені. Дивіться [розширення API](#api-extensions) щоб дізнатися про можливості розширення API.

2. Планувальник [вирішує](/docs/concepts/scheduling-eviction/assign-pod-node/) на якому вузлі запустити кожний Pod. Існує кілька способів розширити планування, про це в розділі [розширення планувальника](#scheduler-extensions).

3. Більшість варіантів поведінки Kubernetes реалізовано через {{< glossary_tooltip term_id="controller" text="контролери" >}}, які є клієнтами API сервера. Контролери часто використовуються разом з нестандартними ресурсами. Дивіться [поєднання нових API з автоматизаціями](#combining-new-apis-with-automation) та [зміна вбудованих ресурсів](#changing-built-in-resources), щоб дізнатися більше.

4. Kublet виконує контейнери на вузлах, та допомагає Podʼами виглядати як вірутальні сервери з їх власними IP в мережі кластера. [Мережеві втулки](#network-plugins) дозволяють реалізувати різні мережеві моделі.

5. Ви можете використовувати [втулки пристроїв](#device-plugins) для використання спеціалізованих пристроїв або інших розташованих на вузлах ресурсів, та робити їх доступними для Podʼів у вашому кластері. Kublent містить підтримку для роботи з втулками пристроїв.

   Kublet також монтує {{< glossary_tooltip term_id="volume" text="томи" >}} для Podʼів та їх контейнерів. [Втулки зберігання](#storage-plugins) дозволяють реалізувати різні моделі зберігання.

#### Вибір точки розширення {#extension-flowchart}

Якщо ви вагаєтесь звідки розпочати, ця діаграма може допомогти вам. Зауважте, що деякі рішення можуть включати кілька типів розширень.

<!-- image source for flowchart: https://docs.google.com/drawings/d/1sdviU6lDz4BpnzJNHfNpQrqI9F19QZ07KnhnxVrp2yg/edit -->

{{< figure src="/docs/concepts/extend-kubernetes/flowchart.svg" alt="Flowchart with questions about use cases and guidance for implementers. Green circles indicate yes; red circles indicate no." class="diagram-large" caption="Діаграма-посібник для вибору методу розширення." >}}

---

## Розширення клієнта {#clent-extensions}

Втулки до `kubectl` дозволяють є окремими програмами, які можуть додавати чи замінувати поведінку певних команд. `kubectl` може інтегруватись з [втулком облікових даних](/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins). Ці розширення впливають лише на локальне оточення користувача і не можуть додавати нові політики до кластера.

Якщо ви бажаєте розширити `kubectl`, ознаиомтесь з [розширення kubectl за допомогою втулків](/docs/tasks/extend-kubectl/kubectl-plugins/).

## Розширення API {#api-extensions}

### Визначення власних ресурсів {#custom-resource-definitions}

Зважте на додавання _власних ресурсів_ у Kubernetes, якщо ви бажаєте визначити нові контролери, обʼєкти налаштування застосунків або інші декларативні API, та керувати ними використовуючи інструменти подібні до `kubectl`.

Докладніше про Custom Resource дивіться в [розділі Custom Resources](/docs/concepts/extend-kubernetes/api-extension/custom-resources/).

### Шар агрегації API {#api-aggregation-layer}

Ви можете використовувати [шар агрегації API](/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/) Kubernetes, щоб додати нові ресурси до API Kubernetes разом з додатковими службами, такими як [метрики](/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/).

### Поєднання нових API з автоматизаціями {#combining-new-apis-with-automation}

Поєднання API власних ресурсів та циклів управління називається шаблонами {{< glossary_tooltip term_id="controller" text="контролерів" >}}. Якщо ваш контролер виконує функції оператора-людини, та розгортає інфраструктуру на основі бажаного стану, то, можливо, він також дотримується {{< glossary_tooltip term_id="operator-pattern" text="шаблону оператора" >}}. Шаблон Оператор використовується для управління конкретними застосунками; зазвичай це застосунки, які підтримують стан та вимагають уважного управління.

Ви також можете створювати власні API та цикли управління, які керують іншими ресурсами, такими як сховище, або визначають політики (наприклад, обмеження контролю доступу).

### Зміна вбудованих ресурсів {#changing-built-in-resources}

Коли ви розширюєте API Kubernetes шляхом додавання власних ресурсів, ці ресурси завжди потрапляють до нової групи API. Ви не можете замінити чи змінити наявні групи API. Додавання API напряму не впливає на поведінку наявних API (таких як Podʼи), однак мають вплив на розширення API доступу.

## Розширення API доступу {#api-access-extensions}

Коли запит потрапляє до API сервера Kubernetes, він спочатку _автентифікується_, потім _авторизується_, і потім він потрапляє до _перевірки допуску (admission control)_ (по факту деякі запити є неавтентифікованими та отримують особливу обробку). Дивіться розділ про [керування доступу до API Kubernetes](/docs/concepts/security/controlling-access/) для отримання деталей.

Кожен крок в процесі автентифікації/авторизації пропонує точки розширення.

### Автентифікація {#authentication}

[Автентифікація](/docs/reference/access-authn-authz/authentication/) зіставляє заголовки або сертифікати усіх запитів з користувачами, які зробили запит.

Kubernetes має кілька вбудованих методів автентифікації. Крім того, він може знаходитись поза проксі-сервером автентифікації та може надсилати токени з заголовком `Authorization` до інших віддалених служб для перевірки ([вебхуки автентифікації](/docs/reference/access-authn-authz/authentication/#webhook-token-authentication)), якщо вбудовані методи не підходять.

### Авторизація {#authorization}

[Авторизація](/docs/reference/access-authn-authz/authorization/) визначає, чи має користувач право читати, писати чи виконувати інші дії з ресурсами API. Це відбувається на рівні всього ресурсу, а не на рівні окремих обʼєктів.

Якщо вбудовані методи авторизації не підходять, Kubernetes може використовувати [вебхуки авторизації](/docs/reference/access-authn-authz/webhook/), що дозволяють викликати власний код для визначення, чи має користувач право виконувати дію.

### Динамічний контроль допуску {#dynamic-admission-control}

Після того, як запит пройшов та авторизацію, і якщо це операція запису, він також проходить через крок [контролю допуску](/docs/reference/access-authn-authz/admission-controllers/). На додачу до вбудованих кроків, є кілька розширень:

* [Вебхуки політик образів](/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook) дозволяють визначити, які образи можуть бути запущені в контейнерах.
* Для прийняття довільних рішень щодо допуску можуть використовуватись загальні [вебхуки допуску](/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks). Деякі з вебхуків допуску змінюють дані вхідних запитів до того, як вони будуть опрацьовані Kubernetes.

## Розширення інфраструктури {#infrastructure-extensions}

### Втулки пристроїв {#device-plugins}

_Втулки пристроїв_ дозволяють вузлам знаходити нові ресурси Node (на додачу до вбудованих, таких як ЦП та памʼять) за допомогою [Втулків пристроїв](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/).

### Втулки зберігання {#storage-plugins}

Втулок {{< glossary_tooltip term_id="csi" text="Container Storage Interface" >}} (CSI) надає спосіб розширювати Kubernetes шляхом підтримки нових типів сховищ. Томи можуть знаходитись в надійних зовнішніх системах зберігання, або впроваджувати ефемерні пристрої зберігання, або можуть надавити read-only інтерфейс до інформації використовуючи парадигму роботи з файловою системою.

Kubernetes має підтримку втулків [FlexVolume](/docs/concepts/storage/volumes/#flexvolume), які вже визнані застаріилими у v1.23 (на користь CSI).

FlexVolume дозволяв користувачам монтувати типи томів які не підтримувались самим Kubernetes. Коли ви запускали Pod, що вимагав FlexVolume, kublet викликав відповідний FlexVolume драйвер, який виконував монтування томів. Архівована пропозиція з проєктування [FlexVolume](https://git.k8s.io/design-proposals-archive/storage/flexvolume-deployment.md) містить більше докладної інформації про те, як все мало відбуватись.

[ЧаПи про втулки роботи з томами в Kubernetes для постачальників рішень](https://github.com/kubernetes/community/blob/master/sig-storage/volume_plugins-faq.md#kubernetes-volume-plugins-faq-for-storage-vendors) містить загальні відомості про втулки роботи з томами в Kubernetes.

### Мережеві втулки {#network-plugins}

Ваш кластер Kubernetes потребує _мережеві втулки_ для того, щоб мати робочу мережу для ваших Podʼів та підтримки аспектів мережевої моделі Kubernetes.

[Мережеві втулки](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/) дозволяють Kubernetes працювати з різними мережевими топологіями та технологіями.

### Втулки kublet image credential provider {#kublet-image-credential-provider-plugins}

{{< feature-state for_k8s_version="1.26" state="stable" >}}

Втулки kublet image credential provider дозволяють динамічно отримувати облікові дані для образів контейнерів з різних джерел. Облікові дані можуть бути використані для отримання образів контейнерів, які відповідають поточній конфігурації.

Втулки можуть спілкуватись з зовнішніми службами чи використовувати локальні файли для отримання облікових даних. В такому разу kublet не треба мати статичні облікові дані для кожного реєстру, і він може підтримувати різноманітні методи та протоколи автентифікації.

Щоб дізнатись про параметри налаштування втулка дивіться [налаштування kubelet image credential provider](/docs/tasks/administer-cluster/kubelet-image-credential-provider/).

## Розширення планувальника {#scheduling-extensions}

Планувальник є спеціальним типом контролера, який вирішує, на якому вузлі запустити який Pod. Стандартний планувальник можна повністю замінити, продовжуючи використовувати інші компоненти Kubernetes, або ж [кілька планувальників](/docs/tasks/extend-kubernetes/configure-multiple-schedulers/) можуть працювати разом.

Це значне завдання, і майже всі користувачі Kubernetes вважають, що їм не потрібно змінювати планувальник.

Ви можете контролювати активність [втулків планувальника](/docs/reference/scheduling/config/#scheduling-plugins) або асоціювати набори втулків з різними іменованими [профілями планування](/docs/reference/scheduling/config/#multiple-profiles). Ви також можете створювати свої власні втулки, які інтегруються з однією або кількома [точками розширення](/docs/concepts/scheduling-eviction/scheduling-framework/#extension-points) kube-scheduler.

Зрештою, вбудований компонент `kube-scheduler` підтримує [вебхуки](https://git.k8s.io/design-proposals-archive/scheduling/scheduler_extender.md), що дозволяє віддаленому HTTP-бекенду (розширенню планувальника) фільтрувати та/або пріоритизувати вузли, які kube-scheduler обирає для Podʼів.

{{< note >}}
Ви можете впливати лише на фільтрування вузлів та їх пріоритизацію за допомогою вебхуків розширювача планувальника; інші точки розширення через інтеграцію вебхука не доступні.
{{< /note >}}

## {{% heading "whatsnext" %}}

* Дізнайтеся більше про розширення інфраструктури
  * [Втулки пристроїв](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
  * [Мережеві втулки](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
  * [Втулки зберігання](https://kubernetes-csi.github.io/docs/) CSI
* Дізнайтеся про [втулки kubectl](/docs/tasks/extend-kubectl/kubectl-plugins/)
* Дізнайтеся більше про [власні ресурси](/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* Дізнайтеся більше про [розширення API сервера](/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
* Дізнайтеся про [Динамічний контроль допуску](/docs/reference/access-authn-authz/extensible-admission-controllers/)
* Дізнайтеся про [шаблон Оператора](/docs/concepts/extend-kubernetes/operator/)