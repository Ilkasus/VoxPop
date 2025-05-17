from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# In-memory comment store
comments = []

@app.route('/')
def index():
    # Show newest comments first
    page = int(request.args.get('page', 1))
    per_page = 5
    total = len(comments)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_comments = comments[::-1][start:end]  # Reverse chronological
    total_pages = (total + per_page - 1) // per_page
    return render_template('index.html', comments=paginated_comments, page=page, total_pages=total_pages)

@app.route('/comment', methods=['POST'])
def post_comment():
    data = request.get_json()
    text = data.get('text', '').strip()
    category = data.get('category', '').lower()

    if not text or category not in ['positive', 'negative']:
        return jsonify({'error': 'Invalid input'}), 400

    comments.append({
        'text': text,
        'category': category,
        'timestamp': datetime.utcnow().isoformat()
    })
    return jsonify({'message': 'Comment added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
