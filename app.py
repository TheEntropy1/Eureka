from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

TMDB_API_KEY = 'YOUR_TMDB_API_KEY'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    category = request.args.get('category', 'movie')
    if not query:
        return redirect('/')
    tmdb_url = f'https://api.themoviedb.org/3/search/{category}?api_key={TMDB_API_KEY}&query={query}'
    response = requests.get(tmdb_url)
    results = response.json().get('results', [])
    return render_template('search.html', query=query, results=results, category=category)

@app.route('/watch/<int:tmdb_id>')
def watch(tmdb_id):
    category = request.args.get('category', 'movie')
    tmdb_url = f'https://api.themoviedb.org/3/{category}/{tmdb_id}?api_key={TMDB_API_KEY}'
    response = requests.get(tmdb_url)
    details = response.json()

    # Build embed URL (example using vidsrc)
    embed_url = f"https://vidsrc.to/embed/{category}/{tmdb_id}"

    return render_template('watch.html', details=details, embed_url=embed_url)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
