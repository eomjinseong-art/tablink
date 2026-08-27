# api/index.py
from flask import Flask, request, jsonify
import re
import base64
import json

app = Flask(__name__)

# URL 추출 정규식 패턴
URL_PATTERN = r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[^\s]*)'

@app.route('/api/extract-link', methods=['POST'])
def extract_link():
    try:
        data = request.get_json()
        
        # 1. 단축어에서 텍스트(Live Text 결과) 또는 이미지를 받음
        raw_text = data.get('text', '')
        
        # 2. 정규식으로 URL 패턴 검색
        urls = re.findall(URL_PATTERN, raw_text)
        
        if not urls:
            return jsonify({'success': False, 'message': '링크를 찾을 수 없습니다.'}), 404
        
        target_url = urls[0]
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'https://' + target_url
            
        return jsonify({
            'success': True,
            'url': target_url
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()