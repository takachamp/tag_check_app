from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import numpy as np
import os

classes = ['水温30℃を限度に、洗濯機で洗えます。',
                '水温30℃を限度に、洗濯機で弱い洗濯ができます。',
                '水温30℃を限度に、洗濯機で非常に弱い洗濯ができます。',
                '水温40℃を限度に、洗濯機で洗えます',
                '水温40℃を限度に、洗濯機で弱い洗濯ができます。',
                '水温40℃を限度に、洗濯機で非常に弱い洗濯ができます。',
                '水温50℃を限度に、洗濯機で洗えます。',
                '水温50℃を限度に、洗濯機で弱い洗濯ができます。',
                '水温60℃を限度に、洗濯機で洗えます。',
                '水温70℃を限度に、洗濯機で洗えます。',
                '水温95℃を限度に、洗濯機で洗えます。',
                '漂白できません。',
                '塩素系・酸素系漂白剤で、漂白できます。',
                '酸素系漂白剤で、漂白できます。塩素系ではできません。',
                'パークロロエチレン及び石油系溶剤による、ドライクリーニングができます。',
                'ドライクリーニングはできません。',
                'パークロロエチレン及び石油系溶剤による、弱いドライクリーニングができます。',
                '平干しが良いでしょう。',
                '日陰の平干しが良いでしょう。',
                '日陰で、脱水せずぬれたまま平干しします。',
                '脱水せずぬれたまま、平干しします。',
                '石油系溶剤による、ドライクリーニングができます。',
                '石油系溶剤による弱いドライクリーニングができます。',
                '液温は40℃を限度とし手洗いができます。',
                'ハンガー等を使って、つり干しします。',
                '日陰で、脱水せずぬれたままつり干しします。',
                '日陰で、つり干しします。',
                '脱水せずぬれたまま、つり干しします。',
                'ご家庭では洗えません。',
                'アイロンは使えません。',
                '110℃を限度に、スチームなしでアイロンが使えます。',
                '150℃を限度に、アイロンが使えます。',
                '200℃を限度に、アイロンが使えます。',
                'タンブル乾燥禁止です。',
                '排気温度60℃を上限に、タンブル乾燥できます。',
                '排気温度80℃を上限に、タンブル乾燥できます。',
                '非常に弱い操作による、ウエットクリーニングができます。',
                '弱い操作による、ウエットクリーニングができます。',
                'ウエットクリーニングができます。',
                'ウエットクリーニングはできません。']

en_classes = ['Can wash in warm water up to 30°C, depending on washing machine.',
                'Can wash in warm water up to 30°C, using mild cycle in washing machine.',
                'Can wash in warm water up to 30°C, using delicate cycle in washing machine.',
                'Can wash in how water up to 40°C, depending on washing machine.',
                'Can wash in warm water up to 40°C, using mild cycle in washing machine.',
                'Can wash in warm water up to 40°C, using delicate cycle in washing machine.',
                'Can wash in hot water up to 50°C, depending on washing machine.',
                'Can wash in warm water up to 50°C, using mild cycle in washing machine.',
                'Can wash in how water up to 60°C, depending on washing machine.',
                'Can wash in how water up to 70°C, depending on washing machine.',
                'Can wash in how water up to 95°C, depending on washing machine.',
                'Chlorine and oxygen bleach use prohibited.',
                'Can be bleached with chlorine and oxygen bleach',
                'Can use the oxygen bleach, but the chlorine bleach is prohibited.',
                'May be dry-cleaned with tetrachloroethylene or a petroleum-based substance.',
                'Do not dry clean.',
                'May be dry-cleaned in a light-operating machine, with tetrachloroethylene or a petoroleum-based substance.',
                'Let dry on flat surface.',
                'Let dry on flat surface in the shade.',
                'Make clothes of the wet state dry in a flat surface.',
                'Make clothes of the wet state dry in a flat surface in the shade.',
                'May be dry-cleaned  with a petroleum-based substance.',
                'May be dry-cleaned in a light-operating machine with a petroleum-based substance.',
                'Can wash in water up to 40°C, by hand only.(do not use washing machine.)',
                'Dry by hanging.',
                'Hung wet clothes and dry in the shade.',
                'Dry by hanging in the shade.',
                'Hung wet clothed and dry.',
                'Can not wash at home.',
                'Do not iron.',
                'Iron at no more than 110°C. Do not use steam.',
                'Iron at no more than 150°C.',
                'Iron at no more than 200°C.',
                'Do not tumble dry.',
                'Tumble dry processing by the low temperature can be done.(Exhaust temperature maximum 60°C.',
                'Tumble dry processing can be done.(Exhausttemperature maximum 80°C.',
                'May be wet-cleaned only with very mild mechanical action.',
                'May be wet-cleaned with mild mechanical action.',
                'May be wet-cleaned with a usual amount of mechanical action.',
                'Do not wet-clean.']

num_classes = len(classes)
image_size = 50
color_setting = 3

app = Flask(__name__, static_folder='static')

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/jp_main', methods = ['GET'])
def jp_main():
    menu_name = "日本語"
    return render_template("jp_main.html")

@app.route('/en_main', methods = ['GET'])
def en_main():
    menu_name = "English"
    return render_template("en_main.html")

@app.route('/jp_list', methods=["GET"])
def jp_list():
  menu_name = "洗濯タグ一覧表示"
  return render_template("jp_list.html")

@app.route('/jp_list_2', methods=["GET"])
def jp_list_2():
  menu_name = "洗濯タグ一覧表示2"
  return render_template("jp_list_2.html")

@app.route('/en_list', methods=['GET'])
def en_list():
    menu_name = "List of Cleaning Tag"
    return render_template("en_list.html")

@app.route('/en_list_2', methods=["GET"])
def en_list_2():
  menu_name = "List of Cleaning Tag_2"
  return render_template("en_list_2.html")

@app.route('/jp_check', methods=['GET', 'POST'])
def jp_check():
    menu_name = "AIでチェック"
    return render_template("jp_check.html")

@app.route("/en_check", methods=['GET'])
def en_check():
    menu_name = "Check with AI"
    return render_template("en_check.html")

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['GET','POST'])
def uploads_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            model = load_model('./vgg16_model.h5')

            im = Image.open(filepath)
            img = im.resize((image_size, image_size))
            img = img.convert(mode='RGB')
            img = img_to_array(img)
            img = img.reshape(image_size, image_size, color_setting)

            result = model.predict(np.array([img]))[0]
            predicted = result.argmax()
            percentage = float(result[predicted] * 100)
            
            resultmsg = classes[predicted]
            percentagemsg = "確率: "+ str(percentage) + "%"
            return render_template('jp_result.html',resultmsg=resultmsg, percentagemsg=percentagemsg ,filepath=filepath)
    return render_template('jp_check.html')

@app.route('/en_predict', methods=['GET','POST'])
def en_uploads_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            model = load_model('./vgg16_model.h5')

            im = Image.open(filepath)
            img = im.resize((image_size, image_size))
            img = img.convert(mode='RGB')
            img = img_to_array(img)
            img = img.reshape(image_size, image_size, color_setting)

            result = model.predict(np.array([img]))[0]
            predicted = result.argmax()
            percentage = float(result[predicted] * 100)
            
            en_resultmsg = en_classes[predicted]
            en_percentagemsg = "probability: "+ str(percentage) + "%"
            return render_template('en_result.html',en_resultmsg=en_resultmsg, en_percentagemsg=en_percentagemsg ,filepath=filepath)
    return render_template('en_check.html')

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)