"""Windows 常驻 toast 通知。

直接用 winrt-runtime 调 Windows 通知 API，scenario=reminder：
不点掉不消失，带「知道了」system-dismiss 按钮。
非 Windows 或任何失败返回 False，由调用方回退 QSystemTrayIcon 气泡。
"""

import html
import logging
import re
import sys

logger = logging.getLogger("gotify-tray")

# PowerShell 自带的 AUMID：未注册 AUMID 的程序借它才能弹系统通知
_AUMID = r"{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"

_URL_RE = re.compile(r"https?://[^\s<>\"']+")


def _build_xml(title: str, body: str) -> str:
    # toast 子元素顺序固定: visual -> audio -> actions，乱序会被静默丢弃
    # 消息带 URL 时加「打开链接」protocol 按钮（toast 本体 protocol 激活
    # 在未注册 AUMID 下不可靠，按钮走 shell 处理最稳）
    url = _URL_RE.search(f"{title}\n{body}")
    actions = '<actions><action content="知道了" arguments="dismiss" activationType="system"/>'
    if url:
        actions += (
            '<action content="打开链接" arguments="'
            + html.escape(url.group(0), quote=True)
            + '" activationType="protocol"/>'
        )
    actions += "</actions>"
    return (
        '<toast scenario="reminder" activationType="system" arguments="dismiss">'
        '<visual><binding template="ToastGeneric">'
        f"<text>{html.escape(title, quote=False)}</text>"
        f"<text>{html.escape(body, quote=False)}</text>"
        "</binding></visual>"
        '<audio silent="true"/>'
        + actions
        + "</toast>"
    )


def show_sticky(title: str, body: str) -> bool:
    if sys.platform != "win32":
        return False
    try:
        from winrt.windows.data.xml.dom import XmlDocument
        from winrt.windows.ui.notifications import (
            ToastNotification,
            ToastNotificationManager,
        )

        xml = XmlDocument()
        xml.load_xml(_build_xml(title, body))
        ToastNotificationManager.create_toast_notifier_with_id(_AUMID).show(
            ToastNotification(xml)
        )
        return True
    except Exception:
        logger.exception("sticky toast failed, fallback to tray balloon")
        return False
