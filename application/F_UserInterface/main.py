from flask import Flask, request, redirect, render_template, url_for, session
import threading

import sys
sys.path.append('C:\\Users\\noudy\\PycharmProjects\\Cassidy\\application')

from F_UserInterface.ApplicationManager.application_manager import ScientificLiteratureAnalyzer, ForumAnalyzer

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to your actual secret key

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['source_type'] = request.form.get('source_type')
        session['link'] = request.form.get('link')
        session['preprocessing_steps'] = request.form.get('preprocessing_steps_order').split(",")
        session['functionality'] = request.form.get('functionality')

        if session['source_type'] == 'Online forum discussion':
            session['message_class'] = request.form.get('message_class')
            session['pagination_class'] = request.form.get('pagination_class')
            session['message_text_class'] = request.form.get('message_text_class')
            session['message_author_class'] = request.form.get('message_author_class')

        return redirect(url_for('loading'))

    return render_template('home.html')

@app.route('/loading', methods=['GET'])
def loading():
    functionality = session['functionality']
    preprocessing_steps = session['preprocessing_steps']

    if session['source_type'] == 'Online forum discussion':
        analyzer = ForumAnalyzer(session['link'], session['message_class'], False, session['pagination_class'],
                                 session['message_text_class'],
                                 session['message_author_class'])
    else:
        analyzer = ScientificLiteratureAnalyzer(session['link'])

    print(preprocessing_steps)

    result = analyzer.analyze(functionality=functionality, preprocessing_steps=preprocessing_steps)
    session['result'] = result

    return redirect(url_for('result'))

@app.route('/result')
def result():
    result = session.get('result')
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
