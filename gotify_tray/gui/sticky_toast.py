"""Windows 常驻 toast 通知。

通过 PowerShell 调 WinRT 通知 API，弹 Scenario=reminder 的系统 toast：
不点掉不消失（Win10/11 原生行为），无需任何第三方依赖。
非 Windows 或任何失败都返回 False，由调用方回退 QSystemTrayIcon 气泡。
"""

import base64
import html
import logging
import subprocess
import sys

logger = logging.getLogger("gotify-tray")

# PowerShell 自带的 AUMID：未注册 AUMID 的脚本程序用它才能弹系统通知
_POWERSHELL_AUMID = (
    r"{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}"
    r"\WindowsPowerShell\v1.0\powershell.exe"
)

_CREATE_NO_WINDOW = 0x08000000


def _build_script(title: str, body: str) -> str:
    # 单引号 here-string 不做插值，只有行首 '@ 会终止，防御性处理一下
    xml_text = html.escape(body, quote=False).replace("\n'@", "\n '@")
    xml = (
        '<toast scenario="reminder" activationType="system" arguments="dismiss">'
        "<visual><binding template=\"ToastGeneric\">"
        f"<text>{html.escape(title, quote=False)}</text>"
        f"<text>{xml_text}</text>"
        '</binding></visual>'
        '<actions><action content="知道了" arguments="dismiss" '
        'activationType="system"/></actions>'
        '<audio silent="true"/>'
        "</toast>"
    )
    return (
        "[Windows.UI.Notifications.ToastNotificationManager,"
        " Windows.UI.Notifications, ContentType = WindowsRuntime] > $null\n"
        "[Windows.Data.Xml.Dom.XmlDocument,"
        " Windows.Data.Xml.Dom, ContentType = WindowsRuntime] > $null\n"
        f"$xmlText = @'\n{xml}\n'@\n"
        "$xml = New-Object Windows.Data.Xml.Dom.XmlDocument\n"
        "$xml.LoadXml($xmlText)\n"
        "$toast = New-Object Windows.UI.Notifications.ToastNotification($xml)\n"
        "[Windows.UI.Notifications.ToastNotificationManager]"
        f"::CreateToastNotifier('{_POWERSHELL_AUMID}').Show($toast)\n"
    )


def show_sticky(title: str, body: str) -> bool:
    if sys.platform != "win32":
        return False
    try:
        encoded = base64.b64encode(
            _build_script(title, body).encode("utf-16-le")
        ).decode("ascii")
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
            creationflags=_CREATE_NO_WINDOW,
            timeout=15,
            check=True,
        )
        return True
    except Exception:
        logger.exception("sticky toast failed, fallback to tray balloon")
        return False
