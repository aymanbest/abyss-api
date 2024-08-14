from flask import Flask, request, jsonify
from lib.aadecode import decode
import re
import base64

app = Flask(__name__)

@app.route('/decode', methods=['POST'])
def decode_string():

    if 'abyss' not in request.form:
        return jsonify({'error': 'No data provided'}), 400

    decoded_string = request.form.get('abyss')
    
    try:
        decoded_string = decode(decoded_string)
    except Exception as e:
        return jsonify({'error': f'Decode function error: {str(e)}'}), 500

    match = re.search(r'(?<=JSON\.parse\(atob\(")([^"]+)(?="\)\))', decoded_string)
    
    if not match:
        return jsonify({'error': 'No match found in decoded string'}), 400

    base64_string = match.group(1)
    try:
        json_string = base64.b64decode(base64_string).decode('utf-8')
    except Exception as e:
        return jsonify({'error': f'Base64 decode error on JSON string: {str(e)}'}), 400
    
    return jsonify({'json': json_string})

@app.route('/')
def home():
    return 'All good working'

if __name__ == '__main__':
    app.run(debug=False)
