import pickle, os
from flask import Flask, render_template, request
from janome.tokenizer import Tokenizer
app = Flask(__name__, static_folder='.', static_url_path='')

def tokenizer(sentence):
    t = Tokenizer()
    return t.tokenize(sentence, wakati = True)

#学習結果をpickleファイルより取得
#tokenizerは読み込みがうまくいかなかったので、再度設定
url = '/home/onishiyutaro/movieclassifier'
pipe_lr \
    = pickle.load(open(os.path.join(url, 'clf.pkl'), 'rb'))
pipe_lr.set_params(count__tokenizer=tokenizer)

def classify(document):
    label = {0:'悪い', 1:'良い'}
    document_array = []
    document_array.append(document)
    predict = pipe_lr.predict(document_array)
    return label[predict[0]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        reviewInput = request.form['reviewInput']
        predict = classify(reviewInput)
        return render_template('results.html', \
                                reviewInput=reviewInput, predict=predict)

if __name__ == '__main__':
    app.run(debug=True)
