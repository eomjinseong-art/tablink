# api/index.py
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# URL 추출 정규식 패턴
URL_PATTERN = r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[^\s]*)'

@app.route('/api/extract-link', methods=['POST'])
def extract_link():
    try:
        data = request.get_json(silent=True) or {}
        raw_text = data.get('text', '')
        
        urls = re.findall(URL_PATTERN, raw_text)
        
        if not urls:
            return jsonify({'success': False, 'message': '텍스트에서 링크를 찾을 수 없습니다.'}), 404
        
        target_url = urls[0].strip()
        target_url = re.sub(r'[\),\.\?]+$', '', target_url)
        
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'https://' + target_url
            
        return jsonify({
            'success': True,
            'url': target_url
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Vercel이 WSGI 애플리케이션으로 핸들링할 수 있도록 app 변수 노출
