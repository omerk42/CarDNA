from flask import Flask, render_template

app = Flask(__name__)
all_posts = [
  {
    'title': 'Post 1',
    'content': "post 1 content",
    'author': "Mike"
  },
  {
    'title': 'Post 2',
    'content': "post 2 content"
  }
]

@app.route('/')
def index(methods=['GET']):
  return render_template('index.html')

@app.route('/posts')
def posts():
  return render_template('posts.html', posts=all_posts)

if __name__ == "__main__":
  app.run(debug=True)

