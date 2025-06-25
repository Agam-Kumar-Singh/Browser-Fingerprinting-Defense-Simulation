from flask import Flask, request, jsonify, render_template
import hashlib
import json
import random
from fingerprint_defender import FingerprintDefender

app = Flask(__name__)
app.debug = True

fingerprints_db = {}
defender = FingerprintDefender()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect_fingerprint():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    fingerprint_str = json.dumps(data, sort_keys=True)
    fingerprint_hash = hashlib.sha256(fingerprint_str.encode()).hexdigest()
    fingerprints_db[fingerprint_hash] = data
    
    return jsonify({
        'status': 'success',
        'fingerprint_id': fingerprint_hash,
        'stored_data': {k: type(v).__name__ for k, v in data.items()}
    })

@app.route('/randomized-fingerprint')
def randomized_fingerprint():
    sample_fp = next(iter(fingerprints_db.values())) if fingerprints_db else {
        "screen": {"width": 1920, "height": 1080, "colorDepth": 24, "pixelDepth": 24},
        "browser": {"userAgent": "Mozilla/5.0"},
        "webgl": "NVIDIA Corporation",
        "canvas": "real_canvas_data"
    }
    
    randomized_fp = defender.randomize(sample_fp)
    return jsonify({
        'randomized_fingerprint': randomized_fp,
        'analysis': analyze_fingerprint_data(randomized_fp)
    })

@app.route('/analyze/<fingerprint_id>')
def analyze_fingerprint(fingerprint_id):
    if fingerprint_id not in fingerprints_db:
        return jsonify({'error': 'Fingerprint not found'}), 404
    return jsonify(analyze_fingerprint_data(fingerprints_db[fingerprint_id]))

@app.route('/protected-fingerprint')
def protected_fingerprint():
    # Use a fresh base fingerprint to ensure different standardized values
    base_fp = {
        "screen": {"width": 1920, "height": 1080, "colorDepth": 24, "pixelDepth": 24},
        "browser": {"userAgent": "Mozilla/5.0"},
        "webgl": "NVIDIA Corporation",
        "canvas": "real_canvas_data"
    }
    
    protected = defender.defend(base_fp)
    return jsonify({
        'protected_fingerprint': protected,
        'analysis': analyze_fingerprint_data(protected)
    })

@app.route('/fake-fingerprint')
def generate_fake_fingerprint():
    # Generate a fake fingerprint using randomization
    fake_fp = defender.generate_fake_fingerprint()
    return jsonify({
        'fake_fingerprint': fake_fp,
        'analysis': analyze_fingerprint_data(fake_fp)
    })

def analyze_fingerprint_data(fingerprint):
    return {
        'uniqueness_score': calculate_uniqueness(fingerprint),
        'risk_score': calculate_risk(fingerprint),
        'characteristics': {
            'num_attributes': len(fingerprint),
            'has_webgl': 'webgl' in fingerprint and fingerprint['webgl'] != 'blocked',
            'has_canvas': 'canvas' in fingerprint and fingerprint['canvas'] != 'blocked',
            'is_fake': fingerprint.get('is_fake', False),
            'is_randomized': fingerprint.get('is_randomized', False),
            'is_mobile': fingerprint.get('is_mobile', False)
        }
    }

def calculate_uniqueness(fingerprint):
    score = 10
    
    # Base attributes
    if fingerprint.get('is_fake', False):
        score += random.randint(5, 20)  # Lower uniqueness for fake fingerprints
    if fingerprint.get('is_randomized', False):
        score += random.randint(10, 30)  # Randomized fingerprints have variable uniqueness
    
    # Screen attributes
    if 'screen' in fingerprint:
        if fingerprint['screen'].get('width', 0) > 1000:
            score += 10  # Larger screens are more unique
        if fingerprint['screen'].get('colorDepth', 24) != 24:
            score += 5   # Non-standard color depth
        if fingerprint['screen'].get('orientation') == 'portrait-primary':
            score += 10  # Mobile-like orientation
    
    # Browser attributes
    if 'browser' in fingerprint:
        if fingerprint['browser'].get('language') not in ['en-US', 'en-GB']:
            score += 10  # Less common languages
        if len(fingerprint['browser'].get('languages', [])) > 2:
            score += 5   # Multiple languages
    
    # WebGL and Canvas
    if 'webgl' in fingerprint and fingerprint['webgl'] != 'blocked':
        score += 20
    if 'canvas' in fingerprint and fingerprint['canvas'] != 'blocked':
        score += 20
    
    # Timezone
    if 'timezone' in fingerprint:
        if fingerprint['timezone'].get('timezone') not in ['America/New_York', 'Europe/London']:
            score += 10  # Less common timezones
    
    # Random variation
    score += random.randint(-5, 5)
    return min(max(score, 5), 100)

def calculate_risk(fingerprint):
    risk = 10
    
    # Base attributes
    if fingerprint.get('is_fake', False):
        risk += random.randint(5, 15)  # Lower risk for fake fingerprints
    if fingerprint.get('is_randomized', False):
        risk += random.randint(10, 25)  # Randomized fingerprints have variable risk
    
    # Screen attributes
    if 'screen' in fingerprint:
        if fingerprint['screen'].get('width', 0) > 1000:
            risk += 10  # Larger screens are more trackable
        if fingerprint['screen'].get('colorDepth', 24) != 24:
            risk += 5   # Non-standard color depth
        if fingerprint['screen'].get('orientation') == 'portrait-primary':
            risk += 5   # Mobile-like orientation
    
    # Browser attributes
    if 'browser' in fingerprint:
        if fingerprint['browser'].get('language') not in ['en-US', 'en-GB']:
            risk += 10  # Less common languages
        if len(fingerprint['browser'].get('languages', [])) > 2:
            risk += 5   # Multiple languages
    
    # WebGL and Canvas
    if 'webgl' in fingerprint and fingerprint['webgl'] != 'blocked':
        risk += 25
    if 'canvas' in fingerprint and fingerprint['canvas'] != 'blocked':
        risk += 25
    
    # Timezone
    if 'timezone' in fingerprint:
        if fingerprint['timezone'].get('timezone') not in ['America/New_York', 'Europe/London']:
            risk += 10  # Less common timezones
    
    # Random variation
    risk += random.randint(-5, 5)
    return min(max(risk, 5), 100)

if __name__ == '__main__':
    app.run(port=5000)