
Готує машину до обслуговування панелі управління

### Опис {#synopsis}

Готує машину до обслуговування панелі управління.

```shell
kubeadm join phase control-plane-prepare [flags]
```

### Приклади {#examples}

```shell
# Готує машину до обслуговування панелі управління
kubeadm join phase control-plane-prepare all
```

### Параметри {#options}

<table style="width: 100%; table-layout: fixed;">
    <colgroup>
        <col span="1" style="width: 10px;" />
        <col span="1" />
    </colgroup>
    <tbody>
        <tr>
            <td colspan="2">-h, --help</td>
        </tr>
        <tr>
            <td></td>
            <td style="line-height: 130%; word-wrap: break-word;"><p>Довідка control-plane-prepare</p></td>
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