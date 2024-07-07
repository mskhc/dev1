---
reviewers:
- bprashanth
- erictune
- foxish
- smarterclayton
title: Примусове видалення Podʼів StatefulSet
content_type: task
weight: 70
---

<!-- overview -->

Ця сторінка показує, як видаляти Podʼи, які є частиною {{< glossary_tooltip text="StatefulSet" term_id="StatefulSet" >}}, та пояснює важливі моменти, які слід враховувати під час цього.

## {{% heading "prerequisites" %}}

- Це досить високорівневе завдання і може порушити деякі властивості, притаманні StatefulSet.
- Перед продовженням ознайомтеся з розглянутими нижче моментами.

<!-- steps -->

## Міркування про StatefulSet {#statefulset-considerations}

При нормальному функціонуванні StatefulSet **ніколи** немає потреби у примусовому видаленні Podʼів StatefulSet. [Контролер StatefulSet](/docs/concepts/workloads/controllers/statefulset/) відповідає за створення, масштабування та видалення членів StatefulSet. Він намагається забезпечити, щоб зазначена кількість Podʼів від ordinal 0 до N-1 були справними та готовими. StatefulSet забезпечує те, що в будь-який момент часу в кластері працює не більше одного Podʼа з заданою ідентичністю. Це називається семантикою *як максимум один*, яку забезпечує StatefulSet.

Примусове видалення слід виконувати з обережністю, оскільки воно може порушити семантику "як максимум один", притаманну StatefulSet. StatefulSet можуть використовуватися для запуску розподілених і кластерних застосунків, які потребують стабільної мережевої ідентичності та стабільного сховища. Ці застосунки часто мають конфігурацію, яка ґрунтується на ансамблі фіксованої кількості членів з фіксованими ідентичностями. Наявність декількох членів із тією самою ідентичністю може бути руйнівною і може призвести до втрати даних (наприклад, у випадку "розщеплення мозку" в системах на основі кворуму).

## Видалення Podʼів {#delete-pods}

Ви можете виконати коректне видалення Podʼа за допомогою наступної команди:

```shell
kubectl delete pods <pod>
```

Щоб таке видалення призвело до коректного завершення, **необхідно** вказати `pod.Spec.TerminationGracePeriodSeconds` більше 0. Практика встановлення `pod.Spec.TerminationGracePeriodSeconds` на 0 секунд є небезпечною та категорично не рекомендується для Podʼів StatefulSet. Коректне видалення є безпечним і забезпечить, що Pod [коректно завершить роботу](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) перед тим, як kubelet видалить імʼя з apiserver.

Pod не видаляється автоматично, коли вузол недоступний. Podʼи, які працюють на недоступному вузлі, потрапляють у стан 'Terminating' або 'Unknown' після [тайм-ауту](/docs/concepts/architecture/nodes/#condition). Podʼи також можуть потрапляти в ці стани, коли користувач спробує коректне видалення Podʼа на недоступному вузлі. Єдині способи, якими Pod у такому стані може бути видалено з apiserver, наступні:

- Обʼєкт Node видаляється (або вами, або [Контролером Вузлів](/docs/concepts/architecture/nodes/#node-controller)).
- kubelet на недоступному Вузлі починає відповідати, припиняє роботу Pod та видаляє запис з apiserver.
- Примусове видалення Podʼа користувачем.

Рекомендована практика — використовувати перший або другий підхід. Якщо вузол підтверджено є несправним (наприклад, постійно відключений від мережі, вимкнений тощо), то видаліть обʼєкт Node. Якщо вузол страждає від розділення мережі, то спробуйте вирішити це або зачекайте на його вирішення. Коли розділення мережі виправляється, kubelet завершить видалення Podʼа та звільнить його імʼя в apiserver.

Зазвичай система завершує видалення, як тільки Pod більше не працює на Вузлі, або Вузол видаляється адміністратором. Ви можете перевизначити це за допомогою примусового видалення Podʼа.

### Примусове видалення {#force-deletion}

Примусові видалення **не** чекають підтвердження від kubelet про те, що Pod було завершено. Незалежно від того, чи успішно примусове завершення Podʼу припиняє його роботу чи ні, воно негайно звільняє імʼя з apiserverʼа. Це дозволить контролеру StatefulSet створити новий Pod з тією самою ідентичністю; це може призвести до дублювання все ще працюючого Podʼа, і якщо цей Pod все ще може спілкуватися з іншими членами StatefulSet, це порушить семантику "як максимум один", яку StatefulSet має гарантувати.

Коли ви примусово видаляєте Pod StatefulSet, ви стверджуєте, що цей Pod більше ніколи не буде знову взаємодіяти з іншими Podʼами StatefulSet, і його імʼя може бути безпечно звільнено для створення заміни.

Якщо ви хочете примусово видалити Pod за допомогою kubectl версії >= 1.5, виконайте наступне:

```shell
kubectl delete pods <pod> --grace-period=0 --force
```

Якщо ви використовуєте будь-яку версію kubectl <= 1.4, ви повинні пропустити параметр `--force` і використовувати:

```shell
kubectl delete pods <pod> --grace-period=0
```

Якщо навіть після цих команд Pod застряг у стані `Unknown`, використайте наступну команду для видалення Podʼа з кластера:

```shell
kubectl patch pod <pod> -p '{"metadata":{"finalizers":null}}'
```

Завжди виконуйте примусове видалення Podʼів StatefulSet обережно та з повним розумінням ризиків, повʼязаних із цим.

## {{% heading "whatsnext" %}}

Дізнайтеся більше про [налагодження StatefulSet](/docs/tasks/debug/debug-application/debug-statefulset/).