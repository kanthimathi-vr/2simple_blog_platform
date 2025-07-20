from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

POSTS_FILE = 'posts.json'

def load_posts():
    try:
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

@app.route('/')
def index():
    query = request.args.get('q', '').lower()
    posts = load_posts()
    if query:
        posts = [p for p in posts if query in p['title'].lower() or query in p['content'].lower()]
    return render_template('index.html', posts=posts, query=query)

@app.route('/post/<int:post_id>')
def post(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    return render_template('post.html', post=post)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            'id': len(posts) + 1,
            'title': request.form['title'],
            'content': request.form['content'],
            'date': datetime.now().strftime("%B %d, %Y")
        }
        posts.insert(0, new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
