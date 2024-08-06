---
reviewers:
- sig-cluster-lifecycle
title: Створення високодоступних кластерів за допомогою kubeadm
content_type: task
weight: 60
---

<!-- overview -->

На цій сторінці пояснюється два різних підходи до налаштування високодоступного кластера Kubernetes з використанням інструменту kubeadm:

- Зі стековими вузлами панелі управління. Цей підхід вимагає менше інфраструктури. Члени etcd та вузли панелі управління розташовані разом.
- Зовнішній кластер etcd. Цей підхід вимагає більше інфраструктури. Вузли панелі управління та члени etcd розділені.

Перед тим як продовжити, вам слід ретельно розглянути, який підхід найкраще відповідає потребам ваших застосунків та оточенню. [Варіанти топології високої доступності](/docs/setup/production-environment/tools/kubeadm/ha-topology/) наводять переваги та недоліки кожного з них.

У випадку виникнення проблем з налаштуванням HA-кластера, будь ласка, повідомте про це в системі [відстеження проблем kubeadm](https://github.com/kubernetes/kubeadm/issues/new).

Також дивіться [документацію з оновлення](/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/).

{{< caution >}}
Ця сторінка не стосується запуску вашого кластера на платформі хмарного провайдера. У хмарному середовищі жоден із документованих тут підходів не працює з обʼєктами служб типу LoadBalancer або з динамічними PersistentVolumes.
{{< /caution >}}

## {{% heading "prerequisites" %}}

Передумови залежать від топології, яку ви обрали для панелі управління кластера:

{{< tabs name="prerequisite_tabs" >}}
{{% tab name="Стековий etcd" %}}
<!--
    note to reviewers: these prerequisites should match the start of the
    external etc tab
-->

Вам потрібно:

- Три або більше машин, які відповідають [мінімальним вимогам kubeadm](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) для вузлів панелі управління. Наявність непарної кількості вузлів панелі управління може бути корисною при виборі лідера в разі відмови машини чи зони,
  - включаючи {{< glossary_tooltip text="середовище виконання контейнерів" term_id="container-runtime" >}}, яке вже налаштоване та працює.
- Три або більше машин, які відповідають [мінімальним вимогам kubeadm](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) для робочих вузлів,
  - включаючи середовище виконання контейнерів, яке вже налаштоване та працює.
- Повноцінне мережеве зʼєднання між усіма машинами в кластері (публічна чи
  приватна мережа).
- Привілеї суперкористувача на всіх машинах за допомогою `sudo`.
  - Ви можете використовувати інший інструмент; цей посібник використовує `sudo` у прикладах.
- SSH-доступ з одного пристрою до всіх вузлів системи.
- `kubeadm` та `kubelet` вже встановлені на всіх машинах.

_Дивіться [Топологія стекового etcd](/docs/setup/production-environment/tools/kubeadm/ha-topology/#stacked-etcd-topology) для контексту._

{{% /tab %}}
{{% tab name="Зовнішній etcd" %}}
<!--
    note to reviewers: these prerequisites should match the start of the
    stacked etc tab
-->
Вам потрібно:

- Три або більше машин, які відповідають [мінімальним вимогам kubeadm](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) для вузлів панелі управління. Наявність непарної кількості вузлів панелі управління може бути корисною при виборі лідера в разі відмови машини чи зони,
  - включаючи робоче {{< glossary_tooltip text="середовище виконання контейнерів" term_id="container-runtime" >}}, яке вже налаштоване та працює
- Три або більше машин, які відповідають [мінімальним вимогам kubeadm](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) для робочих вузлів,
  - включаючи середовище виконання контейнерів контейнера, яке вже налаштоване та працює.
- Повноцінне мережеве зʼєднання між усіма машинами в кластері (публічна чи
  приватна мережа).
- Привілеї суперкористувача на всіх машинах за допомогою `sudo`.
  - Ви можете використовувати інший інструмент; цей посібник використовує `sudo` у прикладах.
- SSH-доступ з одного пристрою до всіх вузлів системи.
- `kubeadm` та `kubelet` вже встановлені на всіх машинах.

<!-- end of shared prerequisites -->

І вам також потрібно:

- Три або більше додаткових машин, які стануть членами кластера etcd. Наявність непарної кількості членів у кластері etcd — це вимога для досягнення оптимального кворуму під час голосування.
  - Ці машини також повинні мати встановлені `kubeadm` та `kubelet`.
  - На цих машинах також потрібно мати середовище виконання контейнерів, яке вже налаштоване та працює.

_Дивіться [Топологія зовнішнього etcd](/docs/setup/production-environment/tools/kubeadm/ha-topology/#external-etcd-topology) для контексту._
{{% /tab %}}
{{< /tabs >}}

### Образи контейнерів {#container-images}

Кожен хост повинен мати доступ для отримання та завантаження образів з реєстру контейнерів Kubernetes, `registry.k8s.io`. Якщо ви хочете розгорнути високодоступний кластер, де хостам не можна здійснювати доступ до образів, це можливо. Вам слід забезпечити, що правильні образи контейнерів вже доступні на відповідних хостах за допомогою інших засобів.

### Інтерфейс командного рядка {#kubectl}

Для управління Kubernetes після налаштування кластера, вам слід
[встановити kubectl](/docs/tasks/tools/#kubectl) на вашому компʼютері. Також корисно
встановити інструмент `kubectl` на кожному вузлі панелі управління, оскільки це може бути корисним для усунення несправностей.

<!-- steps -->

## Перші кроки для обох методів {#first-steps-for-both-methods}

### Створення балансувальника навантаження для kube-apiserver {#create-load-balancer-for-kube-apiserver}

{{< note >}}
Існує багато конфігурацій для балансувальників навантаження. Наведений нижче приклад — лише один із варіантів. Ваші вимоги до кластера можуть вимагати іншої конфігурації.
{{< /note >}}

1. Створіть балансувальник навантаження kube-apiserver з імʼям, яке розпізнається DNS.

   - У хмарному середовищі ви повинні розмістити вузли панелі управління за TCP балансувальником навантаження, який виконує переспрямовування трафіку. Цей балансувальник розподіляє трафік до всіх справних вузлів панелі управління у своєму списку цілей. Перевірка доступності apiserver — це перевірка TCP порту, на якому слухає kube-apiserver (типове значення порту `:6443`).

   - Не рекомендується використовувати IP-адресу безпосередньо у хмарному середовищі.

   - Балансувальник навантаження повинен мати можливість взаємодіяти з усіма вузлами панелі управління на порті apiserver. Також він повинен дозволяти вхідний трафік на його порту прослуховування.

   - Переконайтеся, що адреса балансувальника завжди відповідає адресі `ControlPlaneEndpoint` kubeadm.

   - Прочитайте [Параметри для програмного балансування навантаження](https://git.k8s.io/kubeadm/docs/ha-considerations.md#options-for-software-load-balancing) для отримання додаткових відомостей.

2. Додайте перший вузол панелі управління до балансувальника та перевірте зʼєднання:

   ```shell
   nc -v <LOAD_BALANCER_IP> <PORT>
   ```

   Помилка "connection refused" є очікуваною, оскільки API-сервер ще не запущено. Проте тайм-аут означає, що балансувальник не може взаємодіяти з вузлом панелі управління. Якщо виникає тайм-аут, повторно налаштуйте балансувальник
   для взаємодії з вузлом панелі управління.

3. Додайте решту вузлів панелі управління до цільової групи балансувальника.

## Панель управління та вузли etcd зі стековою архітектурою {#stacked-control-plane-and-etcd-nodes}

### Кроки для першого вузла панелі управління {#steps-for-the-first-control-plane-node}

1. Ініціалізуйте панель управління:

   ```sh
   sudo kubeadm init --control-plane-endpoint "LOAD_BALANCER_DNS:LOAD_BALANCER_PORT" --upload-certs
   ```

   - Ви можете використовувати прапорець `--kubernetes-version`, щоб встановити версію Kubernetes, яку слід використовувати. Рекомендується, щоб версії kubeadm, kubelet, kubectl та Kubernetes відповідали одна одній.
   - Прапорець `--control-plane-endpoint` повинен бути встановлений на адресу або DNS та порт балансувальника.

   - Прапорець `--upload-certs` використовується для завантаження сертифікатів, які слід використовувати на всіх екземплярах панелі управління. Якщо натомість ви віддаєте перевагу копіюванню сертифікатів між вузлами панелі управління вручну або за допомогою засобів автоматизації, видаліть цей прапорець та зверніться до розділу [Розподіл сертифікатів вручну](#manual-certs) нижче.

   {{< note >}}
   Прапорці `kubeadm init` `--config` та `--certificate-key` не можна змішувати, тому якщо ви хочете використовувати [конфігурацію kubeadm](/docs/reference/config-api/kubeadm-config.v1beta3/) вам слід додати поле `certificateKey` у відповідні місця конфігурації (під `InitConfiguration` та `JoinConfiguration: controlPlane`).
   {{< /note >}}

   {{< note >}}
   Деякі мережеві втулки CNI вимагають додаткової конфігурації, наприклад вказівки IP для Podʼа в форматі CIDR, тоді як інші — ні. Див. [документацію мережі CNI](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#pod-network). Щоб додати CIDR Podʼу, скористайтесь прапорцем `--pod-network-cidr`, або якщо ви використовуєте файл конфігурації kubeadm встановіть поле `podSubnet` в обʼєкті `networking` конфігурації `ClusterConfiguration`.
   {{< /note >}}

   Вивід виглядатиме десь так:

   ```sh
   ...
   You can now join any number of control-plane node by running the following command on each as a root:
       kubeadm join 192.168.0.200:6443 --token 9vr73a.a8uxyaju799qwdjv --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866 --control-plane --certificate-key f8902e114ef118304e561c3ecd4d0b543adc226b7a07f675f56564185ffe0c07

   Please note that the certificate-key gives access to cluster sensitive data, keep it secret!
   As a safeguard, uploaded-certs will be deleted in two hours; If necessary, you can use kubeadm init phase upload-certs to reload certs afterward.

   Then you can join any number of worker nodes by running the following on each as root:
       kubeadm join 192.168.0.200:6443 --token 9vr73a.a8uxyaju799qwdjv --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866
   ```

   - Скопіюйте цей вивід у текстовий файл. Ви будете потребувати його пізніше для приєднання вузлів панелі управління та робочих вузлів до кластера.
   - Коли використовується `--upload-certs` з `kubeadm init`, сертифікати основної панелі управління шифруються та завантажуються у `kubeadm-certs` Secret.
   - Щоб знову завантажити сертифікати та згенерувати новий ключ розшифрування, використовуйте наступну команду на вузлі панелі управління який вже приєднаний до кластера:

     ```sh
     sudo kubeadm init phase upload-certs --upload-certs
     ```

   - Ви також можете вказати власний `--certificate-key` під час `init`, який пізніше може бути використаний з `join`. Щоб згенерувати такий ключ, використовуйте наступну команду:

     ```sh
     kubeadm certs certificate-key
     ```

   Ключ сертифіката — це рядок, закодований у шістнадцятковій формі, який є ключем AES розміром 32 байти.

   {{< note >}}
   Секрет `kubeadm-certs` та ключ розшифрування діють впродовж двох годин.
   {{< /note >}}

   {{< caution >}}
   Як зазначено у виводі команди, ключ сертифіката надає доступ до чутливих даних кластера, тримайте його в таємниці!
   {{< /caution >}}

2. Застосуйте обраний вами мережеву втулок CNI: [Дотримуйтеся цих інструкцій](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#pod-network) для встановлення постачальника CNI. Переконайтеся, що конфігурація відповідає CIDR IP для Podʼа, вказаному в файлі конфігурації kubeadm (якщо застосовується).

   {{< note >}}
   Вам слід вибрати мережевий втулок, який відповідає вашому випадку використання та встановити його, перш ніж перейти до наступного кроку. Якщо ви цього не зробите, вам не вдасться належним чином запустити свій кластер.
   {{< /note >}}

3. Введіть наступну команду та спостерігайте, як запускаються екземпляри компонентів панелі управління:

   ```sh
   kubectl get pod -n kube-system -w
   ```

### Кроки для інших вузлів панелі управління {#steps-for-the-rest-of-the-control-plane-nodes}

Для кожного додаткового вузла панелі управління:

1. Виконайте команду приєднання, яка вам була надана раніше виводом `kubeadm init` на першому вузлі. Вона повинна виглядати приблизно так:

   ```sh
   sudo kubeadm join 192.168.0.200:6443 --token 9vr73a.a8uxyaju799qwdjv --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866 --control-plane --certificate-key f8902e114ef118304e561c3ecd4d0b543adc226b7a07f675f56564185ffe0c07
   ```

   - Прапорець `--control-plane` повідомляє `kubeadm join` створити новий вузол панелі управління.
   - Прапорець `--certificate-key ...` призведе до того, що сертифікати вузлів панелі управління будуть завантажені з секрету `kubeadm-certs` в кластері та розшифровані за допомогою вказаного ключа.

Ви можете приєднувати кілька вузлів панелі управління паралельно.

## Зовнішні вузли etcd {#external-etcd-nodes}

Налаштування кластера з зовнішніми вузлами etcd подібно до процедури, використовуваної для стекових вузлів etcd, з винятком того, що ви повинні налаштувати etcd спочатку, і ви повинні передавати інформацію про etcd у конфігураційному файлі kubeadm.

### Налаштуйте кластер etcd {#setup-the-etcd-cluster}

1. Слідуйте цим [інструкціям](/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/) для налаштування кластера etcd.

1. Налаштуйте SSH, як описано [тут](#manual-certs).

1. Скопіюйте наступні файли з будь-якого вузла etcd в кластері на перший вузол панелі управління:

   ```sh
   export CONTROL_PLANE="ubuntu@10.0.0.7"
   scp /etc/kubernetes/pki/etcd/ca.crt "${CONTROL_PLANE}":
   scp /etc/kubernetes/pki/apiserver-etcd-client.crt "${CONTROL_PLANE}":
   scp /etc/kubernetes/pki/apiserver-etcd-client.key "${CONTROL_PLANE}":
   ```

   - Замініть значення `CONTROL_PLANE` на `user@host` першого вузла панелі управління.

### Налаштуйте перший вузол панелі управління {#setup-the-first-control-plane-node} 

1. Створіть файл із назвою `kubeadm-config.yaml` із наступним змістом:

   ```yaml
   ---
   apiVersion: kubeadm.k8s.io/v1beta3
   kind: ClusterConfiguration
   kubernetesVersion: stable
   controlPlaneEndpoint: "LOAD_BALANCER_DNS:LOAD_BALANCER_PORT" # змініть це (див. нижче)
   etcd:
     external:
       endpoints:
         - https://ETCD_0_IP:2379 # змініть ETCD_0_IP відповідно
         - https://ETCD_1_IP:2379 # змініть ETCD_1_IP відповідно
         - https://ETCD_2_IP:2379 # змініть ETCD_2_IP відповідно
       caFile: /etc/kubernetes/pki/etcd/ca.crt
       certFile: /etc/kubernetes/pki/apiserver-etcd-client.crt
       keyFile: /etc/kubernetes/pki/apiserver-etcd-client.key
   ```

   {{< note >}}
   Різниця між stacked etcd та external etcd полягає в тому, що налаштування external etcd потребує конфігураційного файлу з endpointʼами etcd в обʼєкті `external` для `etcd`. У випадку топології stacked etcd це вирішується автоматично.
   {{< /note >}}

   - Замініть наступні змінні в шаблоні конфігурації на відповідні значення для вашого кластера:

     - `LOAD_BALANCER_DNS`
     - `LOAD_BALANCER_PORT`
     - `ETCD_0_IP`
     - `ETCD_1_IP`
     - `ETCD_2_IP`

Наступні кроки схожі на налаштування stacked etcd:

1. Виконайте команду `sudo kubeadm init --config kubeadm-config.yaml --upload-certs` на цьому вузлі.

1. Запишіть вихідні команди для приєднання, які повертаються, у текстовий файл для подальшого використання.

1. Застосуйте обраний вами втулок CNI.

   {{< note >}}
   Ви повинні вибрати мережевий втулок, який відповідає вашому випадку використання та розгорнути його, перш ніж перейдете до наступного кроку. Якщо цього не зробити, ви не зможете належним чином запустити ваш кластер.
   {{< /note >}}

### Кроки для інших вузлів панелі управління {#steps-for-the-rest-of-the-control-plane-nodes}

Кроки аналогічні налаштуванню для stacked etcd:

- Переконайтеся, що перший вузол панелі управління повністю ініціалізований.
- Приєднайте кожен вузол панелі управління за допомогою команди приєднання, яку ви зберегли в текстовий файл. Рекомендується приєднувати вузли панелі управління по одному.
- Не забудьте, що ключ розшифрування з параметром `--certificate-key` діє дві години.

## Загальні завдання після налаштування панелі управління {#common-tasks-after-bootstraping-control-plane}

### Встановлення робочих вузлів {#installing-workers}

Робочі вузли можна приєднати до кластера за допомогою команди, яку ви зберегли раніше як вивід з команди `kubeadm init`:

```sh
sudo kubeadm join 192.168.0.200:6443 --token 9vr73a.a8uxyaju799qwdjv --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866
```

## Ручне поширення сертифікатів {#manual-certs}

Якщо ви вирішили не використовувати `kubeadm init` з параметром `--upload-certs`, це означає, що вам доведеться вручну скопіювати сертифікати з первинного вузла панелі управління до приєднуваних вузлів панелі.

Є багато способів це зробити. У наступному прикладі використовуються `ssh` та `scp`:

SSH потрібен, якщо ви хочете керувати всіма вузлами з одного пристрою.

1. Активуйте ssh-agent на своєму основному пристрої, який має доступ до всіх інших вузлів в системі:

   ```shell
   eval $(ssh-agent)
   ```

1. Додайте свій SSH-ідентифікатор до сеансу:

   ```shell
   ssh-add ~/.ssh/path_to_private_key
   ```

1. Перемикайтесь між вузлами, щоб перевірити, чи зʼєднання правильно працює.

   - Коли ви входите в будь-який вузол через SSH, додайте прапорець `-A`. Цей прапорець дозволяє вузлу, на який ви увійшли за допомогою SSH, отримувати доступ до агента SSH на вашому ПК. Розгляньте альтернативні методи, якщо ви не повністю довіряєте безпеці вашої сесії користувача на вузлі.

     ```shell
     ssh -A 10.0.0.7
     ```

   - Коли використовуєте sudo на будь-якому вузлі, обовʼязково зберігайте середовище, щоб SSH forwarding працював:

     ```shell
     sudo -E -s
     ```

1. Після налаштування SSH на всіх вузлах ви повинні запустити наступний скрипт на першому вузлі панелі управління після запуску `kubeadm init`. Цей скрипт скопіює сертифікати з першого вузла панелі управління на інші вузли панелі:

   У наступному прикладі замініть `CONTROL_PLANE_IPS` на IP-адреси інших вузлів панелі управління.

   ```sh
   USER=ubuntu # налаштовується
   CONTROL_PLANE_IPS="10.0.0.7 10.0.0.8"
   for host in ${CONTROL_PLANE_IPS}; do
       scp /etc/kubernetes/pki/ca.crt "${USER}"@$host:
       scp /etc/kubernetes/pki/ca.key "${USER}"@$host:
       scp /etc/kubernetes/pki/sa.key "${USER}"@$host:
       scp /etc/kubernetes/pki/sa.pub "${USER}"@$host:
       scp /etc/kubernetes/pki/front-proxy-ca.crt "${USER}"@$host:
       scp /etc/kubernetes/pki/front-proxy-ca.key "${USER}"@$host:
       scp /etc/kubernetes/pki/etcd/ca.crt "${USER}"@$host:etcd-ca.crt
       # Пропустіть наступний рядок, якщо використовуєте зовнішній etcd
       scp /etc/kubernetes/pki/etcd/ca.key "${USER}"@$host:etcd-ca.key
   done
    ```

   {{< caution >}}
   Копіюйте лише сертифікати в переліку вище. kubeadm буде опікуватись генеруванням решти сертифікатів з необхідними SAN для приєднання екземплярів панелі управління. Якщо ви помилитесь при копіюванні всіх сертифікатів, створення додаткових вузлів може зазнати невдачі через відсутність необхідних SAN.
   {{< /caution >}}

1. Потім на кожному приєднуваному вузлі панелі управління вам слід виконати наступний скрипт перед виконанням `kubeadm join`. Цей скрипт перемістить раніше скопійовані сертифікати з домашньої теки в `/etc/kubernetes/pki`:

   ```sh
   USER=ubuntu # налаштовується
   mkdir -p /etc/kubernetes/pki/etcd
   mv /home/${USER}/ca.crt /etc/kubernetes/pki/
   mv /home/${USER}/ca.key /etc/kubernetes/pki/
   mv /home/${USER}/sa.pub /etc/kubernetes/pki/
   mv /home/${USER}/sa.key /etc/kubernetes/pki/
   mv /home/${USER}/front-proxy-ca.crt /etc/kubernetes/pki/
   mv /home/${USER}/front-proxy-ca.key /etc/kubernetes/pki/
   mv /home/${USER}/etcd-ca.crt /etc/kubernetes/pki/etcd/ca.crt
   # Пропустіть наступний рядок, якщо використовуєте зовнішній etcd
   mv /home/${USER}/etcd-ca.key /etc/kubernetes/pki/etcd/ca.key
   ```