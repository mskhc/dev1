---
title: Локалізація документації Kubernetes
content_type: concept
approvers:
- remyleone
- rlenferink
weight: 50
card:
  name: contribute
  weight: 50
  title: Локазізація документації
---

<!-- overview -->

Ця сторінка містить приклади [локалізації](https://blog.mozilla.org/l10n/2011/12/14/i18n-vs-l10n-whats-the-diff/) документації Kubernetes різними мовами.

<!-- body -->

## Покращення наявної локалізації {#contribute-to-an-existing-localization}

Ви можете допомогти додати або покращити вміст наявної локалізації. У [Slack Kubernetes](https://slack.k8s.io/), ви можете знайти канал для кожної локалізації. Також є загальний [канал SIG Docs Localizations](https://kubernetes.slack.com/messages/sig-docs-localizations), де ви можете привітатись.

{{< note >}}
За додатковою інформацією про те, як допомогти з певною локалізацією, шукайте локалізовану версію цієї сторінки.
{{< /note >}}

### Визначте дволітерний код вашої мови {#find-your-two-letter-language-code}

Звіртесь зі [стандартом ISO 639-1](https://www.loc.gov/standards/iso639-2/php/code_list.php), щоб знайти дволітерний код вашої мови. Наприклад, дволітерний код для української мови — `uk`.

Деякі мови використовують версію коду країни у нижньому регістрі, як визначено стандартом ISO-3166, разом з їх мовними кодами. Наприклад, код бразильської португальської мови — `pt-br`.

### Зробіть форк та клонуйте репозиторій {#fork-and-clone-the-repo}

Спочатку, [зробіть форк](/docs/contribute/new-content/open-a-pr/#fork-the-repo) репозиторію [kubernetes/website](https://github.com/kubernetes/website).

Потім клонуйте його собі на компʼютер та перейдіть в локальну теку:

```shell
git clone https://github.com/<username>/website
cd website
```

Вміст сайту включає підтеки для кожної мови. Для локалізації, вам потрібно змінювати вміст в підтеках `content/<two-letter-code>`.

### Пропонуйте зміни {#suggest-changes}

Створіть або оновіть вибрану локалізовану сторінку на основі англійського оригіналу. Дивіться розділ [Локалізація вмісту](#localize-content) для отримання додаткових вказівок.

Якщо ви помітили якійсь технічні неточності або інші проблеми з англійською документацією, ви повинні спочатку виправити англійську документацію, а потім повторити відповідні зміни, оновивши локалізацію, над якою ви працюєте.

Обмежте зміни в пул-реквесті однією локалізацією. Розгляд змін, які змінюють вміст у кількох локалізаціях, є проблематичним.

Слідуйте рекомендаціям [Пропонування покращення вімісту](/docs/contribute/suggesting-improvements/) для пропозиції змін у вмісті локалізації. Це процес подібний до пропозиції змін в оригінальний вміст (англійською мовою).

## Створення нової локалізації {#start-a-new-localization}

Якщо ви хочете мати документацію Kubernetes вашою мовою, ось що вам потрібно зробити.

Оскільки учасники не можуть схвалювати свої власні пул-реквести, вам потрібно *принаймні два учасники* для початку локалізації.

Всі команди локалізації повинні бути самостійними. Вебсайт Kubernetes радий опублікувати вашу роботу, але вам потрібно перекладати вміст і підтримувати наявний локалізований вміст.

Вам потрібно зʼясувати дволітерний код вашої мови. Зверніться до [стандарту ISO 639-1](https://www.loc.gov/standards/iso639-2/php/code_list.php), щоб знайти дволітерний код вашої мови. Наприклад, дволітерний код для української мови — `uk`.

Якщо мова, для якої ви починаєте локалізацію, використовується в різних місцях зі значними відмінностями між варіантами, можливо, має сенс поєднати дволітерний код країни з дволітерним кодом мови. Наприклад, бразильська португальська позначається як `pt-br`.

Коли ви починаєте нову локалізацію, вам потрібно локалізувати [мінімально необхідний вміст](#minimum-required-content) перед тим, як проєкт Kubernetes зможе опублікувати ваші зміни на сайті.

SIG Docs може допомогти вам з роботою в окремій гілці, щоб ви могли поступово працювати для досягнення цієї мети.

### Пошук спільноти {#find-community}

Дайте знати команді документації Kubernetes, що ви зацікавлені в створенні локалізації! Приєднуйтесь до [каналу Slack SIG Docs](https://kubernetes.slack.com/messages/sig-docs) та [каналу Slack SIG Docs Localizations](https://kubernetes.slack.com/messages/sig-docs-localizations). Інші команди локалізації будуть раді допомогти вам почати та відповісти на ваші питання.

Розгляньте, будь ласка, можливість участі в [зустрічі підгрупи локалізації SIG Docs](https://github.com/kubernetes/community/tree/master/sig-docs). Місією підгрупи локалізації SIG Docs є співпраця з командами локалізації SIG Docs з метою спільного визначення та документування процесів створення локалізованих посібників. Крім того, підгрупа локалізації SIG Docs розглядає можливості створення та обміну загальними інструментами серед команд локалізації та визначення нових вимог для команди керівників SIG Docs. Якщо у вас є питання щодо цього засідання, будь ласка, запитуйте на
[каналі Slack SIG Docs Localizations](https://kubernetes.slack.com/messages/sig-docs-localizations).

Ви також можете створити канал Slack для своєї локалізації в
репозиторії `kubernetes/community`. Для прикладу, як додавати канал в Slack, див. PR для
[додавання каналу для перської мови](https://github.com/kubernetes/community/pull/4980).

### Приєднуйтесь до організації Kubernetes на GitHub {#join-the-kubernetes-github-organization}

Коли ви відкрили PR для локалізації, ви можете стати учасниками організації Kubernetes. Кожна особа в команді повинна створити свій власний [Запит на членство в організації](https://github.com/kubernetes/org/issues/new/choose) у репозиторії `kubernetes/org`.

### Додайте свою команду локалізації на GitHub {#add-your-localization-team-in-github}

Далі, додайте свою команду локалізації Kubernetes в
[`sig-docs/teams.yaml`](https://github.com/kubernetes/org/blob/main/config/kubernetes/sig-docs/teams.yaml). Для прикладу додавання команди локалізації, див. PR для додавання
[іспанської команди локалізації](https://github.com/kubernetes/org/pull/685).

Члени `@kubernetes/sig-docs-**-owners` можуть схвалювати PR, які змінюють вміст в межах (і лише в межах) вашої теки локалізації: `/content/**/`. Для кожної локалізації команда `@kubernetes/sig-docs-**-reviews` автоматизує додавання рецензій для нових PR. Члени `@kubernetes/website-maintainers` можуть створювати нові гілки локалізації для координації зусиль з перекладу. Члени `@kubernetes/website-milestone-maintainers` можуть використовувати команду [Prow](https://prow.k8s.io/command-help) `/milestone` для призначення віхи завдання чи PR.

### Налаштування робочого процесу {#configure-the-workflow}

Далі, додайте мітку GitHub для вашої локалізації в репозиторії `kubernetes/test-infra`. Мітка дозволяє вам фільтрувати завдання та пул-реквести для вашої мови.

Приклад додавання мітки для [італійської мови](https://github.com/kubernetes/test-infra/pull/11316).

### Зміна конфігурації сайту {#modify-the-site-configuration}

Вебсайт Kubernetes використовує Hugo для обслуговування вмісту. Конфігурація вебсайту знаходиться в файлі [`hugo.toml`](https://github.com/kubernetes/website/tree/main/hugo.toml). Вам потрібно внести зміни у `hugo.toml` для увімкнення підтримки нової локалізації.

Додайте блок конфігурації для нової мови до `hugo.toml` в блок `[languages]`. Наприклад, блок для німецької мови виглядає так:

```toml
[languages.de]
title = "Kubernetes"
description = "Produktionsreife Container-Verwaltung"
languageName = "Deutsch (German)"
languageNameLatinScript = "Deutsch"
contentDir = "content/de"
weight = 8
```

Змінна `languageName` містить назву мови, яка показується в панелі вибору мови. Вкажіть у `languageName` назву в форматі "назва мови вашою мовою (назва мови англійською мовою)". Наприклад, `languageName = "한국어 (Korean)"` або `languageName = "Deutsch (German)"`.

`languageNameLatinScript` може використовуватись для доступу до мови латиницею та використовувати в темах. Вкажіть "назва мови латиною" у `languageNameLatinScript`. Наприклад, `languageNameLatinScript = "Korean"` або `languageNameLatinScript = "Deutsch"`.

Параметр `weight` визначає порядок мов у панелі вибору мови. Менше значення `weight` має пріоритет, що призводить до того, що мова показується першою. Призначаючи параметр `weight`, важливо ретельно ознайомитись з наявними блоками мов та змінити їх вагу, щоб вони були впорядковані відносно всіх мов, включаючи будь-які нові мови.

Для отримання додаткової інформації щодо багатомовної підтримки Hugo дивіться "[Multilingual Mode](https://gohugo.io/content-management/multilingual/)".

### Додавання нової теки локалізації {#add-a-new-localization-directory}

Додайте теку для вашої мови в теку
[`content`](https://github.com/kubernetes/website/tree/main/content) в репозиторії. Наприклад, дволітерний код для німецької мови — `de`:

```shell
mkdir content/de
```

Також потрібно створити теку всередині `data/i18n` для
[локалізованих рядків](#site-strings-in-i18n); перегляньте наявні локалізації для прикладу. Для використання цих нових рядків, вам також потрібно створити символічне посилання
з `i18n/<код-мови>.toml` на фактичну конфігурацію рядків у
`data/i18n/<код-мови>/<код-мови>.toml` (не забудьте додати символічне посилання в коміт).

Наприклад, для німецької мови рядки знаходяться в `data/i18n/de/de.toml`, і `i18n/de.toml` — це символічне посилання на `data/i18n/de/de.toml`.

### Локалізуйте community code of conduct {#localize-community-code-of-conduct}

Створіть пул-реквест в репозиторії [`cncf/foundation`](https://github.com/cncf/foundation/tree/main/code-of-conduct-languages) для додавання правил спільноти вашою мовою.

### Створіть файли OWNERS {#set-up-the-owners-files}

Для призначення ролей кожному учаснику, який вносить внесок у локалізацію, створіть файл `OWNERS` всередині підтеки, яка відповідає вашій мові, з таким вмістом

- **reviewers**: Перелік команд kubernetes з роллю рецензентів
  - команду `sig-docs-**-reviews` створену на кроці [Додайте свою команду локалізації на GitHub](#add-your-localization-team-in-github).
- **approvers**: Перелік команд kubernetes з роллю, що може затверджувати зміни, в цьому випадку
  - команду `sig-docs-**-owners` створену на кроці [Додайте свою команду локалізації на GitHub](#add-your-localization-team-in-github).
- **labels**: Перелік міток, які автоматично додаються до пул-реквестів, в цьому випадку, мітки створені на етапі [Налаштування робочого процесу](#configure-the-workflow).

Докладніше про файл `OWNERS` дивіться — [go.k8s.io/owners](https://go.k8s.io/owners).

Для прикладу [файл Spanish OWNERS](https://git.k8s.io/website/content/es/OWNERS), з кодом мови `es`, виглядає так:

```yaml
# See the OWNERS docs at https://go.k8s.io/owners

# This is the localization project for Spanish.
# Teams and members are visible at https://github.com/orgs/kubernetes/teams.

reviewers:
- sig-docs-es-reviews

approvers:
- sig-docs-es-owners

labels:
- language/es
```

Після додавання файлу `OWNERS` для вашої мови, оновіть [кореневий файл `OWNERS_ALIASES`](https://git.k8s.io/website/OWNERS_ALIASES) новою командою Kubernetes для локалізації, `sig-docs-**-owners` та `sig-docs-**-reviews`.

Для кожної команди додайте список користувачів GitHub, які потрібні на етапі [Додайте свою команду локалізації на GitHub](#add-your-localization-team-in-github), в алфавітному порядку.

```diff
--- a/OWNERS_ALIASES
+++ b/OWNERS_ALIASES
@@ -48,6 +48,14 @@ aliases:
     - stewart-yu
     - xiangpengzhao
     - zhangxiaoyu-zidif
+  sig-docs-es-owners: # Admins for Spanish content
+    - alexbrand
+    - raelga
+  sig-docs-es-reviews: # PR reviews for Spanish content
+    - alexbrand
+    - electrocucaracha
+    - glo-pena
+    - raelga
   sig-docs-fr-owners: # Admins for French content
     - perriea
     - remyleone
```

### Створіть пул-реквест {#open-a-pull-request}

Далі, [створіть пул-реквест](/docs/contribute/new-content/open-a-pr/#open-a-pr) (PR) для додавання локалізації в репозиторій `kubernetes/website`. PR повинен містити [мінімально необхідний вміст](#minimum-required-content) перед тим, як він може бути схваленим.

Наприклад додавання нової локалізації для [французької мови](https://github.com/kubernetes/website/pull/12548).

### Додайте локалізований файл README {#add-a-localized-readme-file}

Щоб керувати іншими учасниками локалізації, додайте новий
[`README-**.md`](https://help.github.com/articles/about-readmes/) в корінь репозиторію [kubernetes/website](https://github.com/kubernetes/website/), де `**` — дволітерний код мови. Наприклад, файл README для української мови буде `README-uk.md`.

Скеровуйте учасників локалізації до локалізованого файлу `README-**.md`. Додайте туди ту ж інформацію, що міститься в `README.md`, а також:

- Контактну інформацію проєкту локалізації
- Будь-яку інформацію, специфічну для локалізації

Після створення локалізованого README, додайте посилання на файл у головний англійський `README.md`, а також включіть контактну інформацію англійською мовою. Ви можете надати ідентифікатор GitHub, адресу електронної пошти, [канал Slack](https://slack.com/) або інший метод звʼязку. Ви також повинні надати посилання на локалізований Кодекс поведінки спільноти.

### Запуск вашої нової локалізації {#launch-your-new-localization}

Коли локалізація відповідає вимогам для робочого процесу та мінімальним вимогам щодо вмісту, SIG Docs робить наступне:

- Вмикає на вебсайті відповідний мовний розділ.
- Сповіщає про наявність локалізованого вмісту через канали [Cloud Native Computing Foundation](https://www.cncf.io/about/) (CNCF), включаючи [блог Kubernetes](/blog/).

## Локалізація вмісту {#localize-content}

Локалізація вмісту *всього* вмісту Kubernetes є неосяжним завданням. Необхідно починати з мінімально необхідного вмісту та поступово розширювати його.

### Мінімально необхідний вміст {#minimum-required-content}

Як мінімум, всі локалізації мають містити:

Опис | Посилання
-----|----------
Документація | [Всі заголовки та підзаголовки](/docs/home/)
Початок роботи | [Всі заголовки та підзаголовки](/docs/setup/)
Посібники | [Основи Kubernetes](/docs/tutorials/kubernetes-basics/), [Привіт Minikube](/docs/tutorials/hello-minikube/)
Локалізація сайту | [Всі рядки](#site-strings-in-i18n) в новому TOML файлі локалізації
Випуски | [Всі заголовки та підзаголовки](/releases)

Перекладена документація має знаходитись у власній підтеці `content/**/` та мати ту ж URL-структуру, що й англійська версія. Наприклад, щоб підготувати [Основи Kubernetes](/docs/tutorials/kubernetes-basics/) для перекладу німецькою мовою, створіть підтеку у `content/de` та скопіюйте в неї сирці англійської версії:

```shell
mkdir -p content/de/docs/tutorials
cp -ra content/en/docs/tutorials/kubernetes-basics/ content/de/docs/tutorials/
```

Інструменти для роботи з перекладами значно прискорюють процес перекладу. Наприклад, деякі редактори пропонують втулки для швидкого перекладу тексту.

{{< caution >}}
Машино-генерований переклад недостатній сам по собі. Локалізація вимагає ретельного перегляду людиною, щоб вміст відповідав мінімальним стандартам якості.
{{< /caution >}}

Щоб переконатись в точності та відповідності перекладу, члени вашої команди локалізації повинні ретельно переглянути всі машинно-генеровані переклади перед публікацією.

### Локалізація зображень SVG {#localize-svg-images}

Проєкт Kubernetes рекомендує використовувати векторні (SVG) зображення, де це можливо, оскільки їх набагато легше редагувати командам локалізації. Якщо ви знаходите растрове зображення, яке потрібно локалізувати, розгляньте можливість спочатку перетворення англійської версії у векторне зображення, а потім локалізуйте його.

При перекладі тексту всередині векторних зображень (SVG — Scalable Vector Graphics) важливо дотримуватися певних рекомендацій, щоб забезпечити точність і підтримувати однорідність між різними мовними версіями. Зображення SVG часто використовуються в документації Kubernetes для ілюстрації концепцій, робочих процесів та схем.

1. **Визначення тексту для перекладу**:
   Почніть з ідентифікації текстових елементів всередині SVG-зображення, які потрібно перекласти. Зазвичай до цих елементів входять мітки, підписи, анотації чи будь-який текст, що передає інформацію.

2. **Редагування файлів SVG**:
   Файли SVG базуються на XML, що означає, що їх можна редагувати за допомогою текстового редактора. Проте важливо враховувати, що більшість зображень в документації Kubernetes вже конвертують текст в криві, щоб уникнути проблем сумісності шрифтів. У таких випадках рекомендується використовувати спеціалізоване програмне забезпечення для редагування SVG, таке як Inkscape. Відкрийте файл SVG у програмі Inkscape та знайдіть елементи тексту, які потребують перекладу.

3. **Переклад текстів**:
   Замініть оригінальний текст перекладеною версією бажаною мовою. Переконайтеся, що перекладений текст точно виражає задумане значення і вміщується у вільне простір у зображенні. При роботі з мовами, які використовують латинський алфавіт, слід використовувати сімʼю шрифтів Open Sans. Ви можете завантажити шрифт Open Sans за цим посиланням: [Open Sans Typeface](https://fonts.google.com/specimen/Open+Sans).

4. **Перетворення тексту в криві**:
   Як вже зазначалося, для розв'язання проблеми сумісності шрифтів рекомендується конвертувати перекладений текст в криві. Конвертація тексту в криві гарантує правильне відображення перекладеного тексту у кінцевому зображенні, навіть якщо система користувача не має шрифту, використаного в оригінальному SVG.

5. **Перегляд та тестування**:
   Після перекладу і конвертації тексту в криві, збережіть та перегляньте оновлене SVG-зображення, щоб переконатися, що текст правильно показується та відповідно вирівняний. Виконайте [Попередній перегляд ваших змін локально](/docs/contribute/new-content/open-a-pr/#preview-locally).

### Файли сирців {#source-files}

Локалізація має базуватись на файлах англійською мовою з конкретного релізу, на який спрямовані зусилля команди локалізації. Кожна команда локалізації може визначити, на який реліз спрямовані її зусилля, що позначено нижче як _цільова версія_.

Для пошуку файлів сирців для цільової версії:

1. Перейдіть до репозиторію вебсайту Kubernetes
   https://github.com/kubernetes/website.

1. Оберіть гілку з вашою цільовою версією користуючись таблицею:

Цільова версія | Гілка
-----|-----
Остання версія | [`main`](https://github.com/kubernetes/website/tree/main)
Попередня версія | [`release-{{< skew prevMinorVersion >}}`](https://github.com/kubernetes/website/tree/release-{{< skew prevMinorVersion >}})
Наступна версія | [`dev-{{< skew nextMinorVersion >}}`](https://github.com/kubernetes/website/tree/dev-{{< skew nextMinorVersion >}})

Гілка `main` містить вміст для поточного релізу `{{< latest-version >}}`. Команда релізу створює гілку `{{< release-branch >}}` перед наступним релізом: v{{< skew nextMinorVersion >}}.

### Рядки сайту в i18n {#site-strings-in-i18n}

Локалізація має включати вміст [`data/i18n/en/en.toml`](https://github.com/kubernetes/website/blob/main/data/i18n/en/en.toml) у новому файлі для відповідної мови. Наприклад, для німецької мови: `data/i18n/de/de.toml`.

Додайте нову теуку для локалізації та файл до `data/i18n/`. Наприклад, для німецької мови (`de`):

```bash
mkdir -p data/i18n/de
cp data/i18n/en/en.toml data/i18n/de/de.toml
```

Ознайомтесь з коментарями вгорі файлу, щоб зрозуміти, які рядки потрібно локалізувати. Наприклад, це німецькомовний текст-заповнювач для поля пошуку:

```toml
[ui_search_placeholder]
other = "Suchen"
```

Локалізовані рядки сайту дозволяють вам налаштувати текстові рядки, які використовуються в багатьох місцях на сайті. Наприклад, текст копірайту в підвалі на кожній сторінці.

### Настанови щодо локалізації певною мовою {#language-specific-localization-guide}

Як команда локалізації, ви можете формалізувати найкращі практики, які використовує ваша команда, створивши мовно-специфічний посібник з локалізації. 

Наприклад, див. [Корейський посібник з локалізації](/ko/docs/contribute/localization_ko/), який включає опис таких тем, як:

- Частота спринтів та релізи
- Стратегія створення гілок
- Робота з pull request
- Посібник зі стилю
- Глосарій локалізованих та нелокалізованих термінів
- Конвенції Markdown
- Термінологія обʼєктів Kubernetes API
  
### Зустрічі в Zoom для обговорення локалізації відповідною мовою {#language-specific-zoom-meetings}

Якщо проєкту з локалізації потрібен окремий час на зустрічі, звʼяжіться з одним з координаторів SIG Docs або Tech Lead, щоб створити нову регулярну зустріч в Zoom та запрошення в календар. Це потрібно тільки тоді, коли команда достатньо велика та вимагає окремих зустрічей.

Відповідно до правил CNCF, команди локалізації повинні завантажувати свої зустрічі в плейлист YouTube SIG Docs. Координатор SIG Docs або Tech Lead може допомогти з цим процесом до тих пір, поки SIG Docs не автоматизує його.

## Стратегія створення гілок {#branch-strategy}

Оскільки проєкти локалізації є зусиллями кількох осіб, ми закликаємо команди працювати в спільних гілках локалізації, особливо на початковому етапі, коли локалізація ще не є оприлюдненою.

Щоб співпрацювати в гілці локалізації:

1. Член команди [@kubernetes/website-maintainers](https://github.com/orgs/kubernetes/teams/website-maintainers) створює гілку локалізації з гілки основного проєкту
   <https://github.com/kubernetes/website>.

   Особи з вашої команди, які затверджують зміни, приєднуються до команди `@kubernetes/website-maintainers`, коли ви [створюєте свою команду локалізації](#add-your-localization-team-in-github) до репозиторію [`kubernetes/org`](https://github.com/kubernetes/org).

   Ми радимо наступну схему найменування гілок:

   `dev-<source version>-<language code>.<team milestone>`

   Наприклад, затверджувач зміни німецької команди створює гілку для локалізації `dev-1.12-de.1` безпосередньо в репозиторії `kubernetes/website`, яка базується на гілці для Kubernetes v1.12.

2. Індивідуальні учасники створюють гілки-теми на основі гілки локалізації.

   Наприклад, учасник німецькою команди створює пул-реквест зі змінами у `kubernetes:dev-1.12-de.1` з `username:local-branch-name`.

3. Затверджувач переглядає зміни та зливає гілку-тему в гілку локалізації.

4. Періодично затверджувач обʼєднує гілку локалізації зі своєю вихідною гілкою, відкриваючи та затверджуючи новий pull request. Обовʼязково обʼєднуйте (squash) коміти перед затвердженням pull request.

Повторюйте кроки 1-4 за потреби, поки локалізація не буде завершена. Наприклад, наступні гілки локалізації німецькою мовою будуть: `dev-1.12-de.2`, `dev-1.12-de.3` і т.д.

Команди повинні обʼєднувати локалізований вміст у ту гілку, з якої вміст було отримано. Наприклад:

- Гілку локалізації створену з гілки `main` потрібно заливати у гілку `main`.
- Гілку локалізації створену з `release-{{% skew "prevMinorVersion" %}}` потрібно заливати у `release-{{% skew "prevMinorVersion" %}}`.

{{< note >}}
Якщо ваша гілка локалізації була створена з гілки `main`, але її не обʼєднано з `main` до створення нової гілки релізу `{{< release-branch >}}`, обʼєднайте її як з `main`, так і з новою гілкою релізу `{{< release-branch >}}`. Для обʼєднання гілки локалізації з новою гілкою релізу `{{< release-branch >}}` потрібно змінити вищезазначену гілку вашої локалізації на гілку `{{< release-branch >}}`.
{{< /note >}}

На початку кожного етапу команді корисно відкрити тікет для порівняння змін вверх між попередньою гілкою локалізації та поточною гілкою. Є два скрипти для порівняння змін.

- [`upstream_changes.py`](https://github.com/kubernetes/website/tree/main/scripts#upstream_changespy)
  є корисним для перевірки змін, що були зроблені у відповідному файлі, та
- [`diff_l10n_branches.py`](https://github.com/kubernetes/website/tree/main/scripts#diff_l10n_branchespy)
  є корисним для створення переліку застарілих файлів для відповідної гілки локалізації.

Хоча тільки затверджувачі можуть створювати нові гілки локалізації та обʼєднувати пул-реквести, будь-хто може відкрити пул-реквести для нової гілки локалізації. Для цього спеціальні дозволи не потрібні.

Для отримання додаткової інформації про роботу з форками або безпосередньо з репозиторієм, див. ["розгалуження та клонування репозиторію"](#fork-and-clone-the-repo).

## Внесення змін до оригінальної документації {#upstream-contributions}

Команда SIG Docs вітає внески та виправлення до англійської версії документації.