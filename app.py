from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets 인증 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 사용할 Google Sheets 문서 열기
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PoEirMAOoH4cgUjV95w9pswOsYREsfx5VDHBWb01GGk/edit?gid=0#gid=0")  # ✅ ID 직접 사용
worksheet = sheet.sheet1  # 첫 번째 시트 사용

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    car_type = request.form['car_type']
    car_number = request.form['car_number']
    usage_type = request.form['usage_type']
    location = request.form['location']
    amount = request.form['amount']
    user = request.form['user']
    date = request.form['date']

    # Google Sheets에 데이터 추가
    worksheet.append_row([car_type, car_number, usage_type, location, amount, user, date])

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

# 시트 이름 리스트 출력 테스트
sheets = client.openall()
print("내가 접근할 수 있는 시트 목록:")
for s in sheets:
    print("-", s.title)
