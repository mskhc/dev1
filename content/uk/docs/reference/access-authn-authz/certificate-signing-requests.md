---
reviewers:
- liggitt
- mikedanese
- munnerz
- enj
title: Сертифікати та запити на їх підписування
api_metadata:
- apiVersion: "certificates.k8s.io/v1"
  kind: "CertificateSigningRequest"
  override_link_text: "CSR v1"
- apiVersion: "certificates.k8s.io/v1alpha1"
  kind: "ClusterTrustBundle"
content_type: concept
weight: 60
---

<!-- overview -->

API для сертифікатів та наборів довіри Kubernetes дозволяють автоматизувати створення облікових даних X.509, надаючи програмний інтерфейс для клієнтів API Kubernetes для запиту та отримання X.509 {{< glossary_tooltip term_id="certificate" text="сертифікатів" >}} від Центру сертифікації (CA).

Також є експериментальна (альфа) підтримка розподілу [наборів довіри](#cluster-trust-bundles).

<!-- body -->

## Запити на підписання сертифікатів {#certificate-signing-requests}

{{< feature-state for_k8s_version="v1.19" state="stable" >}}

Ресурс CertificateSigningRequest (CSR) використовується для запиту підписання сертифіката від вказаного підписувача, після чого запит може бути схвалений або відхилений перед остаточним підписанням.

### Процес підписання запиту {#request-signing-process}

Ресурс типу CertificateSigningRequest дозволяє клієнту запросити видачу сертифіката X.509 на основі запиту на підписання. Обʼєкт CertificateSigningRequest містить PEM-кодований запит на підпис у форматі PKCS#10 у полі `spec.request`. CertificateSigningRequest вказує підписувача (одержувача, до якого робиться запит) за допомогою поля `spec.signerName`. Зверніть увагу, що після версії API `certificates.k8s.io/v1` ключ `spec.signerName` є обовʼязковим. У Kubernetes v1.22 та пізніших версіях клієнти можуть за бажанням встановити поле `spec.expirationSeconds`, щоб запросити певний термін дії виданого сертифіката. Мінімальне допустиме значення для цього поля — `600`, тобто десять хвилин.

Після створення CertificateSigningRequest його необхідно схвалити перед підписанням. Залежно від обраного підписувача, CertificateSigningRequest може бути автоматично схвалений контролером. В іншому випадку CertificateSigningRequest слід схвалити вручну через API REST (або client-go) або за допомогою команди `kubectl certificate approve`. Аналогічно CertificateSigningRequest також може бути відхилений, що повідомляє налаштованому підписувачу, що він не повинен підписати запит.

Для схвалених сертифікатів наступним кроком є підписання. Відповідний контролер підпису перевіряє, чи виконуються умови підписання, а потім створює сертифікат. Після цього контролер підпису оновлює CertificateSigningRequest, зберігаючи новий сертифікат у полі `status.certificate` наявного обʼєкта CertificateSigningRequest. Поле `status.certificate` CertificateSigningRequest може бути порожнім або містити сертифікат X.509, кодований у форматі PEM. Поле `status.certificate` CertificateSigningRequest залишається порожнім, доки підписувач не зробить це.

Після заповнення поля `status.certificate` запит вважається завершеним, і клієнти тепер можуть отримати PEM-дані підписаного сертифіката з ресурсу CertificateSigningRequest. Підписувачі також можуть відхилити підпис сертифіката, якщо умови схвалення не виконані.

Для зменшення кількості застарілих ресурсів CertificateSigningRequest в кластері періодично запускається контролер збору сміття. Він видаляє CertificateSigningRequests, які не змінювали стан протягом певного періоду:

* Схвалені запити: автоматично видаляються після 1 години
* Відхилені запити: автоматично видаляються після 1 години
* Невдалі запити: автоматично видаляються після 1 години
* Запити в очікуванні: автоматично видаляються після 24 годин
* Усі запити: автоматично видаляються після того, як видача сертифіката закінчиться після спливання часу дії

### Авторизація підпису сертифікатів {#authorization}

Для можливості створення запиту на підпис сертифіката та отримання будь-якого запиту на підпис сертифіката:

* Дієслова: `create`, `get`, `list`, `watch`, група: `certificates.k8s.io`, ресурс: `certificatesigningrequests`

Наприклад:

{{% code_sample file="access/certificate-signing-request/clusterrole-create.yaml" %}}

Для можливості схвалення запиту на підпис сертифіката:

* Дієслова: `get`, `list`, `watch`, група: `certificates.k8s.io`, ресурс: `certificatesigningrequests`
* Дієслова: `update`, група: `certificates.k8s.io`, ресурс: `certificatesigningrequests/approval`
* Дієслова: `approve`, група: `certificates.k8s.io`, ресурс: `signers`, resourceName: `<signerNameDomain>/<signerNamePath>` або `<signerNameDomain>/*`

Наприклад:

{{% code_sample file="access/certificate-signing-request/clusterrole-approve.yaml" %}}

Для можливості підписання запиту на підпис сертифіката:

* Дієслова: `get`, `list`, `watch`, група: `certificates.k8s.io`, ресурс: `certificatesigningrequests`
* Дієслова: `update`, група: `certificates.k8s.io`, ресурс: `certificatesigningrequests/status`
* Дієслова: `sign`, група: `certificates.k8s.io`, ресурс: `signers`, resourceName: `<signerNameDomain>/<signerNamePath>` або `<signerNameDomain>/*`

{{% code_sample file="access/certificate-signing-request/clusterrole-sign.yaml" %}}

## Підписувачі {#signers}

Підписувачі абстрактно представляють сутність або сутності, які можуть підписувати або вже підписали сертифікат.

Будь-який підписувач, який доступний за межами конкретного кластера, повинен надавати інформацію про те, як працює підписувач, щоб споживачі могли зрозуміти, що це означає для CertificateSigningRequests та (якщо це увімкнено) [ClusterTrustBundles](#cluster-trust-bundles). Це охоплює:

1. **Розподіл довіри**: як розподіляються якорі довіри (CA-сертифікати або набори сертифікатів).
2. **Дозволені субʼєкти**: будь-які обмеження та поведінка, коли запитано недопустимий субʼєкт.
3. **Дозволені розширення x509**: включаючи IP subjectAltNames, DNS subjectAltNames, Email subjectAltNames, URI subjectAltNames тощо, та поведінка, коли запитано недопустиме розширення.
4. **Дозволені використання ключів / розширені використання ключів**: будь-які обмеження та поведінка, коли використання, відмінне від використання, визначеного підписувачем, вказане в CSR.
5. **Термін дії / термін життя сертифіката**: чи він фіксується підписувачем, настроюваний адміністратором, визначений полем `spec.expirationSeconds` CSR тощо, та поведінка, коли термін дії, визначений підписувачем, відрізняється від поля `spec.expirationSeconds` CSR.
6. **Дозволені / заборонені прапорці CA**: та поведінка, якщо CSR містить запит на отримання сертифіката CA, коли підписувач не пропускає його.

Зазвичай поле `status.certificate` обʼєкта CertificateSigningRequest містить один PEM-кодований сертифікат X.509, як тільки CSR схвалено, і сертифікат видається. Деякі підписувачі зберігають кілька сертифікатів у полі `status.certificate`. У цьому випадку документація для підписувача повинна вказувати значення додаткових сертифікатів; наприклад, це може бути сертифікат плюс проміжні сертифікати, які представляються під час рукостискання TLS.

Якщо ви хочете зробити _якір довіри_ (кореневий сертифікат) доступним, це слід зробити окремо від CertificateSigningRequest та його поля `status.certificate`. Наприклад, ви можете використовувати ClusterTrustBundle.

Формат підпису PKCS#10 не має стандартного механізму для вказання терміну дії або терміну життя сертифіката. Термін дії або термін життя має бути встановлено через поле `spec.expirationSeconds` обʼєкта CSR. Вбудовані підписувачі використовують параметр конфігурації `ClusterSigningDuration`, який стандартно становить 1 рік, (прапорець командного рядка `--cluster-signing-duration` kube-controller-manager) в як стандартне значення, коли не вказано `spec.expirationSeconds`. Коли вказано `spec.expirationSeconds`, використовується мінімум з `spec.expirationSeconds` та `ClusterSigningDuration`.

{{< note >}}
Поле `spec.expirationSeconds` було додано в Kubernetes v1.22. У попередніх версіях Kubernetes це поле не враховується. API-сервери Kubernetes до v1.22 будуть мовчки видаляти це поле при створенні обʼєкта.
{{< /note >}}

### Підписувачі Kubernetes {#kubernetes-signers}

Kubernetes надає вбудовані підписувачі для підпису сертифікатів, кожен з яких має широко відоме імʼя підписувача `signerName`:

1. `kubernetes.io/kube-apiserver-client`: підписує сертифікати, які мають вважатись сертифікатами клієнтів сервером API. Ніколи автоматично не затверджуються {{< glossary_tooltip term_id="kube-controller-manager" >}}.
   1. Розподіл довіри: підписані сертифікати мають вважатись клієнтськими сертифікатами для доступу до API-сервера. Набір ЦС не поширюється жодним іншим способом.
   2. Дозволені субʼєкти: немає обмежень для субʼєктів, однак затверджувачі та підписувачі можуть відхилити запити на затвердження та підпис. Певні субʼєкти подібні до користувачів та груп на рівні кластера є різними поміж різними дистрибутивами, що вимагає додаткових перевірок перед затвердженням та підписуванням. Втулок допуску `CertificateSubjectRestrictions` є стандартно увімкненим для обмеження `system:masters`, але в кластері є не тільки субʼєкти рівня адміністраторів кластера.
   3. Дозволені розширення x509: враховують subjectAltNames та використання ключів, відкидаючи інші розширення.
   4. Використання дозволених ключів: мають включати `["client auth"]`. Не мають містити використання ключів поза `["digital signature", "key encipherment", "client auth"]`.
   5. Термін дії / термін життя сертифіката: для реалізації підписувача kube-controller-manager, встановлюється у мінімальне значення з `--cluster-signing-duration` або, якщо вказано, поля `spec.expirationSeconds` обʼєкта CSR.
   6. Біт ЦС дозволено / заборонено: не дозволяється.

2. `kubernetes.io/kube-apiserver-client-kubelet`: підписує сертифікати, які мають вважатись сертифікатами клієнтів сервером API. Можуть бути автоматично затверджені {{< glossary_tooltip term_id="kube-controller-manager" >}}.
   1. Розподіл довіри: підписані сертифікати мають вважатись клієнтськими сертифікатами для доступу до API-сервера. Набір ЦС не поширюється жодним іншим способом.
   2. Дозволені субʼєкти: організації є безумовно `["system:nodes"]`, загальні імена починаються з "`system:node:`".
   3. Дозволені розширення x509: враховують розширення з використанням ключів, забороняють розширення subjectAltNames та відкидає інші розширення.
   4. Дозволені використання ключів: `["key encipherment", "digital signature", "client auth"]` або `["digital signature", "client auth"]`.
   5. Термін дії / термін життя сертифіката: для реалізації підписувача kube-controller-manager, встановлюється у мінімальне значення з `--cluster-signing-duration` або, якщо вказано, поля `spec.expirationSeconds` обʼєкта CSR.
   6. Біт ЦС дозволено / заборонено: не дозволяється.

3. `kubernetes.io/kubelet-serving`: підписує сертифікати, які мають вважатись сертифікатами, які обслуговуються kubelet, але не мають жодних гарантій. Ніколи автоматично не затверджуються {{< glossary_tooltip term_id="kube-controller-manager" >}}.
   1. Розподіл довіри: підписані сертифікати мають вважатись API сервером дійсними для обробки зʼєднань з kubelet. Набір ЦС не поширюється жодним іншим способом.
   2. Дозволені субʼєкти: організації є безумовно `["system:nodes"]`, загальні імена починаються з "`system:node:`".
   3. Дозволені розширення x509: враховують використання ключів та розширень DNSName/IPAddress subjectAltName extensions, забороняють розширення EmailAddress та URI subjectAltName, відкидають інші розширення. Принаймні один субʼєкт DNS чи IP повинен бути у subjectAltNames.
   4. Дозволені використання ключів: `["key encipherment", "digital signature", "server auth"]` або `["digital signature", "server auth"]`.
   5. Термін дії / термін життя сертифіката: для реалізації підписувача kube-controller-manager, встановлюється у мінімальне значення з `--cluster-signing-duration` або, якщо вказано, поля `spec.expirationSeconds` обʼєкта CSR.
   6. Біт ЦС дозволено / заборонено: не дозволяється.

4. `kubernetes.io/legacy-unknown`: не має гарантій довіри взагалі. Деякі сторонні дистрибутиви Kubernetes можуть використовувати сертифікати клієнтів, підписані ним. Стабільний API CertificateSigningRequest (версії `certificates.k8s.io/v1` та пізніше) не дозволяють встановлювати `signerName` на `kubernetes.io/legacy-unknown`. Ніколи автоматично не затверджується {{< glossary_tooltip term_id="kube-controller-manager" >}}.
   1. Розподіл довіри: Немає. Для цього підписувача не існує стандартної довіри або розподілу в кластері Kubernetes.
   2. Дозволені субʼєкти: будь-які
   3. Дозволені розширення x509: враховуються subjectAltNames та використання ключів, відкидаються інші розширення.
   4. Дозволені використання ключів: будь-які
   5. Термін дії / термін життя сертифіката: для реалізації підписувача kube-controller-manager, встановлюється у мінімальне значення з `--cluster-signing-duration` або, якщо вказано, поля `spec.expirationSeconds` обʼєкта CSR.
   6. Біт ЦС дозволено / заборонено: не дозволяється.

`kube-controller-manager` реалізує [підписування панелю управління](#signer-control-plane) для кожного з вбудованих підписувачів. Збої для всіх цих операцій повідомляються лише в логах `kube-controller-manager`.

{{< note >}}
Поле `spec.expirationSeconds` було додано в Kubernetes v1.22. Раніше версії Kubernetes не враховували це поле. API-сервери Kubernetes до v1.22 будуть просто ігнорувати це поле під час створення обʼєкта.
{{< /note >}}

Розподіл довіри відбувається поза рамками для цих підписувачів. Будь-яка довіра за межами описаного вище є строго випадковою. Наприклад, деякі дистрибутиви можуть приймати `kubernetes.io/legacy-unknown` як клієнтські сертифікати для `kube-apiserver`, але це не є стандартом. Жодне з цих використань не повʼязане з токенами секретів ServiceAccount `.data[ca.crt]`. Цей пакет CA гарантовано лише для верифікації зʼєднання з API-сервером за допомогою стандартного Service (`kubernetes.default.svc`).

### Власні підписувачі {#custom-signers}

Ви можете ввести власних підписувачів, які матимуть схожі імена з префіксами, але такі, що вказують на ваш власний домен. Наприклад, якщо ви є представником проєкту з відкритими сирцями, який використовує доменне імʼя `open-fictional.example`, тоді ви можете використовувати `issuer.open-fictional.example/service-mesh` як імʼя підписувача.

Власний підписувач використовує API Kubernetes для випуску сертифікатів. Дивіться [підписувачі на основі API](#signer-api) для деталей.

## Підписування {#signing}

### Підписування панеллю управління {#signer-control-plane}

Панель управління Kubernetes реалізує кожного з [підписувачів Kubernetes](/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers) як частину `kube-controller-manager`.

{{< note >}}
До Kubernetes v1.18, `kube-controller-manager` підписував будь-які CSRs, які були позначені як схвалені.
{{< /note >}}

{{< note >}}
Поле `spec.expirationSeconds` було додано в Kubernetes v1.22. Раніше версії Kubernetes не враховували це поле. API-сервери Kubernetes до v1.22 будуть просто ігнорувати це поле під час створення обʼєкта.
{{< /note >}}

### Підписувачі на основі API {#signer-api}

Користувачі REST API можуть підписувати CSRs, надсилаючи запит UPDATE до субресурсу `status` CSR, який потрібно підписати.

У рамках цього запиту поле `status.certificate` повинно бути встановлено, щоб містити підписаний сертифікат. Це поле містить один або більше сертифікатів, закодованих у форматі PEM.

Всі PEM блоки повинні мати мітку "CERTIFICATE", не містити заголовків, а закодовані дані повинні бути структурою сертифіката BER, закодованого в ASN.1, як описано в [розділі 4 RFC5280](https://tools.ietf.org/html/rfc5280#section-4.1).

Приклад вмісту сертифіката:

```none
-----BEGIN CERTIFICATE-----
MIIDgjCCAmqgAwIBAgIUC1N1EJ4Qnsd322BhDPRwmg3b/oAwDQYJKoZIhvcNAQEL
BQAwXDELMAkGA1UEBhMCeHgxCjAIBgNVBAgMAXgxCjAIBgNVBAcMAXgxCjAIBgNV
BAoMAXgxCjAIBgNVBAsMAXgxCzAJBgNVBAMMAmNhMRAwDgYJKoZIhvcNAQkBFgF4
MB4XDTIwMDcwNjIyMDcwMFoXDTI1MDcwNTIyMDcwMFowNzEVMBMGA1UEChMMc3lz
dGVtOm5vZGVzMR4wHAYDVQQDExVzeXN0ZW06bm9kZToxMjcuMC4wLjEwggEiMA0G
CSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDne5X2eQ1JcLZkKvhzCR4Hxl9+ZmU3
+e1zfOywLdoQxrPi+o4hVsUH3q0y52BMa7u1yehHDRSaq9u62cmi5ekgXhXHzGmm
kmW5n0itRECv3SFsSm2DSghRKf0mm6iTYHWDHzUXKdm9lPPWoSOxoR5oqOsm3JEh
Q7Et13wrvTJqBMJo1GTwQuF+HYOku0NF/DLqbZIcpI08yQKyrBgYz2uO51/oNp8a
sTCsV4OUfyHhx2BBLUo4g4SptHFySTBwlpRWBnSjZPOhmN74JcpTLB4J5f4iEeA7
2QytZfADckG4wVkhH3C2EJUmRtFIBVirwDn39GXkSGlnvnMgF3uLZ6zNAgMBAAGj
YTBfMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggrBgEFBQcDAjAMBgNVHRMB
Af8EAjAAMB0GA1UdDgQWBBTREl2hW54lkQBDeVCcd2f2VSlB1DALBgNVHREEBDAC
ggAwDQYJKoZIhvcNAQELBQADggEBABpZjuIKTq8pCaX8dMEGPWtAykgLsTcD2jYr
L0/TCrqmuaaliUa42jQTt2OVsVP/L8ofFunj/KjpQU0bvKJPLMRKtmxbhXuQCQi1
qCRkp8o93mHvEz3mTUN+D1cfQ2fpsBENLnpS0F4G/JyY2Vrh19/X8+mImMEK5eOy
o0BMby7byUj98WmcUvNCiXbC6F45QTmkwEhMqWns0JZQY+/XeDhEcg+lJvz9Eyo2
aGgPsye1o3DpyXnyfJWAWMhOz7cikS5X2adesbgI86PhEHBXPIJ1v13ZdfCExmdd
M1fLPhLyR54fGaY+7/X8P9AZzPefAkwizeXwe9ii6/a08vWoiE4=
-----END CERTIFICATE-----
```

Не-PEM вміст може зʼявлятися до або після блоків CERTIFICATE PEM і не перевіряється, щоб дозволити пояснювальний текст, як описано в [розділі 5.2 RFC7468](https://www.rfc-editor.org/rfc/rfc7468#section-5.2).

При кодуванні в JSON або YAML це поле закодоване в base-64. Запит на підпис сертифіката (CertificateSigningRequest), що містить приклад сертифіката вище, виглядатиме так:

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  certificate: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JS..."
```

## Схвалення або відхилення {#approval-rejection}

Перед тим, як [підписувач](#signers) видасть сертифікат на основі запиту на підписання сертифіката (CertificateSigningRequest), підписувач зазвичай перевіряє, що видача для цього CSR була _схвалена_.

### Автоматичне схвалення панелі управління {#approval-rejection-control-plane}

`kube-controller-manager` поставляється з вбудованим схвалювачем для сертифікатів з іменем підписувача `kubernetes.io/kube-apiserver-client-kubelet`, який делегує різні дозволи на CSRs для облікових даних вузлів до авторизації. `kube-controller-manager` надсилає ресурси SubjectAccessReview до API-сервера для перевірки авторизації на схвалення сертифіката.

### Схвалення або відхилення за допомогою `kubectl` {#approval-rejection-kubectl}

Адміністратор Kubernetes (з відповідними дозволами) може вручну схвалювати (або відхиляти) запити на підписання сертифікатів (CertificateSigningRequests) за допомогою команд `kubectl certificate approve` та `kubectl certificate deny`.

Щоб схвалити CSR за допомогою kubectl:

```shell
kubectl certificate approve <certificate-signing-request-name>
```

Аналогічно, щоб відхилити CSR:

```shell
kubectl certificate deny <certificate-signing-request-name>
```

### Схвалення або відхилення за допомогою API Kubernetes {#approval-rejection-api-client}

Користувачі REST API можуть схвалювати CSRs, надсилаючи запит UPDATE до субресурсу `approval` CSR, який потрібно схвалити. Наприклад, ви можете написати {{< glossary_tooltip term_id="operator-pattern" text="оператор" >}}, який слідкує за певним видом CSR, а потім надсилає UPDATE для їх схвалення.

Коли ви робите запит на схвалення або відхилення, встановіть або умову статусу `Approved`, або `Denied` залежно від визначеного стану:

Для схвалених CSR:

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  conditions:
  - lastUpdateTime: "2020-02-08T11:37:35Z"
    lastTransitionTime: "2020-02-08T11:37:35Z"
    message: Approved by my custom approver controller
    reason: ApprovedByMyPolicy # Ви можете вказати тут будь-який рядок
    type: Approved
```

Для відхилених CSR:

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  conditions:
  - lastUpdateTime: "2020-02-08T11:37:35Z"
    lastTransitionTime: "2020-02-08T11:37:35Z"
    message: Denied by my custom approver controller
    reason: DeniedByMyPolicy # Ви можете вказати тут будь-який рядок
    type: Denied
```

Зазвичай встановлюється в поле `status.conditions.reason` код причини, зручний для машинного зчитування, використовуючи TitleCase; це є умовністю, але ви можете встановити тут будь-яке значення. Якщо ви хочете додати примітку для читання людьми, використовуйте поле `status.conditions.message`.

## Пакети довіри кластера {#cluster-trust-bundles}

{{< feature-state for_k8s_version="v1.27" state="alpha" >}}

{{< note >}}
У Kubernetes {{< skew currentVersion >}} ви повинні ввімкнути [функціональну можливість](/docs/reference/command-line-tools-reference/feature-gates/) `ClusterTrustBundle` _та_ {{< glossary_tooltip text="групу API" term_id="api-group" >}} `certificates.k8s.io/v1alpha1`,
щоб використовувати цей API.
{{< /note >}}

ClusterTrustBundles — це обʼєкт масштабу кластера для розподілу якорів довіри X.509 (кореневих сертифікатів) до робочих навантажень у кластері. Вони розроблені для гарної роботи з концепцією [підписувача](#signers) із запитів на підписання сертифікатів (CertificateSigningRequests).

ClusterTrustBundles можна використовувати у двох режимах: [звʼязаний з підписувачем](#ctb-signer-linked) та [незвʼязаний з підписувачем](#ctb-signer-unlinked).

### Загальні властивості та валідація {#ctb-common}

Усі обʼєкти ClusterTrustBundle мають сувору валідацію вмісту їхнього поля `trustBundle`. Це поле повинно містити один або більше сертифікатів X.509, серіалізованих у DER, кожен з яких обгорнутий у блок PEM `CERTIFICATE`. Сертифікати повинні аналізуватися як дійсні сертифікати X.509.

Езотеричні функції PEM, такі як дані між блоками та заголовки всередині блоків, або відхиляються під час валідації обʼєкта, або можуть ігноруватися споживачами обʼєкта. Крім того, споживачі можуть перевпорядковувати сертифікати в пакеті за своїм власним довільним, але стабільним порядком.

Обʼєкти ClusterTrustBundle слід вважати загальнодоступними в межах кластера. Якщо ваш кластер використовує авторизацію [RBAC](/docs/reference/access-authn-authz/rbac/), усі ServiceAccounts стандартно мають  дозволи **get**, **list** та **watch** для всіх обʼєктів ClusterTrustBundle. Якщо ви використовуєте власний механізм авторизації та ввімкнули ClusterTrustBundles у своєму кластері, вам слід налаштувати еквівалентне правило для того, щоб ці обʼєкти були загальнодоступними в межах кластера, щоб вони працювали належним чином.

Якщо ви не маєте стандартного дозволу для отримання переліку пакетів довіри кластера у вашому кластері, ви можете діяти від імені службового облікового запису, до якого у вас є доступ, щоб побачити доступні ClusterTrustBundles:

```bash
kubectl get clustertrustbundles --as='system:serviceaccount:mynamespace:default'
```

### ClusterTrustBundles, звʼязані з підписувачем {#ctb-signer-linked}

ClusterTrustBundles, звʼязані з підписувачем, асоціюються з _імʼям підписувача_, як тут:

```yaml
apiVersion: certificates.k8s.io/v1alpha1
kind: ClusterTrustBundle
metadata:
  name: example.com:mysigner:foo
spec:
  signerName: example.com/mysigner
  trustBundle: "<... PEM data ...>"
```

ClusterTrustBundles призначені для підтримки контролера, специфічного для підписувача в кластері, тому вони мають кілька функцій безпеки:

* Щоб створити або оновити ClusterTrustBundle, звʼязаний з підписувачем, ви повинні мати дозвіл **підтвердити** підписувача (спеціальне дієслово авторизації `attest`, група API `certificates.k8s.io`; шлях ресурсу `signers`). Ви можете налаштувати авторизацію для конкретного імені ресурсу `<signerNameDomain>/<signerNamePath>` або відповідати шаблону, наприклад `<signerNameDomain>/*`.
* ClusterTrustBundles, звʼязані з підписувачем, **повинні** бути названі з префіксом, отриманим з їхнього поля `spec.signerName`. Слеші (`/`) замінюються на двокрапки (`:`), а в кінці додається двокрапка. За цим слідує довільне імʼя. Наприклад, підписувач `example.com/mysigner` може бути звʼязаний з ClusterTrustBundle `example.com:mysigner:<arbitrary-name>`.

ClusterTrustBundles, звʼязані з підписувачем, зазвичай використовуються у робочих навантаженнях за допомогою комбінації [селектора полів](/docs/concepts/overview/working-with-objects/field-selectors/) за іменем підписувача та окремого [селектора міток](/docs/concepts/overview/working-with-objects/labels/#label-selectors).

### ClusterTrustBundles, незвʼязані з підписувачем {#ctb-signer-unlinked}

ClusterTrustBundles, незвʼязані з підписувачем, мають порожнє поле `spec.signerName`, як це:

```yaml
apiVersion: certificates.k8s.io/v1alpha1
kind: ClusterTrustBundle
metadata:
  name: foo
spec:
  # signerName не вказано, тому поле порожнє
  trustBundle: "<... PEM data ...>"
```

Вони призначені головним чином для випадків використання конфігурації кластера. Кожен ClusterTrustBundle, незвʼязаний з підписувачем, є незалежним обʼєктом, на відміну від звичайної групової поведінки ClusterTrustBundles, звʼязаних з підписувачем.

ClusterTrustBundles, незвʼязані з підписувачем, не мають вимоги щодо дієслова `attest`. Натомість, ви контролюєте доступ до них безпосередньо за допомогою звичайних механізмів, таких як контроль доступу на основі ролей.

Щоб відрізнити їх від ClusterTrustBundles, звʼязаних з підписувачем, назви ClusterTrustBundles, незвʼязаних з підписувачем, **не повинні** містити двокрапку (`:`).

### Доступ до ClusterTrustBundles з Podʼів {#ctb-projection}

{{<feature-state for_k8s_version="v1.29" state="alpha" >}}

Вміст ClusterTrustBundles може бути впроваджений у файлову систему контейнера, подібно до ConfigMaps та Secrets. Дивіться [джерело projected томів clusterTrustBundle](/docs/concepts/storage/projected-volumes#clustertrustbundle) для отримання додаткової інформації.

<!-- TODO this should become a task page -->

## Як видати сертифікат для користувача {#normal-user}

Для того, щоб звичайний користувач міг автентифікуватися та викликати API, потрібно виконати кілька кроків. Спершу цей користувач повинен мати сертифікат, виданий кластером Kubernetes, а потім надати цей сертифікат API Kubernetes.

### Створення приватного ключа {#create-private-key}

Наступні скрипти показують, як згенерувати приватний ключ PKI та CSR. Важливо встановити значення CN та O атрибута CSR. CN — це імʼя користувача, а O — це група, до якої належатиме цей користувач. Ви можете звернутися до [RBAC](/docs/reference/access-authn-authz/rbac/) по стандартні групи.

```shell
openssl genrsa -out myuser.key 2048
openssl req -new -key myuser.key -out myuser.csr -subj "/CN=myuser"
```

### Створення запиту на підписання сертифікату {#create-certificatessigningrequest}

Створіть запит на підписання сертифікату (CertificateSigningRequest) і подайте його до кластера Kubernetes через kubectl. Нижче наведено скрипт для CertificateSigningRequest.

```shell
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: myuser
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZVzVuWld4aE1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQTByczhJTHRHdTYxakx2dHhWTTJSVlRWMDNHWlJTWWw0dWluVWo4RElaWjBOCnR2MUZtRVFSd3VoaUZsOFEzcWl0Qm0wMUFSMkNJVXBGd2ZzSjZ4MXF3ckJzVkhZbGlBNVhwRVpZM3ExcGswSDQKM3Z3aGJlK1o2MVNrVHF5SVBYUUwrTWM5T1Nsbm0xb0R2N0NtSkZNMUlMRVI3QTVGZnZKOEdFRjJ6dHBoaUlFMwpub1dtdHNZb3JuT2wzc2lHQ2ZGZzR4Zmd4eW8ybmlneFNVekl1bXNnVm9PM2ttT0x1RVF6cXpkakJ3TFJXbWlECklmMXBMWnoyalVnald4UkhCM1gyWnVVV1d1T09PZnpXM01LaE8ybHEvZi9DdS8wYk83c0x0MCt3U2ZMSU91TFcKcW90blZtRmxMMytqTy82WDNDKzBERHk5aUtwbXJjVDBnWGZLemE1dHJRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBR05WdmVIOGR4ZzNvK21VeVRkbmFjVmQ1N24zSkExdnZEU1JWREkyQTZ1eXN3ZFp1L1BVCkkwZXpZWFV0RVNnSk1IRmQycVVNMjNuNVJsSXJ3R0xuUXFISUh5VStWWHhsdnZsRnpNOVpEWllSTmU3QlJvYXgKQVlEdUI5STZXT3FYbkFvczFqRmxNUG5NbFpqdU5kSGxpT1BjTU1oNndLaTZzZFhpVStHYTJ2RUVLY01jSVUyRgpvU2djUWdMYTk0aEpacGk3ZnNMdm1OQUxoT045UHdNMGM1dVJVejV4T0dGMUtCbWRSeEgvbUNOS2JKYjFRQm1HCkkwYitEUEdaTktXTU0xMzhIQXdoV0tkNjVoVHdYOWl4V3ZHMkh4TG1WQzg0L1BHT0tWQW9FNkpsYWFHdTlQVmkKdjlOSjVaZlZrcXdCd0hKbzZXdk9xVlA3SVFjZmg3d0drWm89Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # один день
  usages:
  - client auth
EOF
```

Декілька моментів, на які варто звернути увагу:

* `usages` має бути '`client auth`'.
* `expirationSeconds` можна зробити довшим (наприклад, `864000` для десяти днів) або коротшим (наприклад, `3600` для однієї години).
* `request` — це base64-кодоване значення вмісту файлу CSR. Ви можете отримати цей вміст за допомогою такої команди:

```shell
cat myuser.csr | base64 | tr -d "\n"
```

### Схвалення CertificateSigningRequest {#approve-certificate-signing-request}

Використовуйте kubectl, щоб створити CSR та схвалити його.

Отримайте список CSR:

```shell
kubectl get csr
```

Схваліть CSR:

```shell
kubectl certificate approve myuser
```

### Отримання сертифіката {#get-the-certificate}

Отримайте сертифікат з CSR:

```shell
kubectl get csr/myuser -o yaml
```

Значення сертифіката знаходиться в форматі Base64-кодування в `status.certificate`.

Експортуйте виданий сертифікат з CertificateSigningRequest.

```shell
kubectl get csr myuser -o jsonpath='{.status.certificate}'| base64 -d > myuser.crt
```

### Створення Role та RoleBinding {#create-role-and-rolebinding}

Зі створеним сертифікатом, час визначити Role та RoleBinding для цього користувача для доступу до ресурсів кластера Kubernetes.

Ось приклад команди для створення Role для цього нового користувача:

```shell
kubectl create role developer --verb=create --verb=get --verb=list --verb=update --verb=delete --resource=pods
```

Ось приклад команди для створення RoleBinding для цього нового користувача:

```shell
kubectl create rolebinding developer-binding-myuser --role=developer --user=myuser
```

### Додавання до kubeconfig {#add-to-kubeconfig}

Останній крок — додати цього користувача до файлу kubeconfig.

Спершу, вам потрібно додати нові облікові дані:

```shell
kubectl config set-credentials myuser --client-key=myuser.key --client-certificate=myuser.crt --embed-certs=true

```

Потім, вам потрібно додати контекст:

```shell
kubectl config set-context myuser --cluster=kubernetes --user=myuser
```

Для перевірки, змініть контекст на `myuser`:

```shell
kubectl config use-context myuser
```

## {{% heading "whatsnext" %}}

* Прочитайте [Керування TLS-сертифікатами у кластері](/docs/tasks/tls/managing-tls-in-a-cluster/)
* Перегляньте вихідний код вбудованого [підписувача](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/signer/cfssl_signer.go) kube-controller-manager
* Перегляньте вихідний код вбудованого [схвалювача](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/approver/sarapprove.go) kube-controller-manager
* Для деталей щодо X.509, звертайтеся до [RFC 5280](https://tools.ietf.org/html/rfc5280#section-3.1) розділ 3.1
* Для інформації щодо синтаксису запитів на підписання сертифікатів PKCS#10, звертайтеся до [RFC 2986](https://tools.ietf.org/html/rfc2986)
* Прочитайте про API ClusterTrustBundle:
  * {{< page-api-reference kind="ClusterTrustBundle" >}}