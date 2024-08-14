from flask import Flask, request, jsonify
from lib.aadecode import decode
import re
import base64

app = Flask(__name__)

@app.route('/decode', methods=['POST'])
def decode_string():
    encoded_string = request.form.get('abyss')
    
    if not encoded_string:
        return jsonify({'error': 'No string provided'}), 400
    
    try:
        decoded_string = decode(encoded_string)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    match = re.search(r'(?<=JSON\.parse\(atob\(")([^"]+)(?="\)\))', decoded_string)
    
    if not match:
        return jsonify({'error': 'No match found in decoded string'}), 400
    
    if match:
        base64_string = match.group(1)
        json_string = base64.b64decode(base64_string).decode('utf-8')
    
    return json_string

@app.route('/')
def home():
    return 'All good working'


if __name__ == '__main__':
    app.run(debug=False)