import os
from config import AM_URL

def text_notice_card(a: dict) -> dict:
    """生成一个"文本通知型"卡片"""
    labels = a.get("labels", {})
    ann = a.get("annotations", {})
    sev = labels.get("severity", "info")
    color = {"critical":"warning","warning":"comment"}.get(sev.lower(), "info")

    return {
      "msgtype": "template_card",
      "template_card": {
        "card_type": "text_notice",
        "source": {"icon_url": "", "desc": "Notice Robot", "desc_color": 0},
        "main_title": {"title": labels.get("alertname","Alert"),
                       "desc": ann.get("summary") or ann.get("description") or ""},
        "emphasis_content": {"title": sev.upper()},
        "sub_title_text": f"{labels.get('instance','-')}",
        "horizontal_content_list": [
          {"keyname":"status", "value": a.get("status","firing")},
          {"keyname":"startsTime", "value": a.get("startsAt","")},
        ],
        "jump_list": [
          {"type":1, "title":"Open Grafana",
           "url": a.get("generatorURL") or AM_URL}
        ],
        "card_action": {"type":1, "url": a.get("generatorURL") or AM_URL}
      }
    }
