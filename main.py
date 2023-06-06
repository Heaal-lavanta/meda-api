from flask import Flask, request
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'contact.meda.app@gmail.com'
receiver_email = 'berathanyedibela7@gmail.com'
password = 'kwabjhyxapebgjsq'
app = Flask(__name__)


def mailgönder(adres,urun,miktar):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Yardim Dağitimi hk.'

    body = f"""
Merhaba,

{adres} Konumunda , {miktar} adet {urun} malzemesi dağitimi yapilacaktir, bilginize.

İyi günler.
"""
    message.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

def json_oku(dosya_adi):
    with open("./"+dosya_adi, encoding="utf-8") as dosya:
        return json.load(dosya)

def json_yaz(oyun, dosya_adi):
    with open("./"+dosya_adi, 'w', encoding="utf-8") as dosya:
        json.dump(oyun, dosya)

@app.route('/')
def hello():
    return 'Merhaba, Meda dünyasina hoş geldiniz!'

@app.route('/register', methods=['GET'])
def register():
    args = request.args
    seckey = "DKOEFE-232320-AWDWOP"
    key = args['key']
    ad = args['ad']
    soyad = args['soyad']
    email = args['email']
    phone = args['phone']
    password = args['password']
    json_status = {
        "status": "",
        "ad": "",
        "soyad": "",
        "error": ""
    }
    if key == seckey:
        jsondata = json_oku("users.json")
        for i in jsondata['data']:
            if i['email'] == email:
                json_status['status'] = "False"
                json_status['error'] = "Bu mail daha önce kullanilmiş!"
                return json.dumps(json_status)
            if i['phone'] == phone:
                json_status['status'] = "False"
                json_status['error'] = "Bu numara daha önce kullanilmiş!"
                return json.dumps(json_status)
        jsonham = {
            "name": ad,
            "surname": soyad,
            "email": email,
            "phone": phone,
            "password": password
        }
        jsondata['data'].append(jsonham)
        json_yaz(jsondata, "users.json")
        json_status['status'] = "True"
        json_status['ad'] = ad
        json_status['soyad'] = soyad
        return json.dumps(json_status)
    else:
        data = {
            "status": "False",
            "error": "güvenlik keyi hatali"
        }
        return json.dumps(data)

@app.route('/login', methods=['GET'])
def login():
    args = request.args
    email = args['email']
    password = args['password']
    jsondata = json_oku("users.json")
    for user in jsondata['data']:
        if user['email'] == email and user['password'] == password:
            data = {
                "status": "True",
                "message": "Giriş başarili!"
            }
            return json.dumps(data)
    data = {
        "status": "False",
        "error": "Giriş başarisiz! Kullanici adi veya şifre hatali."
    }
    return json.dumps(data)

@app.route("/yardimget", methods=['GET'])
def yardimget():
    args = request.args
    phone = args['phone']
    sehir = args['sehir']
    ilce = args['ilce']
    mahalle = args['mahalle']
    sokak = args['sokak']
    urun = args['urun']
    miktar = args['miktar']
    key = args['key']
    seckey = "DKOEFE-232320-AWDWOP"
    
    jsondata = json_oku("yardim.json")
    
    json_data = {
        "phone": "",
        "adres": "",
        "urun": "",
        "miktar": ""
    }
    
    if key == seckey:
        adres = f"{mahalle} mahallesi, {sokak} sokak, {ilce}/{sehir}"
        json_data['adres'] = adres
        json_data['phone'] = phone
        json_data['urun'] = urun
        json_data['miktar'] = miktar
        
        jsondata['data'].append(json_data)
        mailgönder(adres,urun,miktar)
        json_yaz(jsondata, "yardim.json")  
        
        return json_data, 200  
    else:
        data = {
            "status": "False",
            "error": "güvenlik keyi hatali"
        }
        return json.dumps(data), 401  
    
@app.route("/yardimlist", methods=['GET'])
def yardimlist():
    args = request.args
    key = args['key']
    seckey = "DKOEFE-232320-AWDWOP"
    
    
    if key == seckey:
        
        
       
        json_data = json_oku("yardim.json")  
        
        return json_data, 200  
    else:
        data = {
            "status": "False",
            "error": "güvenlik keyi hatali"
        }
        return json.dumps(data), 401  


if __name__ == '__main__':
    app.run(debug=True)