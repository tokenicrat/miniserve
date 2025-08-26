import os
import secrets
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from flask import Flask, request, jsonify, abort, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

UPLOAD_FOLDER: str = '/data'
MAX_CONTENT_LENGTH: int = int(os.environ.get('MAX_CONTENT_LENGTH', 100)) * 1024 * 1024
AUTH_TOKEN: str = os.environ.get('AUTH_TOKEN', secrets.token_hex(20))

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

def authenticate() -> bool:
    token: Optional[str] = request.headers.get('Authorization')
    if not token or not AUTH_TOKEN:
        return False
    
    # Allow `Bearer xxxxx` token format
    if token.startswith('Bearer '):
        token = token[7:]
    
    return token == AUTH_TOKEN

def generate_filename(extension: str = '') -> str:
    while True:
        filename: str = secrets.token_hex(10)
        if extension:
            full_filename: str = f"{filename}.{extension}"
        else:
            full_filename = filename
            
        filepath: Path = Path(UPLOAD_FOLDER) / full_filename
        if not filepath.exists():
            return full_filename

@app.route('/upload', methods=['POST'])
def upload_file() -> Tuple[Response, int]:
    if not authenticate():
        abort(401)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file: FileStorage = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Generate random name while preserving extension
    assert file.filename is not None
    original_extension: str = Path(file.filename).suffix.lstrip('.')
    new_filename: str = generate_filename(original_extension)
    filepath: Path = Path(UPLOAD_FOLDER) / new_filename
    
    try:
        file.save(str(filepath))
        response_data: Dict[str, Any] = {
            'filename': new_filename,
            'original_filename': secure_filename(file.filename),
            'size': filepath.stat().st_size
        }
        return jsonify(response_data), 201
    except Exception:
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename: str) -> Tuple[Response, int]:
    if not authenticate():
        abort(401)
    
    sanitized_filename: str = secure_filename(filename)
    filepath: Path = Path(UPLOAD_FOLDER) / sanitized_filename
    
    # Make sure requested file is within uploaded directory
    try:
        filepath.resolve().relative_to(Path(UPLOAD_FOLDER).resolve())
    except ValueError:
        return jsonify({'error': 'Invalid filename'}), 400
    
    if not filepath.exists():
        return jsonify({'error': 'File not found'}), 404
    
    try:
        filepath.unlink()
        response_data: Dict[str, str] = {'message': f'File {sanitized_filename} deleted successfully'}
        return jsonify(response_data), 200
    except Exception:
        return jsonify({'error': 'Delete failed'}), 500

@app.errorhandler(401)
def unauthorized(_) -> Tuple[Response, int]:
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(413)
def file_too_large(_) -> Tuple[Response, int]:
    return jsonify({'error': 'File too large'}), 413

if __name__ == '__main__':
    if not os.environ.get('AUTH_TOKEN'):
        print(f"Use random token: {AUTH_TOKEN}")
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.run(host='0.0.0.0', port=5000, debug=False)
