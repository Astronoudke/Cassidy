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
        source_type = request.form.get('source_type')
        link = request.form.get('link')
        preprocessing_steps = request.form.getlist('preprocessing_steps')
        functionality = request.form.get('functionality')

        if source_type == 'Online forum discussion':
            message_class = request.form.get('message_class')
            pagination_class = request.form.get('pagination_class')
            message_text_class = request.form.get('message_text_class')
            message_author_class = request.form.get('message_author_class')
            analyzer = ForumAnalyzer(link, message_class, False, pagination_class, message_text_class,
                                     message_author_class)
        else:
            analyzer = ScientificLiteratureAnalyzer(link)

        result = analyzer.analyze(functionality=functionality, preprocessing_steps=preprocessing_steps)
        session['result'] = result

        def background_analysis():
            result = analyzer.analyze(functionality=functionality, preprocessing_steps=preprocessing_steps)
            session['result'] = result

        # Start the background task and then immediately redirect to the loading page
        threading.Thread(target=background_analysis).start()
        return redirect(url_for('loading'))

    return render_template('home.html')


@app.route('/loading', methods=['GET'])
def loading():
    return render_template('loading.html')


@app.route('/result')
def result():
    result = session.get('result')
    return render_template('result.html', result=result)