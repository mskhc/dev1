---
title: "Зовнішня конфігурація за допомогою MicroProfile, ConfigMaps та Secrets"
content_type: tutorial
weight: 10
---

<!-- overview -->

У цьому посібнику ви дізнаєтеся, як і чому варто зовнішньо налаштовувати конфігурацію вашого мікросервісу. Зокрема, ви дізнаєтеся, як використовувати Kubernetes ConfigMaps і Secrets для встановлення змінних середовища та їх подальшого використання за допомогою MicroProfile Config.

## {{% heading "prerequisites" %}}

### Створення Kubernetes ConfigMaps та Secrets {#creating-kubernetes-configmaps-secrets}

Існує кілька способів встановлення змінних середовища для Docker-контейнера в Kubernetes, зокрема: Dockerfile, kubernetes.yml, Kubernetes ConfigMap та Kubernetes Secret. У цьому посібнику ви дізнаєтеся, як використовувати останні два для встановлення змінних середовища, значення яких будуть впроваджені у ваші мікросервіси. Однією з переваг використання ConfigMap та Secret є те, що вони можуть повторно використовуватися у кількох контейнерах, включаючи можливість призначення різним змінним середовища для різних контейнерів.

ConfigMap — це обʼєкти API, які зберігають неконфіденційні пари "ключ-значення". У інтерактивному посібнику ви дізнаєтеся, як використовувати ConfigMap для зберігання імені програми. Більше інформації про ConfigMap ви можете знайти у [документації](/docs/tasks/configure-pod-container/configure-pod-configmap/).

Хоча Secret також використовуються для зберігання пар "ключ-значення", вони відрізняються від ConfigMap тим, що призначені для конфіденційної/чутливої інформації та зберігаються за допомогою кодування Base64. Це робить Secret відповідним вибором для зберігання таких речей, як облікові дані, ключі та токени, що ви й зробите в інтерактивному завданні. Більше інформації про Secret ви можете знайти у [документації](/docs/concepts/configuration/secret/).

### Зовнішня конфігурація з коду {#externalizing-config-from-code}

Зовнішня конфігурація застосунків корисна, оскільки конфігурація зазвичай змінюється залежно від вашого середовища. Для цього ми будемо використовувати Java Contexts and Dependency Injection (CDI) та MicroProfile Config. MicroProfile Config — це функція MicroProfile, набору відкритих Java-технологій для розробки та розгортання хмаро-орієнтованих мікросервісів.

CDI надає стандартну можливість впровадження залежностей, що дозволяє створювати застосунок з працюючих разом, слабо звʼязаних частин. MicroProfile Config надає застосункам та мікросервісам стандартний спосіб отримання конфігураційних властивостей з різних джерел, включаючи застосунок, середовище виконання та оточення. Відповідно до визначеного пріоритету джерела, властивості автоматично комбінуються в єдиний набір властивостей, до якого застосунок може отримати доступ через API. Разом, CDI та MicroProfile будуть використані в інтерактивному посібнику для отримання зовнішньо наданих властивостей з Kubernetes ConfigMap та Secret і їх додавання у ваш код застосунку.

Багато відкритих фреймворків та середовищ виконання реалізують і підтримують MicroProfile Config. Протягом інтерактивного уроку ви будете використовувати Open Liberty, гнучке відкрите середовище виконання Java для створення та запуску хмаро-орієнтованих застосунків та мікросервісів. Однак замість нього можна використовувати будь-яке сумісне з MicroProfile середовище.

## {{% heading "objectives" %}}

* Створити Kubernetes ConfigMap та Secret
* Встановити конфігурацію мікросервісу за допомогою MicroProfile Config

<!-- lessoncontent -->

## Приклад: Зовнішня конфігурація за допомогою MicroProfile, ConfigMap та Secret {#example-externalizing-config-using-microprofile-configmaps-and-secrets}

[Почати інтерактивний урок](/uk/docs/tutorials/configuration/configure-java-microservice/configure-java-microservice-interactive/)