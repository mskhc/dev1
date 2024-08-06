---
title: Ризики обходу сервера API Kubernetes
description: >
  Інформація про архітектуру безпеки, що стосується сервера API та інших компонентів
content_type: concept
weight: 90
---

<!-- overview -->

Сервер API Kubernetes є головним входом до кластера для зовнішніх сторін (користувачів та сервісів), що з ним взаємодіють.

У рамках цієї ролі сервер API має кілька ключових вбудованих елементів безпеки, таких як ведення логів аудити та {{< glossary_tooltip text="контролери допуску" term_id="admission-controller" >}}. Однак існують способи модифікації конфігурації або вмісту кластера, які обминають ці елементи.

Ця сторінка описує способи обходу вбудованих в сервер API Kubernetes засобів контролю безпеки, щоб оператори кластера та архітектори безпеки могли переконатися, що ці обхідні механізми адекватно обмежені.

## Статичні Podʼи {#static-pods}

{{< glossary_tooltip text="Kubelet" term_id="kubelet" >}} на кожному вузлі завантажує та безпосередньо керує будь-якими маніфестами, що зберігаються в іменованій теці або завантажуються з конкретної URL-адреси як [*статичні Podʼи*](/docs/tasks/configure-pod-container/static-pod) у вашому кластері. Сервер API не керує цими статичними Podʼами. Зловмисник з правами на запис у цьому місці може змінити конфігурацію статичних Podʼів, завантажених з цього джерела, або внести нові статичні Podʼи.

Статичним Podʼам заборонено доступ до інших обʼєктів у Kubernetes API. Наприклад, ви не можете налаштувати статичний Pod для монтування Secretʼу з кластера. Однак ці Podʼи можуть виконувати інші дії, що стосуються безпеки, наприклад, використовувати монтування з `hostPath` з підлеглого вузла.

Типово kubelet створює {{< glossary_tooltip text="дзеркальний Pod" term_id="mirror-pod">}}, щоб статичні Podʼи були видимими у Kubernetes API. Однак якщо зловмисник використовує недійсне імʼя простору імен при створенні Podʼа, він не буде видимим у Kubernetes API та може бути виявлений лише інструментами, які мають доступ до пошкоджених вузлів.

Якщо статичний Pod не пройшов контроль допуску, kubelet не зареєструє Pod у сервері API. Однак Pod все ще працює на вузлі. Для отримання додаткової інформації зверніться до [тікету kubeadm #1541](https://github.com/kubernetes/kubeadm/issues/1541#issuecomment-487331701).

### Зменшення ризиків {#static-pods-mitigations}

- Увімкніть [функціональність маніфесту статичних Podʼів kubelet](/docs/tasks/configure-pod-container/static-pod/#static-pod-creation) лише в разі необхідності для вузла.
- Якщо вузол використовує функціональність статичних Podʼів, обмежте доступ до файлової системи до теки маніфестів статичних Podʼів або URL для користувачів, які потребують такого доступу.
- Обмежте доступ до параметрів та файлів конфігурації kubelet, щоб запобігти зловмиснику встановлення шляху або URL статичного Podʼа.
- Регулярно перевіряйте та централізовано звітуйте про всі доступи до тек або місць зберігання вебсайтів, які містять маніфести статичних Podʼів та файли конфігурації kubelet.

## API kubelet {#kubelet-api}

kubelet надає HTTP API, який, як правило, відкритий на TCP-порту 10250 на вузлах робочих груп кластера. API також може бути відкритим на вузлах панелі управління залежно від дистрибутиву Kubernetes, що використовується. Прямий доступ до API дозволяє розкривати інформацію про Podʼи, що працюють на вузлі, журнали з цих Podʼів та виконання команд у кожному контейнері, що працює на вузлі.

Коли у користувачів кластера Kubernetes є доступ RBAC до ресурсів обʼєкта `Node`, цей доступ слугує авторизацією для взаємодії з API kubelet. Точний доступ залежить від того, який доступ цим ресурсам був наданий, про що детально описано в [авторизації kubelet](/docs/reference/access-authn-authz/kubelet-authn-authz/#kubelet-authorization).

Прямий доступ до API kubelet не є предметом уваги контролю допуску та не реєструється системою аудиту Kubernetes. Зловмисник з прямим доступом до цього API може здійснити обхід елементів захисту, що виявляють або запобігають певним діям.

API kubelet можна налаштувати для автентифікації запитів за допомогою кількох способів. Типово конфігурація kubelet дозволяє анонімний доступ. Більшість постачальників Kubernetes змінюють це на використання автентифікації за допомогою вебхуків та сертифікатів. Це дозволяє панелі управління перевірити, чи авторизований той хто надсилає запит має доступ до ресурсу API `nodes` або його ресурсів. Анонімний доступ типово не дає цього підтвердження панелі управління.

### Зменшення ризиків {#mitigations}

- Обмежте доступ до ресурсів обʼєкта API `nodes`, використовуючи механізми, такі як [RBAC](/docs/reference/access-authn-authz/rbac/). Надавайте цей доступ лише за необхідності, наприклад, для служб моніторингу.
- Обмежте доступ до порту kubelet. Дозволяйте доступ до порту лише зазначеним та довіреним діапазонам IP-адрес.
- Переконайтеся, що [автентифікація kubelet](/docs/reference/access-authn-authz/kubelet-authn-authz/#kubelet-authentication) налаштована на режим webhook або сертифікату.
- Переконайтеся, що неавтентифікований "тільки для читання" порт kubelet не ввімкнено в кластері.

## API etcd {#the-etcd-api}

Кластери Kubernetes використовують etcd як сховище даних. Сервіс `etcd` прослуховує TCP-порт 2379. Доступ до нього необхідний лише для сервера API Kubernetes та будь-яких інструментів резервного копіювання, які ви використовуєте. Прямий доступ до цього API дозволяє розголошення або зміну будь-яких даних, що зберігаються в кластері.

Доступ до API etcd зазвичай керується автентифікацією за допомогою сертифікатів клієнта. Будь-який сертифікат, виданий центром сертифікації, якому довіряє etcd, дозволяє повний доступ до даних, збережених всередині etcd.

Прямий доступ до etcd не підлягає контролю допуску Kubernetes і не реєструється журналом аудиту Kubernetes. Нападник, який має доступ до приватного ключа сертифіката клієнта etcd сервера API (або може створити новий довірений сертифікат клієнта), може отримати права адміністратора кластера, отримавши доступ до секретів кластера або зміни прав доступу. Навіть без підвищення привілеїв RBAC Kubernetes нападник, який може змінювати etcd, може отримати будь-який обʼєкт API або створювати нові робочі навантаження всередині кластера.

Багато постачальників Kubernetes налаштовують etcd для використання взаємного TLS (обидва, клієнт і сервер перевіряють сертифікати один одного для автентифікації). Наразі не існує загальноприйнятої реалізації авторизації для API etcd, хоча функція існує. Оскільки немає моделі авторизації, будь-який сертифікат з доступом клієнта до etcd може бути використаний для повного доступу до etcd. Зазвичай сертифікати клієнта etcd, які використовуються лише для перевірки стану, також можуть надавати повний доступ на читання та запис.

### Зменшення ризиків {#etcd-api-mitigations}

- Переконайтеся, що центр сертифікації, якому довіряє etcd, використовується лише для цілей автентифікації цього сервісу.
- Керуйте доступом до приватного ключа сертифіката сервера etcd, а також до сертифіката і ключа клієнта сервера API.
- Призначте обмеження доступу до порту etcd на рівні мережі, щоб дозволити доступ лише зазначеним і довіреним діапазонам IP-адрес.

## Сокет контейнера {#runtime-socket}

На кожному вузлі в кластері Kubernetes доступ до взаємодії з контейнерами контролюється відносно контейнерного середовища (або середовищ, якщо ви налаштували більше одного). Зазвичай контейнерне середовище відкриває сокет Unix, до якого може отримати доступ kubelet. Нападник з доступом до цього сокету може запускати нові контейнери або взаємодіяти з працюючими контейнерами.

На рівні кластера вплив цього доступу залежить від того, чи мають контейнери, що працюють на скомпрометованому вузлі, доступ до Secretʼів або інших конфіденційних даних, які нападник може використати для підвищення привілеїв на інші вузли або для управління компонентами панелі управління.

### Зменшення ризиків {#runtime-socket-mitigations}

- Переконайтеся, що ви щільно контролюєте доступ до файлової системи для сокетів контейнерного середовища. Коли це можливо, обмежте цей доступ до користувача `root`.
- Ізолюйте kubelet від інших компонентів, що працюють на вузлі, використовуючи механізми, такі як простори імен ядра Linux.
- Переконайтеся, що ви обмежуєте або забороняєте використання [монтуванню `hostPath`](/docs/concepts/storage/volumes/#hostpath), які охоплюють робочий порт контейнерного середовища, або безпосередньо, або монтуванням батьківського каталогу. Крім того, монтування `hostPath` має бути встановлено тільки для читання для зменшення ризиків обходу обмежень каталогу.
- Обмежте доступ користувачів до вузлів, особливо обмежте доступ суперкористувача до вузлів.