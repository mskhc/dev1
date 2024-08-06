---
title: kube-proxy Configuration (v1alpha1)
content_type: tool-reference
package: kubeproxy.config.k8s.io/v1alpha1
auto_generated: false
---

## Типи ресурсів {#resource-types}

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

## `ClientConnectionConfiguration` {#ClientConnectionConfiguration}

**Appears in:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1-KubeSchedulerConfiguration)

- [GenericControllerManagerConfiguration](#controllermanager-config-k8s-io-v1alpha1-GenericControllerManagerConfiguration)

ClientConnectionConfiguration містить деталі для створення клієнта.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>kubeconfig</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>kubeconfig — шлях до файлу KubeConfig.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>acceptContentTypes</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>acceptContentTypes визначає заголовок Accept, що надсилається клієнтами при підключенні до сервера, переважаючи стандартне значення 'application/json'. Це поле контролює всі підключення до сервера, що використовуються конкретним клієнтом.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>contentType</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>contentType — це тип вмісту, що використовується при надсиланні даних на сервер з цього клієнта.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>qps</code> <b>[Обовʼязкове]</b><br/>
                <code>float32</code>
            </td>
            <td>
                <p>qps контролює кількість запитів на секунду, дозволених для цього зʼєднання.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>burst</code> <b>[Обовʼязкове]</b><br/>
                <code>int32</code>
            </td>
            <td>
                <p>burst дозволяє накопичувати додаткові запити, коли клієнт перевищує свій поріг.</p>
            </td>
        </tr>
    </tbody>
</table>

## `DebuggingConfiguration` {#DebuggingConfiguration}

**Appears in:**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1-KubeSchedulerConfiguration)

- [GenericControllerManagerConfiguration](#controllermanager-config-k8s-io-v1alpha1-GenericControllerManagerConfiguration)

DebuggingConfiguration містить конфігурацію для функцій, повʼязаних із налагодженням.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>enableProfiling</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>enableProfiling дозволяє профілювання через веб-інтерфейс за адресою host:port/debug/pprof/</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>enableContentionProfiling</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>enableContentionProfiling дозволяє профілювання блокувань, якщо enableProfiling встановлено в true.</p>
            </td>
        </tr>
    </tbody>
</table>

## `LeaderElectionConfiguration` {#LeaderElectionConfiguration}

**Appears in:**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1-KubeSchedulerConfiguration)

- [GenericControllerManagerConfiguration](#controllermanager-config-k8s-io-v1alpha1-GenericControllerManagerConfiguration)

LeaderElectionConfiguration визначає конфігурацію клієнтів вибору лідера для компонентів, які можуть працювати з увімкненим вибором лідера.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>leaderElect</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>leaderElect дозволяє клієнту вибору лідера отримати лідерство перед виконанням основного циклу. Увімкніть це при запуску повторюваних компонентів для високої доступності.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>leaseDuration</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>leaseDuration — це тривалість, яку не-лідери кандидати будуть чекати після спостереження за поновленням лідерства, перш ніж спробувати отримати лідерство замісць лідера, який не був поновлений. Це фактично максимальна тривалість, протягом якої лідер може бути зупинений перед заміною іншим кандидатом. Це застосовується тільки в разі увімкнення вибору лідера.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>renewDeadline</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>renewDeadline — це інтервал між спробами діючого майстра поновити слот лідерства перед тим, як він перестане бути лідером. Це має бути менше або дорівнювати тривалості оренди. Це застосовується тільки в разі увімкнення вибору лідера.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>retryPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>retryPeriod — це тривалість, протягом якої клієнти повинні чекати між спробами отримання і поновлення лідерства. Це застосовується тільки в разі увімкнення вибору лідера.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>resourceLock</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>resourceLock вказує тип обʼєкта ресурсу, який буде використовуватися для блокування під час циклів вибору лідера.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>resourceName</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>resourceName вказує імʼя обʼєкта ресурсу, який буде використовуватися для блокування під час циклів вибору лідера.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>resourceNamespace</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>resourceNamespace вказує простір імен обʼєкта ресурсу, який буде використовуватися для блокування під час циклів вибору лідера.</p>
            </td>
        </tr>
    </tbody>
</table>

## `KubeProxyConfiguration` {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration}

KubeProxyConfiguration містить все необхідне для налаштування проксі-сервера Kubernetes.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>apiVersion</code><br/>string
            </td>
            <td>
                <code>kubeproxy.config.k8s.io/v1alpha1</code>
            </td>
        </tr>
        <tr>
            <td>
                <code>kind</code><br/>string
            </td>
            <td>
                <code>KubeProxyConfiguration</code>
            </td>
        </tr>
        <tr>
            <td>
                <code>featureGates</code> <b>[Обовʼязкове]</b><br/>
                <code>map[string]bool</code>
            </td>
            <td>
                <p>featureGates є зіставленням імен функцій до булевих значень, які дозволяють або забороняють альфа/експериментальні функції.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>clientConnection</code> <b>[Обовʼязкове]</b><br/>
                <a href="#ClientConnectionConfiguration"><code>ClientConnectionConfiguration</code></a>
            </td>
            <td>
                <p>clientConnection вказує файл kubeconfig і налаштування зʼєднання клієнта для використання проксі-сервером при спілкуванні з apiserver.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>logging</code> <b>[Обовʼязкове]</b><br/>
                <a href="#LoggingConfiguration"><code>LoggingConfiguration</code></a>
            </td>
            <td>
                <p>logging вказує параметри ведення логу. Дивіться <a href="https://github.com/kubernetes/component-base/blob/master/logs/options.go">Logs Options</a> для додаткової інформації.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>hostnameOverride</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>hostnameOverride, якщо не порожній, буде використовуватися як імʼя вузла, на якому працює kube-proxy. Якщо не задано, імʼя вузла вважається таким же, як і hostname вузла.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>bindAddress</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>bindAddress може бути використано для переозначення IP-адреси вузла, яка є основною для kube-proxy. Зверніть увагу, що імʼя є історичним артефактом, і kube-proxy насправді не привʼязує жодні сокети до цього IP.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>healthzBindAddress</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>healthzBindAddress — це IP-адреса та порт для сервера перевірки стану, на якому він буде служити, стандартно "0.0.0.0:10256" (якщо bindAddress не встановлено або IPv4), або "[::]:10256" (якщо bindAddress є IPv6).</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>metricsBindAddress</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>metricsBindAddress — це IP-адреса та порт для сервера метрик, на якому він буде служити, стандартно "127.0.0.1:10249" (якщо bindAddress не встановлено або IPv4), або "[::1]:10249" (якщо bindAddress є IPv6). (Встановіть на "0.0.0.0:10249" / "[::]:10249", щоб привʼязатися до всіх інтерфейсів.)</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>bindAddressHardFail</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>bindAddressHardFail, якщо true, вказує kube-proxy вважати помилку привʼязки до порту фатальною і вийти</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>enableProfiling</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>enableProfiling дозволяє профілювання через веб-інтерфейс на обробнику /debug/pprof. Обробники профілювання будуть оброблені сервером метрик.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>showHiddenMetricsForVersion</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>showHiddenMetricsForVersion — це версія, для якої ви хочете показати приховані метрики.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>mode</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-ProxyMode"><code>ProxyMode</code></a>
            </td>
            <td>
                <p>mode вказує, який режим проксі використовувати.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>iptables</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPTablesConfiguration"><code>KubeProxyIPTablesConfiguration</code></a>
            </td>
            <td>
                <p>iptables містить параметри конфігурації, що стосуються iptables.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>ipvs</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPVSConfiguration"><code>KubeProxyIPVSConfiguration</code></a>
            </td>
            <td>
                <p>ipvs містить параметри конфігурації, що стосуються ipvs.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>nftables</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyNFTablesConfiguration"><code>KubeProxyNFTablesConfiguration</code></a>
            </td>
            <td>
                <p>nftables містить параметри конфігурації, що стосуються nftables.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>winkernel</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyWinkernelConfiguration"><code>KubeProxyWinkernelConfiguration</code></a>
            </td>
            <td>
                <p>winkernel містить параметри конфігурації, що стосуються winkernel.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>detectLocalMode</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-LocalMode"><code>LocalMode</code></a>
            </td>
            <td>
                <p>detectLocalMode визначає режим, який використовується для виявлення локального трафіку, стандартно — LocalModeClusterCIDR</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>detectLocal</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-DetectLocalConfiguration"><code>DetectLocalConfiguration</code></a>
            </td>
            <td>
                <p>detectLocal містить додаткові параметри конфігурації, що стосуються DetectLocalMode.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>clusterCIDR</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>clusterCIDR — це діапазон CIDR для Podʼів у кластері. (Для кластерів з подвійними стеками це може бути пара діапазонів CIDR, розділених комою). Коли DetectLocalMode встановлено в LocalModeClusterCIDR, kube-proxy буде вважати трафік локальним, якщо його вихідний IP знаходиться в цьому діапазоні. (Інакше не використовується.)</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>nodePortAddresses</code> <b>[Обовʼязкове]</b><br/>
                <code>[]string</code>
            </td>
            <td>
                <p>nodePortAddresses — це список діапазонів CIDR, які містять допустимі IP-адреси вузлів. Якщо встановлено, зʼєднання з сервісами NodePort будуть прийматися лише на IP-адресах вузлів в одному з вказаних діапазонів. Якщо не встановлено, зʼєднання NodePort будуть прийматися на всіх локальних IP.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>oomScoreAdj</code> <b>[Обовʼязкове]</b><br/>
                <code>int32</code>
            </td>
            <td>
                <p>oomScoreAdj — це значення oom-score-adj для процесу kube-proxy. Значення повинні бути в межах [-1000, 1000]</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>conntrack</code> <b>[Обовʼязкове]</b><br/>
                <a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConntrackConfiguration"><code>KubeProxyConntrackConfiguration</code></a>
            </td>
            <td>
                <p>conntrack містить параметри конфігурації, що стосуються conntrack.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>configSyncPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>configSyncPeriod — це інтервал часу, через який конфігурація з apiserver оновлюється. Має бути більше 0.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>portRange</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>portRange раніше використовувався для конфігурації проксі користувача, але тепер не використовується.</p>
            </td>
        </tr>
    </tbody>
</table>

## `DetectLocalConfiguration` {#kubeproxy-config-k8s-io-v1alpha1-DetectLocalConfiguration}

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

DetectLocalConfiguration містить необовʼязкові налаштування, що стосуються параметра DetectLocalMode

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>bridgeInterface</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>bridgeInterface — це імʼя інтерфейсу моста (bridge). Коли DetectLocalMode встановлено в LocalModeBridgeInterface, kube-proxy буде вважати трафік локальним, якщо він походить з цього моста.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>interfaceNamePrefix</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>interfaceNamePrefix — це префікс імені інтерфейсу. Коли DetectLocalMode встановлено в LocalModeInterfaceNamePrefix, kube-proxy буде вважати трафік локальним, якщо він походить з будь-якого інтерфейсу, чиє імʼя починається з цього префіксу.</p>
            </td>
        </tr>
    </tbody>
</table>

## `KubeProxyConntrackConfiguration` {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConntrackConfiguration}

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyConntrackConfiguration містить налаштування conntrack для
Kubernetes proxy server.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>maxPerCore</code> <b>[Обовʼязкове]</b><br/>
                <code>int32</code>
            </td>
            <td>
                <p>maxPerCore — максимальна кількість NAT зʼєднань, які слід відстежувати на однt процесорнt ядро (0 для того, щоб залишити обмеження без змін і проігнорувати min).</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>min</code> <b>[Обовʼязкове]</b><br/>
                <code>int32</code>
            </td>
            <td>
                <p>min — мінімальне значення записів connect-tracking, які слід виділити, незалежно від maxPerCore (встановіть maxPerCore=0, щоб залишити обмеження без змін).</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>tcpEstablishedTimeout</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>tcpEstablishedTimeout — як довго неактивне TCP зʼєднання буде зберігатися (наприклад, '2s'). Має бути більше 0 для встановлення.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>tcpCloseWaitTimeout</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>tcpCloseWaitTimeout — як довго неактивний запис conntrack у стані CLOSE_WAIT залишиться в таблиці conntrack (наприклад, '60s'). Має бути більше 0 для встановлення.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>tcpBeLiberal</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>tcpBeLiberal, якщо true, kube-proxy налаштує conntrack
                для роботи в ліберальному режимі для TCP зʼєднань, і пакети з
                послідовними номерами за межами вікна не будуть позначені як INVALID.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>udpTimeout</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>udpTimeout — як довго неактивний запис conntrack для UDP у стані UNREPLIED залишиться в таблиці conntrack (наприклад, '30s'). Має бути більше 0 для встановлення.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>udpStreamTimeout</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>udpStreamTimeout — як довго неактивний запис conntrack для UDP у стані ASSURED залишиться в таблиці conntrack (наприклад, '300s'). Має бути більше 0 для встановлення.</p>
            </td>
        </tr>
    </tbody>
</table>

## `KubeProxyIPTablesConfiguration` {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPTablesConfiguration}

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyIPTablesConfiguration містить налаштування, повʼязані з iptables,
для Kubernetes proxy server.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>masqueradeBit</code> <b>[Обовʼязкове]</b><br/>
                <code>int32</code>
            </td>
            <td>
                <p>masqueradeBit — біт iptables fwmark простору, який слід використовувати для SNAT, якщо використовується режим iptables або ipvs. Значення повинні бути в межах [0, 31].</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>masqueradeAll</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>masqueradeAll вказує kube-proxy виконувати SNAT для всього трафіку, надісланого на IP-адреси сервісів кластера, при використанні режиму iptables або ipvs. Це може бути необхідно для деяких плагінів CNI.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>localhostNodePorts</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>localhostNodePorts, якщо false, вказує kube-proxy вимкнути застарілу поведінку дозволу доступу до сервісів NodePort через localhost. (Застосовується лише для режиму iptables та IPv4;  localhost NodePorts ніколи не дозволяються з іншими режимами проксі або з IPv6.)</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>syncPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>syncPeriod — інтервал (наприклад, '5s', '1m', '2h22m'), що вказує, як часто виконуються різні операції повторної синхронізації та очищення. Має бути більше 0.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>minSyncPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>minSyncPeriod — мінімальний період між повторними синхронізаціями правил iptables (наприклад, '5s', '1m', '2h22m'). Значення 0 означає, що кожна зміна Service або EndpointSlice призведе до негайної повторної синхронізації iptables.</p>
            </td>
        </tr>
    </tbody>
</table>

## `KubeProxyIPVSConfiguration` {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPVSConfiguration}

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyIPVSConfiguration містить деталі конфігурації, що стосуються IPVS
для Kubernetes proxy server.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>syncPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>syncPeriod — інтервал (наприклад, '5s', '1m', '2h22m'), що вказує, як часто виконуються різні операції повторної синхронізації та очищення. Має бути більше 0.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>minSyncPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>minSyncPeriod — мінімальний період між повторними синхронізаціями правил IPVS (наприклад, '5s', '1m', '2h22m'). Значення 0 означає, що кожна зміна Service або EndpointSlice призведе до негайної повторної синхронізації IPVS.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>scheduler</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>scheduler — IPVS планувальник, який слід використовувати</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>excludeCIDRs</code> <b>[Обовʼязкове]</b><br/>
                <code>[]string</code>
            </td>
            <td>
                <p>excludeCIDRs — список CIDR, які IPVS proxier не повинен торкатися при очищенні IPVS сервісів.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>strictARP</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>strictARP налаштовує arp_ignore та arp_announce, щоб уникнути відповіді на ARP запити з інтерфейсу kube-ipvs0</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>tcpTimeout</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>tcpTimeout — значення тайм-ауту для неактивних IPVS TCP сесій. Стандартне значення — 0, що зберігає поточне значення тайм-ауту в системі.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>tcpFinTimeout</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>tcpFinTimeout — значення тайм-ауту для IPVS TCP сесій після отримання FIN. Стандартне значення — 0, що зберігає поточне значення тайм-ауту в системі.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>udpTimeout</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>udpTimeout — значення тайм-ауту для IPVS UDP пакетів. Стандартне значення — 0, що зберігає поточне значення тайм-ауту в системі.</p>
            </td>
        </tr>
    </tbody>
</table>

## `KubeProxyNFTablesConfiguration` {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyNFTablesConfiguration}

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyNFTablesConfiguration містить деталі конфігурації, що стосуються nftables для Kubernetes proxy server.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>masqueradeBit</code> <b>[Обовʼязкове]</b><br/>
                <code>int32</code>
            </td>
            <td>
                <p>masqueradeBit — це біт простору iptables fwmark, який слід використовувати для SNAT при використанні режиму nftables. Значення повинні бути в межах [0, 31].</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>masqueradeAll</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>masqueradeAll вказує kube-proxy, щоб SNAT весь трафік, що надходить на IP-адреси кластерів Service, при використанні режиму nftables. Це може бути необхідним для деяких CNI втулків.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>syncPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>syncPeriod — інтервал (наприклад, '5s', '1m', '2h22m'), що вказує, як часто виконуються різні операції повторної синхронізації та очищення. Має бути більше 0.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>minSyncPeriod</code> <b>[Обовʼязкове]</b><br/>
                <a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
            </td>
            <td>
                <p>minSyncPeriod — мінімальний період між повторними синхронізаціями правил iptables (наприклад, '5s', '1m', '2h22m'). Значення 0 означає, що кожна зміна Service або EndpointSlice призведе до негайної повторної синхронізації iptables.</p>
            </td>
        </tr>
    </tbody>
</table>

## `KubeProxyWinkernelConfiguration` {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyWinkernelConfiguration}

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyWinkernelConfiguration містить налаштування Windows/HNS для
Kubernetes proxy server.

<table class="table">
    <thead>
        <tr>
            <th width="30%">Поле</th>
            <th>Опис</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>networkName</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>networkName — це імʼя мережі, яку kube-proxy використовуватиме
                для створення точок доступу і політик.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>sourceVip</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>sourceVip — це IP-адреса джерела VIP точки доступу, яка використовується для NAT при балансуванні навантаження.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>enableDSR</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>enableDSR вказує kube-proxy, чи слід створювати HNS політики
                з DSR.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>rootHnsEndpointName</code> <b>[Обовʼязкове]</b><br/>
                <code>string</code>
            </td>
            <td>
                <p>rootHnsEndpointName — це імʼя hnsendpoint, яке прикріплене до
                l2bridge для кореневого простору мережі.</p>
            </td>
        </tr>
        <tr>
            <td>
                <code>forwardHealthCheckVip</code> <b>[Обовʼязкове]</b><br/>
                <code>bool</code>
            </td>
            <td>
                <p>forwardHealthCheckVip пересилає VIP сервісу для порту перевірки
                справності у Windows.</p>
            </td>
        </tr>
    </tbody>
</table>

## `LocalMode` {#kubeproxy-config-k8s-io-v1alpha1-LocalMode}
    
(Аліас для `string`)

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

LocalMode представляє режими для визначення локального трафіку з вузла.

## `ProxyMode` {#kubeproxy-config-k8s-io-v1alpha1-ProxyMode}
    
(Аліас для `string`)

**Зʼявляється у:**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

ProxyMode представляє режими, що використовуються сервером проксі Kubernetes.

На даний момент доступні два режими проксі на платформах Linux: 'iptables' та 'ipvs'. Один режим проксі доступний на платформах Windows: 'kernelspace'.

Якщо режим проксі не вказано, буде використано найкращий доступний режим проксі (на даний момент це `iptables` в Linux і `kernelspace` у Windows). Якщо вибраний режим проксі не може бути використаний (через відсутність підтримки в ядрі, відсутність компонентів користувацького простору тощо), kube-proxy вийде з помилкою.