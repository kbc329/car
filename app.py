from flask import Flask, render_template, request, redirect
import openpyxl
import os

app = Flask(__name__)

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

    file_path = r'C:\Users\ktmos\OneDrive\바탕 화면\주차소액관리\data.xlsx'


    if os.path.exists(file_path):
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['차종', '차량번호', '사용용도', '사용처', '사용금액', '사용자', '날짜'])

    ws.append([car_type, car_number, usage_type, location, amount, user, date])
    wb.save(file_path)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
