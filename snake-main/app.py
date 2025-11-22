# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Supported algorithms with their display names
SUPPORTED_ALGORITHMS = {
    'hamilton': 'Hamilton Algorithm',
    'greedy': 'Greedy Algorithm'
}

# Supported pathfinding algorithms for short/long algr
PATHFINDING_ALGORITHMS = ['astar', 'dfs', 'bfs', 'dijkstra']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-snake', methods=['POST'])
def run_snake():
    try:
        data = request.get_json()
        algorithm = data.get('algorithm', 'greedy')
        short_algr = data.get('shortAlgr', '')
        long_algr = data.get('longAlgr', '')
        
        # Validate main algorithm parameter
        if algorithm not in SUPPORTED_ALGORITHMS:
            return jsonify({
                'success': False, 
                'error': f'Unsupported algorithm type. Supported: {", ".join(SUPPORTED_ALGORITHMS.keys())}'
            })
        
        # Build command
        cmd = [sys.executable, 'run.py', '-s', algorithm]
        
        # Add short algorithm if provided and valid
        if short_algr and short_algr in PATHFINDING_ALGORITHMS:
            cmd.extend(['--shortalgr', short_algr])
        
        # Add long algorithm if provided and valid  
        if long_algr and long_algr in PATHFINDING_ALGORITHMS:
            cmd.extend(['--longalgr', long_algr])
        
        # Execute command and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Check if execution was successful
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'output': result.stdout,
                'algorithm': algorithm,
                'algorithm_name': SUPPORTED_ALGORITHMS[algorithm],
                'short_algr': short_algr,
                'long_algr': long_algr
            })
        else:
            return jsonify({
                'success': False,
                'error': f"Execution error: {result.stderr}"
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        })

@app.route('/run-stats', methods=['POST'])
def run_stats():
    try:
        data = request.get_json()
        episodes = data.get('episodes', 5)
        
        # Validate episodes parameter
        try:
            episodes = int(episodes)
            if episodes <= 0 or episodes > 100:
                return jsonify({
                    'success': False,
                    'error': 'Episodes must be between 1 and 100'
                })
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Episodes must be a valid number'
            })
        
        # ?建??文件?捕??出
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
        
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['TF_ENABLE_ONEDNN_OPTS'] = '0'
        
        # 重定向?出到文件
        cmd = f'"{sys.executable}" -u run.py --stats-cli -all -e {episodes} > "{temp_file}" 2>&1'
        
        print(f"Executing command with output redirection: {cmd}")
        
        result = subprocess.run(
            cmd,
            shell=True,
            env=env,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=600
        )
        
        # ?取?出文件
        with open(temp_file, 'r', encoding='utf-8') as f:
            output_text = f.read()
        
        # ?除??文件
        os.unlink(temp_file)
        
        print(f"Output from file length: {len(output_text)}")
        if output_text:
            print(f"First 500 chars from file: {output_text[:500]}")
        
        if result.returncode == 0:
            cleaned_output = clean_output(output_text)
            
            if not cleaned_output.strip():
                cleaned_output = f"Command completed but no output captured. (episodes: {episodes})"
                
            return jsonify({
                'success': True,
                'output': cleaned_output,
                'command': 'stats',
                'episodes': episodes
            })
        else:
            cleaned_error = clean_output(output_text)
            return jsonify({
                'success': False,
                'error': f"Execution failed: {cleaned_error}"
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        })
        
def clean_output(text):
    """Clean up output by replacing problematic Unicode characters"""
    if not text:
        return text
    
    # Replace Unicode checkmarks and cross marks with ASCII equivalents
    replacements = {
        '\u2713': '[OK]',      # Unicode checkmark
        '\u2714': '[OK]',      # Heavy checkmark  
        '\u2717': '[ERROR]',   # Unicode cross mark
        '\u2718': '[ERROR]',   # Heavy cross mark
        '\u2192': '->',        # Right arrow
        '\u2014': '-',         # Em dash
        '\u2013': '-'          # En dash
    }
    
    cleaned = text
    for unicode_char, ascii_replacement in replacements.items():
        cleaned = cleaned.replace(unicode_char, ascii_replacement)
    
    return cleaned

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')