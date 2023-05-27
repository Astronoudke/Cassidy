from flask import Flask, request, redirect, render_template, url_for, session
import threading
import os
import time
import json

import sys
sys.path.append('C:\\Users\\noudy\\PycharmProjects\\Cassidy\\application')

from F_UserInterface.ApplicationManager.application_manager import ScientificLiteratureAnalyzer, ForumAnalyzer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploaded_files')
app.secret_key = 'your_secret_key_here'  # Change to your actual secret key

@app.route('/', methods=['GET', 'POST'])
def home():
    recommended_steps = {
        'sentiment_analysis': ['clean_data'],
        'summarize': ['clean_data', 'split_sentences'],
        'relation_extractor': ['clean_data', 'case_folding', 'split_sentences', 'tokenize', 'pos_tagging', 'filter_pos_tagged'],
        # Add more mappings as necessary
    }

    if request.method == 'POST':
        session['source_type'] = request.form.get('source_type')

        if 'pdf_file' in request.files and session['source_type'] == 'Scientific article':
            pdf_file = request.files['pdf_file']
            if pdf_file.filename != '':  # check if file has been uploaded
                print("True")
                # Add a timestamp to the filename
                filename = str(time.time()) + "_" + pdf_file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                pdf_file.save(file_path)
                session['link'] = file_path  # The link now contains local file path
            else:
                print("False")
                session['link'] = request.form.get('link')
        else:
            print("False")
            session['link'] = request.form.get('link')

        session['preprocessing_steps'] = request.form.get('preprocessing_steps_order').split(",")
        session['functionality'] = request.form.get('functionality')

        if session['source_type'] == 'Online forum discussion':
            session['message_class'] = request.form.get('message_class')
            session['pagination_class'] = request.form.get('pagination_class')
            session['message_text_class'] = request.form.get('message_text_class')
            session['message_author_class'] = request.form.get('message_author_class')

        return redirect(url_for('loading'))

    return render_template('home.html', recommended_steps=recommended_steps)


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

    result = analyzer.analyze(functionality=functionality, preprocessing_steps=preprocessing_steps)
    # Convert the result to JSON and save it to a file
    result_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{time.time()}_result.json")
    with open(result_filename, 'w') as f:
        json.dump(result, f)

    # Save the filename in the session instead of the result itself
    session['result_filename'] = result_filename

    return redirect(url_for('result'))

@app.route('/result')
def result():
    result_filename = session.get('result_filename')
    # Read the result from the file
    with open(result_filename, 'r') as f:
        result = json.load(f)

    functionality = session.get('functionality')

    # Remove the result file
    if os.path.exists(result_filename):
        os.remove(result_filename)

    if functionality == 'sentiment_analysis':
        avg_sentiment = sum(result.values()) / len(result)
        return render_template('result_sentiment.html', result=result, avg_sentiment=avg_sentiment)
    elif functionality == 'summarize':
        return render_template('result_summary.html', result=result)
    elif functionality == 'relation_extractor':
        return render_template('result_relation.html', result=result)
    else:
        return render_template('result.html', result=result)  # fallback


if __name__ == '__main__':
    app.run(debug=True)
