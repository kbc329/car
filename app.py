from flask import Flask, request, render_template, redirect
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from datetime import datetime

app = Flask(__name__)

# Google Sheets 인증 (환경변수 사용)
creds_json = os.getenv("GOOGLE_CREDENTIALS")  # ✅ 환경변수 이름 변경됨
if not creds_json:
    raise ValueError("GOOGLE_CREDENTIALS 환경변수가 설정되지 않았습니다.")

creds_json = creds_json.replace("\\n", "\n")

creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict)
gc = gspread.authorize(creds)

# 구글 시트 열기 (시트 이름을 실제 사용 중인 이름으로 유지)
SHEET_NAME = "차량_영수증"
sh = gc.open(SHEET_NAME)
worksheet = sh.sheet1

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "날짜": request.form.get("date"),
            "차종": request.form.get("car_type"),
            "차량번호": request.form.get("car_number"),
            "사용용도": request.form.get("usage"),
            "사용처": request.form.get("place"),
            "사용금액": request.form.get("amount"),
            "사용자": request.form.get("user")
        }

        # Google Sheets에 추가
        worksheet.append_row([
            data["날짜"],
            data["차종"],
            data["차량번호"],
            data["사용용도"],
            data["사용처"],
            data["사용금액"],
            data["사용자"]
        ])
        return redirect("/")

    # 기본값: 오늘 날짜
    today = datetime.today().strftime("%Y-%m-%d")
    return render_template("index.html", today=today)
