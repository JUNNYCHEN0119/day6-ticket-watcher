import requests
import time
from bs4 import BeautifulSoup

WEBHOOK_URL = "https://discord.com/api/webhooks/1462827312000008427/HETzd8grblNohYE2F_Hj4Ia4N9D8eH77BWJAI8nJ87QtP6oml6fGh7unTnEOkYh5BRtA"

URL = "https://tixcraft.com/activity/detail/26_day6"

CHECK_INTERVAL = 30

last_status = {
    "0307": False,
    "0308": False
}

def send_discord(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def check_ticket():
    global last_status
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text()

    results = {
        "0307": "2026/03/07" in text and "售完" not in text,
        "0308": "2026/03/08" in text and "售完" not in text
    }

    for day, available in results.items():
        if available and not last_status[day]:
            send_discord(
                f"🎫【DAY6 清票通知】\n\n"
                f"📅 日期：2026/{day[:2]}/{day[2:]}\n"
                f"🎟 狀態：可能已可購買（清票）\n\n"
                f"👉 https://tixcraft.com/activity/detail/26_day6"
            )
        last_status[day] = available

if __name__ == "__main__":
    send_discord("🤖 DAY6 監票系統已啟動")
    while True:
        check_ticket()
        time.sleep(CHECK_INTERVAL)
