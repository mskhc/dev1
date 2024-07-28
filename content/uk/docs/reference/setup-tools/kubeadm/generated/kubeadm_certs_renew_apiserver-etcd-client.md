
Поновлює сертифікат, який apiserver використовує для доступу до etcd

### Опис {#synopsis}

Поновлює сертифікат, який apiserver використовує для доступу до etcd.

Поновлення виконується безумовно, незалежно від дати закінчення терміну дії сертифіката; додаткові атрибути, такі як SAN, будуть базуватися на наявних файлах/сертифікатах, нема потреби їх поновлювати.

Типово поновлення намагається використовувати центр сертифікації в локальному PKI, керованому kubeadm; як альтернативу можна використовувати API сертифікатів K8s для поновлення сертифікатів, або, як останній варіант, згенерувати CSR запит.

Після оновлення, щоб зміни набули чинності, необхідно перезапустити компоненти панелі управління та, зрештою, повторно розповсюдити оновлений сертифікат у випадку, якщо файл використовується деінде.

```shell
kubeadm certs renew apiserver-etcd-client [flags]
```

### Параметри {#options}

<table style="width: 100%; table-layout: fixed;">
    <colgroup>
        <col span="1" style="width: 10px;" />
        <col span="1" />
    </colgroup>
    <tbody>
        <tr>
            <td colspan="2">--cert-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Типово: "/etc/kubernetes/pki"</td>
        </tr>
        <tr>
            <td></td>
            <td style="line-height: 130%; word-wrap: break-word;"><p>Шлях, де будуть збережені сертифікати</p></td>
        </tr>
        <tr>
            <td colspan="2">--config string</td>
        </tr>
        <tr>
            <td></td>
            <td style="line-height: 130%; word-wrap: break-word;"><p>Шлях до конфігураційного файлу kubeadm.</p></td>
        </tr>
        <tr>
            <td colspan="2">-h, --help</td>
        </tr>
        <tr>
            <td></td>
            <td style="line-height: 130%; word-wrap: break-word;"><p>Довідка apiserver-etcd-client</p></td>
        </tr>
        <tr>
            <td colspan="2">--kubeconfig string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Типово: "/etc/kubernetes/admin.conf"</td>
        </tr>
        <tr>
            <td></td>
            <td style="line-height: 130%; word-wrap: break-word;"><p>Файл kubeconfig, який використовується для спілкування з кластером. Якщо прапорець не встановлено, може буити переглянутий набір стандартних місць для пошуку наявного файлу kubeconfig.</p></td>
        </tr>
    </tbody>
</table>

### Параметри успадковані від батьківських команд {#options-inherited-from-parent-commands}

<table style="width: 100%; table-layout: fixed;">
    <colgroup>
        <col span="1" style="width: 10px;" />
        <col span="1" />
    </colgroup>
    <tbody>
        <tr>
            <td colspan="2">--rootfs string</td>
        </tr>
        <tr>
            <td></td>
            <td style="line-height: 130%; word-wrap: break-word;"><p>[EXPERIMENTAL] Шлях до реальної кореневої файлової системи хоста.</p></td>
        </tr>
    </tbody>
</table>