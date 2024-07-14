
Генерує приватний ключ для підпису токенів службових облікових записів, що дозволяє їм мати власні публічні ключі

### Опис {#synopsis}

Генерує приватний ключ для підпису токенів службових облікових записів, що дозволяє їм мати власні публічні ключі, та записує їх у файли sa.key та sa.pub.

Якщо обидва файли вже існують, kubeadm пропускає крок генерації та використовує наявні файли.

```shell
kubeadm init phase certs sa [flags]
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
            <td colspan="2">-h, --help</td>
        </tr>
        <tr>
            <td></td>
            <td style="line-height: 130%; word-wrap: break-word;"><p>Довідка sa</p></td>
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
