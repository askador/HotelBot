import csv
from flask import request, jsonify
from app import app
from server.generate_gpt_response import generate_gpt_response
from text_contains_kwrds import text_contains_kwrds

keywords = []

with open('./data/hotel-keywords.csv') as f:
    reader = csv.reader(f)
    keywords += [row[0] for row in reader]
    

@app.route('/question', methods=["POST"])
def get_gpt_answer():
    data = request.get_json()
    
    if not data:
        return jsonify('')
    
    question = data.get('question')
    
    if not question:
        return jsonify('')
    
    question = str(question).strip()
    
    if not text_contains_kwrds(question, keywords):
        answer = 'I am sorry, but your question is not relevant to our hotel.'
        return jsonify(answer)
    
    answer = generate_gpt_response(question)
    
    return jsonify(answer)