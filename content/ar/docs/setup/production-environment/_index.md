---
title: "بيئات الإنتاج"
description: تصميم عنقود كوبيرنيتيس جاهز للإنتاج
weight: 30
no_list: true
---
<!-- overview -->

يتطلب إنشاء عنقود كوبيرنيتيس بجودة إنتاجية تخطيطًا وإعدادًا دقيقين.
إذا كان عنقود كوبيرنيتيس الخاص بك سيقوم بتشغيل أحمال عمل حساسة،
فيجب تكوينه ليكون متينًا وقادرًا على التكَيُّف والصمود.
تشرح هذه الصفحة الإرشادات لإعداد عنقود جاهز للإنتاج،
أو لترقية عنقود حالي للاستخدام الإنتاجي.
إذا كنت على دراية مسبقة بالإعداد الإنتاجي وترغب في الوصول إلى روابط الموارد مباشرةً، انتقل إلى [الخطوات التالية](#what-s-next).

<!-- body -->

## معايير البيئة الإنتاجية

عادة ما تكون لبيئة عنقود كوبيرنيتيس الإنتاجية معايير أعلى من بيئة التعلم الشخصية أو التطوير أو الاختبار.
قد تتطلب البيئة الإنتاجية توافر التطبيقات باستمرار،
وقدرة الوصول إليها بأمان،
والموارد الحاسوبية اللازمة للتكيف مع متطلباتها المتغيرة.

عند اتخاذ القرار بشأن مكان استضافة بيئة كوبيرنيتيس الإنتاجية الخاصة بك
(سواء على أجهزتك الخاصة أو في السحابة)
ومدى رغبتك في تولى إدارة البيئة أو تفويض ذلك للآخرين،
ضع في اعتبارك كيف تتأثر متطلباتك للعنقود بالأمور التالية:

- _التوافر_: تكشف بيئة كوبيرنيتيس ذات الجهاز الواحد
  ([كبيئة التعلم](/docs/setup/#learning-environment))
  نقطة فشل واحدة.
  لتفادي ذلك ينصح بتصميم عنقود عالي التوافر، وذلك يتضمن:
    - فصل مستوى التحكم عن العُقد العاملة.
    - نشر عدة نسخ من مكونات مستوى التحكم على عدة عُقد.
    - موازنة حركة المرور إلى [خادم واجهة برمجة التطبيقات](/docs/reference/glossary/?all=true#term-kube-apiserver) للعنقود.
    - توفير عدد كافٍ من العقد العاملة، أو القدرة على توفيرها بسرعة،
	حسب ما تتطلبه أحمال العمل المتغيرة.
	
- _القابلية للتوسع_: إذا كنت تتوقع أن تتلقى بيئة كوبيرنيتيس الإنتاجية الخاصة بك مستوى طلب ثابت،
  فقد تتمكن من الإعداد للسعة التي تحتاجها مرة واحدة والانتهاء من الأمر.
  ولكن إذا كنت تتوقع نمو الطلب مع مرور الوقت أو تغيره بشكل كبير بتغير المواسم،
  فعليك التخطيط لكيفية التوسع الآلي للعنقود لتخفيف الضغط عليه عند زيادة الطلب،
  أو لتقليل الموارد غير المستخدمة عند نقصان الطلب.

- _الأمان وإدارة الوصول_: بطبيعة الحال،
  يمنحك عنقود كوبيرنيتيس التعليمي صلاحيات التحكم به كاملةً،
  ولكن العناقيد الإنتاجية ذات الأحمال المهمة تتطلب نهجاً أكثر دقة في منح صلاحيات التحكم.
  يمكنك استخدام نظام التحكم في الوصول المبني على الأدوار ([RBAC](/docs/reference/access-authn-authz/rbac/))
  وآليات الآمان الأخرى للتأكد من منح صلاحيات الوصول إلى التطبيقات بشكل مناسب،
  مع الحفاظ على آمان التطبيقات والعنقود نفسه.
  يمكنك وضع حدود للوصول إلى موارد العنقود باسخدام
  [السياسات](/docs/concepts/policy/)
  و[موارد الحاويات](/docs/concepts/configuration/manage-resources-containers/).

قبل بناء بيئة كوبيرنيتيس إنتاجية بنفسك،
ضع في اعتبارك تفويض بعض أو كل تلك المهام إلى مزودي [حلول السحابة الجاهزة](/docs/setup/production-environment/turnkey-solutions/)
أو [شركاء كوبيرنيتيس](/partners/) الآخرين. تشمل الخيارات:

- _البنية التحتية كخدمة (IaaS)_: قم بتشغيل تطبيقاتك على أجهزة طرف ثالث دون إدارة العنقود على الإطلاق.
  سيتم محاسبتك على استهلاكك للموارد الحاسوبية كوحدة المعالجة المركزية والذاكرة وطلبات القرص.
- _مستوى التحكم المُدار_: دع المزود يدير مستوى التحكم للعنقود،
  متوليًا إتاحة وتحجيم الموارد بالإضافة إلى القيام بالتصحيحات والترقيات.
- _العُقد العاملة المُدارة_: قم بتكوين مجموعات من العُقد لتلبية احتياجاتك،
  فيقوم المزود بالمحافظة على توافر وجاهزية العقد وتنفيذ الترقيات عند الحاجة.
- _التكامل_: هناك مزودون يدمجون كوبيرنيتيس مع خدمات أخرى قد تحتاجها، مثل التخزين وسجلات الحاويات وطرق المصادقة وأدوات التطوير.

سواءً اخترت بناء عنقود إنتاجي بنفسك أو الاستناد إلى طرف ثالث،
راجع الأقسام التالية لتقييم احتياجاتك فيما يتعلق بـ_مستوى التحكم_ و_العقد العاملة_ و_وصول المستخدم_ و_موارد أحمال العمل_ الخاصة بعنقودك.

## إعداد العنقود الإنتاجي

في عناقيد كوبيرنيتيس الإنتاجية، يدير مستوى التحكم العنقود عادةً من خلال خدمات يمكن توزيعها على عدة أجهزة بطرق مختلفة. ومع ذلك، تمثل كل عقدة كيانًا مستقلاً قادراً على تشغيل حجيرات كوبيرنيتيس.

### مستوى التحكم الإنتاجي

في أبسط عنقود، تعمل مكونات مستوى التحكم وخدمات العقدة كلها على جهز واحد،
أي أن مستوى التحكم يعمل على تلك العقدة الواحدة.
يمكنك توسيع تلك البيئة عن طريق إضافة عقد عاملة، كما هو موضح في الرسم التوضيحي في [مكونات كوبيرنيتيس](/docs/concepts/overview/components/).
إذا كان المرغوب أن يكون العنقود متاحًا لفترة وجيزة فقط، أو أن يكون قابل للاستبدال لسبب عطل على المثال، فقد يلبي هذا احتياجاتك.

ولكن، إذا كنت بحاجة إلى عنقود دائم وعالي التوافر،
فعليك النظر في توسيع مستوى التحكم.
بحكم التصميم، فإن خدمات مستوى التحكم ذات الجهاز الواحد التي تعمل على جهاز واحد ليست عالية التوافر.
إذا كان الحفاظ على صحة العنقود وضمان إمكانية تصليحه أمرًا مهمًا، ففكر في الخطوات الآتية:

- _اختيار أداة النشر_: يمكنك نشر مستوى تحكم باستخدام أدوات مثل kubeadm و kops و kubespray.
  راجع [تثبيت كوبيرنيتيس بأدوات النشر](/docs/setup/production-environment/tools/) للتعرف على نصائح حول النشر الإنتاجي باستخدام تلك الأدوات.
  تتوفر عدة [محركات تشغيل حاويات](/docs/setup/production-environment/container-runtimes/) للاستخدام في التصميم الخاص بك.
  
- _إدارة الشهادات_: يتم الاتصال الآمن بين خدمات مستوى التحكم باستخدام الشهادات.
  تُنشأ الشهادات تلقائيًا أثناء النشر الخدمات و بإمكانك أيضاً توكيل سلطة الشهادات الخاصة بك لإنشائها.
  راجع [شهادات PKI ومتطلباتها](/docs/setup/best-practices/certificates/) للتفاصيل.
  
- _تكوين موازن أحمال لخادم واجهة برمجة التطبيقات_:
  قم بتكوين موازن أحمال كي يوزع طلبات التواصل مع العنقود بين نسخ خادم واجهة برمجة التطبيقات المختلفة.
  راجع [إنشاء موازن أحمال خارجي](/docs/tasks/access-application-cluster/create-external-load-balancer/) للحصول على التفاصيل.

- _فصل خدمة etcd عن مستوى التحكم، والنسخ الاحتياطي لها_:
  يمكن لخدمات etcd أن تعمل سوياً مع خدمات مستوى التحكم على نفس الأجهزة،
  أو أن تعمل على أجهزة منفصلة، والثانية أكثر أمانًا.
  نظرًا لأن etcd تخزن بيانات تكوين العنقود، يجب إجراء نسخ احتياطي لقاعدة بيانات etcd بانتظام لضمان إمكانية تصليح العنقود إذا لزم الأمر.
  راجع [الأسئلة الشائعة حول etcd](https://etcd.io/docs/v3.5/faq/) للحصول على تفاصيل حول تكوين واستخدام etcd.
  راجع [تشغيل عناقيد etcd لكوبيرنيتيس](/docs/tasks/administer-cluster/configure-upgrade-etcd/)
  و[إعداد عنقود etcd عالي التوافر باستخدام kubeadm](/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/) للحصول على التفاصيل.
  
- _إنشاء أنظمة مستوى تحكم متعددة_: لتحقيق توافر عالٍ،
  يجب ألا يقتصر نشر مستوى التحكم على جهاز واحد.
  إذا تم تشغيل خدمات مستوى التحكم بواسطة خدمة تهيئة (مثل systemd)،
  فيجب أن تعمل كل خدمة على ثلاثة أجهزة على الأقل.
  بينما يضمن تشغيل خدمات مستوى التحكم كحجيرات في كوبيرنيتيس توافر العدد المطلوب من النسخ دائمًا.
  ليتحقق ذلك، يجب أن يكون مجدول كوبيرنيتيس قادرًا على تحمل الأخطاء.
  تقوم بعض أدوات النشر لكوبيرنيتيس بإعداد خوارزمية إجماع [Raft](https://raft.github.io/) لإجراء انتخاب قائد لكل خدمة في مستوى التحكم.
  إذا اختفى القائد الأساسي، تُنتخب أحد النسخ الأخرى مكانها وتتولى المسؤولية.

- _الامتداد عبر مناطق متعددة_: إذا كان الحفاظ على توافر عنقودك في جميع الأوقات أمرًا بالغ الأهمية،
  ففكر في إنشاء عنقود موزع على عدة مراكز بيانات (والتي يشار إليها  _بالمناطق_).
  تُعرف مجموعات المناطق _بالأقاليم_.
  من خلال نشر عنقود عبر مناطق متعددة في نفس الإقليم،
  يمكنك تحسين فرص استمرار عمل عنقودك حتى تعطلت العُقد في منطقة ما.
  راجع [التشغيل في مناطق متعددة](/docs/setup/best-practices/multiple-zones/)للتفاصيل.

- _المهام الإدارية_: إذا كنت تخطط للحفاظ على عنقودك لفترة طويلة،
  فهناك مهام يجب عليك القيام بها للحفاظ على صحته وأمنه.
  على سبيل المثال، إذا قمت بالتثبيت باستخدام kubeadm،
  فعليك [إدارة الشهادات](/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)
  و[ترقية عناقيد kubeadm](/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/).
  راجع [إدارة العنقود](/docs/tasks/administer-cluster/) للحصول على قائمة أطول بمهام إدارة كوبيرنيتيس.

لمعرفة الخيارات المتاحة لتشغيل خدمات مستوى التحكم، راجع صفحات مكونات [kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/) و[kube-controller-manager](/docs/reference/command-line-tools-reference/kube-controller-manager/) و[kube-scheduler](/docs/reference/command-line-tools-reference/kube-scheduler/).
للحصول على أمثلة على مستويات التحكم عالية التوافر، راجع [خيارات للطوبولوجيا العالية التوافر](/docs/setup/production-environment/tools/kubeadm/ha-topology/) و[إنشاء عناقيد عالية التوافر باستخدام kubeadm](/docs/setup/production-environment/tools/kubeadm/high-availability/) و[تشغيل عناقيد etcd لكوبيرنيتيس](/docs/tasks/administer-cluster/configure-upgrade-etcd/).
راجع [النسخ الاحتياطي لعنقود etcd](/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster) للحصول على معلومات حول وضع خطة نسخ احتياطي لـ etcd.

### العُقد العاملة الإنتاجية

تحتاج أحمال العمل ذات الجودة الإنتاجية إلى أن تكون قادرة على التكيف وكل ما تعتمد عليه يجب أن يكون قادرًا على التكيف أيضًا (مثل CoreDNS).
سواء كنت تدير مستوى التحكم الخاص بك أو تترك مزود خدمة يقوم بذلك نيابًة عنك،
فلا يزال عليك النظر في كيفية إدارة العقد العاملة الخاصة بك (والتي يشار إليها ببساطة باسم _العقد_).

- _تكوين العقد_: يمكن أن تكون العقد أجهزة حقيقية أو افتراضية.
  إذا كنت ترغب في إنشاء وإدارة العقد الخاصة بك،
  فعليك تثبيت نظام تشغيل مدعوم على الجهاز،
  ثم إضافة وتشغيل [خدمات العقدة](/docs/concepts/overview/components/#node-components) المناسبة. ضع في اعتبارك:
    - متطلبات أحمال العمل الخاصة بك عند إعداد العقد من خلال توفير ذاكرة ووحدة معالجة مركزية وسرعة قرص وسعة تخزين مناسبة.
    - ما إذا كانت أنظمة الكمبيوتر العامة ستفي بالغرض أم إن لديك أحمال عمل تحتاج إلى معالجات GPU أو عقد Windows أو عزل الأجهزة الافتراضية.
- _التحقق من صحة العقد_: راجع [إعداد العقدة الصحيح](/docs/setup/best-practices/node-conformance/) للحصول على معلومات حول كيفية التأكد من أن العقدة تفي بالمتطلبات اللازمة للانضمام إلى عنقود كوبيرنيتيس.
- _إضافة عقد إلى العنقود_: إذا كنت تدير عنقودك بنفسك،
  فيمكنك إضافة عقد عن طريق إعداد أجهزتك الخاصة وإضافتها يدويًا أو جعلها تسجل نفسها مع خادم واجهة برمجة التطبيقات للعنقود.
  راجع قسم [العقد](/docs/concepts/architecture/nodes/) للحصول على معلومات حول كيفية إعداد كوبيرنيتيس لإضافة العقد بهذه الطرق.
- _تحجيم العقد_: ضع خطة لتوسيع عنقودك إلى السعة المطلوبة في النهاية.
  راجع [اعتبارات للعناقيد الكبيرة](/docs/setup/best-practices/cluster-large/) للمساعدة في تحديد عدد العقد التي تحتاجها،
  بناءً على عدد الحجيرات والحاويات التي تحتاج إلى تشغيلها.
  إذا كنت تدير العقد بنفسك، فقد يعني هذا شراء وتثبيت معداتك المادية الخاصة.
- _التحجيم التلقائي للعقد_: يدعم معظم مزودي الخدمات السحابية [تحجيم العناقيد تلقائيًا](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#readme) لاستبدال العقد غير الصحية أو زيادة وتقليص عدد العقد حسب الطلب.
  راجع [الأسئلة الشائعة](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md) لمعرفة كيفية عمل الموسع التلقائي
  و[النشر](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#deployment) لمعرفة كيفية تطبيقه من قبل مزودي الخدمات السحابية المختلفين.
  بالنسبة للأنظمة المحلية، هناك بعض منصات المحاكاة الافتراضية التي يمكن برمجتها لتشغيل عقد جديدة بناءً على الطلب.
- _إعداد فحوصات صحة العقدة_: بالنسبة لأحمال العمل المهمة،
  تريد التأكد من صحة العقد والحجيرات التي تعمل عليها.
  يمكنك التأكد من أن عقدك صحية باستخدام برنامج [كاشف مشاكل العقدة](/docs/tasks/debug/debug-cluster/monitor-node-health/).

## إدارة المستخدمين في البيئة الإنتاجية

عادةً ما يستخدم المطور البيئة التعليمية وحده،
فلا يحتاج المطور إلى أكثر من حساب إداري واحد للوصول للعنقود.
على النقيض، قد تتاح البيئات الإنتاجية لعشرات أو مئات المستخدمين،
ولذلك ينصح بإعداد عدة حسابات إدارية ذات صلاحيات متدرجة في البيئات الإنتاجية،
للتحكم مثلاً في الوصول إلى النطاقات المختلفة.

عليك كمسؤول عن بيئةٍ إنتاجيةٍ اتخاذ القرار بشأن طرق السماح للوصول إلى عنقودك،
فعليك وضع الاستراتيجيات للتحقق من هويات المستخدمين (المصادقة)،
وما إذا كان لديهم الصلاحيات للقيام بما يطلبونه على العنقود (التفويض):

- _المصادقة_: يمكن لخادم واجهة برمجة التطبيقات مصادقة المستخدمين باستخدام أيٍ من شهادات العميل والرموز المميزة للحامل ووكيل المصادقة والمصادقة الأساسية عبر HTTP.
  عليك اختيار طريقة المصادقة التي تريد استخدامها.
  باستخدام الإضافات، يمكن لخادم واجهة برمجة التطبيقات الاستفادة من طرق المصادقة الحالية في مؤسستك، مثل LDAP أو Kerberos.
  راجع [المصادقة](/docs/reference/access-authn-authz/authentication/) للحصول على وصف لهذه الطرق المختلفة لمصادقة مستخدمي كوبيرنيتيس.
- _التفويض_: عندما تبدأ في تفويض مستخدميك العاديين، ستختار على الأرجح بين تفويض RBAC وABAC.
  راجع [نظرة عامة على التفويض](/docs/reference/access-authn-authz/authorization/)لمراجعة الأوضاع المختلفة لتفويض حسابات المستخدمين
  (بالإضافة إلى وصول حساب الخدمة إلى عنقودك):
    - _التحكم في الوصول المستند إلى الأدوار_ ([RBAC](/docs/reference/access-authn-authz/rbac/)): يتيح لك تعيين الوصول إلى عنقودك من خلال منح مجموعات محددة من الصلاحيات للمستخدمين المصادق عليهم. يمكن تعيين الصلاحيات لنطاق محدد (الدور) أو عبر العنقود بأكمله (دور العنقود). ثم باستخدام ربط الأدوار وربط أدوار العنقود، يمكن إرفاق تلك الصلاحيات بمستخدمين معينين.
    - _التحكم في الوصول المستند إلى السمات_ ([ABAC](/docs/reference/access-authn-authz/abac/)): يتيح لك إنشاء سياسات بناءً على سمات الموارد في العنقود، فيُسمح أو يُرفض الوصول بناءً على تلك السمات. يحدد كل سطر من ملف السياسة خصائص الإصدار (apiVersion وkind) وخريطة لخصائص المستخدم (سواءً كان فرداً أو مجموعة). راجع [الأمثلة](/docs/reference/access-authn-authz/abac/#examples) للحصول على التفاصيل.

إليك بعض الأمور التي يجب مراعاتها عند إعداد المصادقة والتفويض:

- _تعيين وضع التفويض_: عند بدء تشغيل خادم واجهة برمجة التطبيقات لكوبيرنيتيس ([kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/))، يجب تعيين أوضاع المصادقة المرغوبة باستخدام العلامة _--authorization-mode_.
  على سبيل المثال، يمكن تعيين تلك العلامة في ملف _kube-apiserver.yaml_
  (في _/etc/kubernetes/manifests_) إلى `Node,RBAC`.
   سيسمح ذلك بالتفويض عن طريق العقد مباشرةً ونظام RBAC معًا.

- _إنشاء شهادات المستخدم, وربط الأدوار (RBAC)_: إذا كنت تستخدم تفويض RBAC،
  يمكن للمستخدم إنشاء طلب توقيع شهادة (CSR)، والذي يُوقع بواسطة سلطة شهادات العنقود.
  ومن ثم يمكنك ربط الأدوار وأدوار العنقود بالمستخدمين.
  راجع [طلبات توقيع الشهادات](/docs/reference/access-authn-authz/certificate-signing-requests/) للحصول على التفاصيل.

- _إنشاء سياسات تجمع بين السمات (ABAC)_: إذا كنت تستخدم تفويض ABAC،
  يمكنك تشكيل سياسة لتفويض الوصول إلى عدة موارد بناءً على اشتراكها في عدة سمات.
  لمزيد من المعلومات، راجع [الأمثلة](/docs/reference/access-authn-authz/abac/#examples).

- _النظر في وحدات التحكم في القبول_: هناك آليات إضافية لتفويض الطلبات يديرهاخادم واجهة برمجة التطبيقات،
  ومنها [مصادقة Webhook](/docs/reference/access-authn-authz/authentication/#webhook-token-authentication).
  تفعل تلك الآليات عن طريق إضافة [وحدات تحكم القبول](/docs/reference/access-authn-authz/admission-controllers/) إلى خادم واجهة برمجة التطبيقات.


## وضع حدود على استهلاك الموارد

يمكن أن تسبب متطلبات أحمال العمل الإنتاجية ضغطًا داخل وخارج مستوى التحكم لكوبيرنيتيس.
ضع في اعتبارك الأمور الآتية عند الإعداد:

- _تعيين حدود للنطاقات_: قم بتعيين حصة من الموارد الحاسوبية لكل نطاق.
  راجع [إدارة الذاكرة ووحدة المعالجة المركزية وموارد واجهة برمجة التطبيقات](/docs/tasks/administer-cluster/manage-resources/) للحصول على التفاصيل.
  يمكنك أيضًا تعيين [نطاقات هرمية](/blog/2020/08/14/introducing-hierarchical-namespaces/) لتوريث تلك الحدود.

- _الاستعداد لطلبات DNS_: إذا كنت تتوقع أن تتوسع أحمال العمل بشكل كبير،
  فيجب أن تكون خدمة DNS الخاصة بك جاهزة للتوسع أيضًا.
  راجع [التحجيم الآلي لخدمة DNS](/docs/tasks/administer-cluster/dns-horizontal-autoscaling/).

- _إنشاء حسابات خدمة إضافية_: تحدد حسابات المستخدمين ما يمكن للمستخدمين القيام به في العنقود، بينما يحدد حساب الخدمة صلاحيات الحجيرات داخل نطاقها.
  تأخذ الحجيرة طبيعياً حساب الخدمة الافتراضي من نطاقها.
  راجع [إدارة حسابات الخدمة](/docs/reference/access-authn-authz/service-accounts-admin/) للحصول على معلومات حول إنشاء حساب خدمة جديد.
  على سبيل المثال، قد ترغب في:
    - إضافة أسرار لتمكين الحجيرات من سحب صور الحاويات من سجل حاويات معين.
      راجع [تكوين حسابات الخدمة للحجيرات](/docs/tasks/configure-pod-container/configure-service-account/) للاطلاع على مثال.
    - تعيين أذونات RBAC لحساب خدمة.
      راجع [أذونات حساب الخدمة](/docs/reference/access-authn-authz/rbac/#service-account-permissions) للحصول على التفاصيل.

## {{% heading "whatsnext" %}}

- قرر ما إذا كنت تريد بناء عنقود كوبيرنيتيس إنتاجي بنفسك أو الإعتماد على أحد [حلول السحابة الجاهزة](/docs/setup/production-environment/turnkey-solutions/)
  أو [شركاء كوبيرنيتيس](/partners/).
- إذا اخترت بناء عنقودك بنفسك، خطط لكيفية التعامل مع [الشهادات](/docs/setup/best-practices/certificates/)
  وإعداد التوافر العالي للخدمات مثل [etcd](/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)
  و[خادم واجهة برمجة التطبيقات](/docs/setup/production-environment/tools/kubeadm/ha-topology/).
- اختر من بين طرق النشر [kubeadm](/docs/setup/production-environment/tools/kubeadm/) أو [kops](https://kops.sigs.k8s.io/) أو [Kubespray](https://kubespray.io/).
- قم بإدارة المستخدمين عن طريق تحديد طرق [المصادقة](/docs/reference/access-authn-authz/authentication/)
  و[التفويض](/docs/reference/access-authn-authz/authorization/).
- استعد لأحمال العمل التطبيقية عن طريق تعيين [حدود الموارد](/docs/tasks/administer-cluster/manage-resources/)
  و[التحجيم الآلي لـ DNS](/docs/tasks/administer-cluster/dns-horizontal-autoscaling/)
  و[حسابات الخدمة](/docs/reference/access-authn-authz/service-accounts-admin/).