from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 📌 현재 접근 가능한 Google Sheets 이름 출력
print("접근 가능한 구글 시트들:")
print([sheet.title for sheet in client.openall()])  # 👈 여기서 "주차소액관리" 확인 가능

# ✅ 아래에 정확한 시트 이름을 복사해서 붙여 넣으세요!
sheet = client.open("주차소액관리").sheet1

@app.route('/')
def index():
    return render_template('form.html')  # HTML 폼 템플릿 이름

@app.route('/submit', methods=['POST'])
def submit():
    car_type = request.form['car_type']
    car_number = request.form['car_number']
    purpose = request.form['purpose']
    place = request.form['place']
    amount = request.form['amount']
    user = request.form['user']
    date = request.form['date']  # 사용자 입력 날짜 사용

    data = [car_type, car_number, purpose, place, amount, user, date]  # 날짜는 마지막 열
    sheet.append_row(data)
    return '저장되었습니다!'

if __name__ == '__main__':
    app.run(debug=True)
