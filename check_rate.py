import os
import json
import smtplib
from email.mime.text import MIMEText
from datetime import date
import yfinance as yf

THRESHOLD_PERCENT = 0.5
STATE_FILE = "last_rate.json"

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]


def get_usdkrw():
    ticker = yf.Ticker("KRW=X")
    hist = ticker.history(period="5d")
    prev_close = hist["Close"].iloc[-2]
    current = hist["Close"].iloc[-1]
    change_pct = (current - prev_close) / prev_close * 100
    return current, prev_close, change_pct


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except json.JSONDecodeError:
            pass
    return {"alerted_date": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send_alert_email(current, prev_close, change_pct):
    subject = f"[환율 알림] USD/KRW {change_pct:+.2f}% 변동"
    body = (
        f"현재 환율: {current:.2f}원\n"
        f"전일 종가: {prev_close:.2f}원\n"
        f"변동률: {change_pct:+.2f}%\n"
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print("메일 발송 완료")


def main():
    state = load_state()
    today_str = str(date.today())

    current, prev_close, change_pct = get_usdkrw()
    print(f"현재 {current:.2f}원 (전일대비 {change_pct:+.2f}%)")

    if abs(change_pct) >= THRESHOLD_PERCENT and state.get("alerted_date") != today_str:
        send_alert_email(current, prev_close, change_pct)
        state["alerted_date"] = today_str
    else:
        print("조건 미충족 또는 오늘 이미 발송함")

    save_state(state)


if __name__ == "__main__":
    main()