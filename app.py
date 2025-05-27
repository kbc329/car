import base64
import json
import os
from flask import Flask, request, render_template, redirect
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv

# .env 로컬 개발용
load_dotenv()

app = Flask(__name__)

# Google Sheets API scope
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


# base64 인코딩된 GOOGLE_CREDENTIALS_BASE64 환경변수 읽기
encoded = os.getenv("GOOGLE_CREDENTIALS_BASE64")
if not encoded:
    raise ValueError("GOOGLE_CREDENTIALS_BASE64 환경변수가 설정되지 않았습니다.")

# base64 → bytes → json 문자열 디코딩
decoded_bytes = base64.b64decode(encoded)
creds_json = decoded_bytes.decode("utf-8")

# JSON 문자열 → dict로 변환
creds_dict = json.loads(creds_json)

# Credentials 생성
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
gc = gspread.authorize(creds)

# Google Sheets 열기 (시트 이름은 실제 사용 중인 이름으로 맞춰야 함)
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

    today = datetime.today().strftime("%Y-%m-%d")
    return render_template("form.html", today=today)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
