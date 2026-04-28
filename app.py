"""
INF232 EC2 - Data Collection and Analysis Application
A Flask-based web application for collecting customer feedback and performing descriptive analysis.
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import sqlite3
import os
import json
from functools import wraps
import statistics

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
DATABASE = os.environ.get('DATABASE_PATH', '/tmp/feedback.db')


# Translations
TRANSLATIONS = {
    'en': {
        'title': 'Customer Feedback Collector',
        'subtitle': 'Share your valuable feedback with us',
        'form_title': 'Submit Your Feedback',
        'product_label': 'Product/Service',
        'rating_label': 'Rating (1-5 stars)',
        'comment_label': 'Your Comments',
        'submit_btn': 'Submit Feedback',
        'success_msg': 'Thank you! Your feedback has been recorded.',
        'error_msg': 'An error occurred. Please try again.',
        'analysis_title': 'Feedback Analysis',
        'total_responses': 'Total Responses',
        'avg_rating': 'Average Rating',
        'highest_rating': 'Highest Rating',
        'lowest_rating': 'Lowest Rating',
        'rating_distribution': 'Rating Distribution',
        'recent_feedback': 'Recent Feedback',
        'no_data': 'No feedback data available yet.',
        'language': 'Language',
        'dark_mode': 'Dark Mode',
        'home': 'Home',
        'analytics': 'Analytics',
        'back': 'Back',
        'date': 'Date',
        'product': 'Product',
        'rating': 'Rating',
        'comment': 'Comment',
    },
    'fr': {
        'title': 'Collecteur de Retours Clients',
        'subtitle': 'Partagez vos précieux retours avec nous',
        'form_title': 'Soumettre vos Retours',
        'product_label': 'Produit/Service',
        'rating_label': 'Évaluation (1-5 étoiles)',
        'comment_label': 'Vos Commentaires',
        'submit_btn': 'Soumettre les Retours',
        'success_msg': 'Merci ! Vos retours ont été enregistrés.',
        'error_msg': 'Une erreur s\'est produite. Veuillez réessayer.',
        'analysis_title': 'Analyse des Retours',
        'total_responses': 'Nombre Total de Réponses',
        'avg_rating': 'Évaluation Moyenne',
        'highest_rating': 'Évaluation la Plus Élevée',
        'lowest_rating': 'Évaluation la Plus Basse',
        'rating_distribution': 'Distribution des Évaluations',
        'recent_feedback': 'Retours Récents',
        'no_data': 'Aucune donnée de retours disponible pour le moment.',
        'language': 'Langue',
        'dark_mode': 'Mode Sombre',
        'home': 'Accueil',
        'analytics': 'Analyses',
        'back': 'Retour',
        'date': 'Date',
        'product': 'Produit',
        'rating': 'Évaluation',
        'comment': 'Commentaire',
    }
}

def get_db():
    """Get database connection with WAL mode for multi-worker safety."""
    db = sqlite3.connect(DATABASE, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA journal_mode=WAL')
    return db

def init_db():
    """Initialize the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()
    db.close()

def get_language():
    """Get the current language from session or default to 'en'."""
    try:
        return session.get('language', 'en')
    except Exception:
        return 'en'
        
def get_translation(key):
    """Get translation for a key."""
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def get_descriptive_stats():
    """Calculate descriptive statistics from feedback data."""
    db = get_db()
    cursor = db.cursor()
    
    # Get all ratings
    cursor.execute('SELECT rating FROM feedback ORDER BY created_at DESC')
    ratings = [row[0] for row in cursor.fetchall()]
    
    db.close()
    
    if not ratings:
        return None
    
    stats = {
        'total_count': len(ratings),
        'average': round(statistics.mean(ratings), 2),
        'median': statistics.median(ratings),
        'mode': statistics.mode(ratings) if len(set(ratings)) < len(ratings) else None,
        'std_dev': round(statistics.stdev(ratings), 2) if len(ratings) > 1 else 0,
        'min': min(ratings),
        'max': max(ratings),
        'distribution': {i: ratings.count(i) for i in range(1, 6)}
    }
    
    return stats

@app.before_request
def before_request():
    """Initialize database and session."""
    init_db()
    if 'language' not in session:
        session['language'] = 'en'

@app.route('/')
def index():
    """Home page with feedback form."""
    translations = TRANSLATIONS[get_language()]
    return render_template('index.html', translations=translations, lang=get_language())

@app.route('/analytics')
def analytics():
    """Analytics page with descriptive analysis."""
    db = get_db()
    cursor = db.cursor()
    
    # Get all feedback
    cursor.execute('SELECT * FROM feedback ORDER BY created_at DESC LIMIT 50')
    feedback_list = [dict(row) for row in cursor.fetchall()]
    
    db.close()
    
    stats = get_descriptive_stats()
    translations = TRANSLATIONS[get_language()]
    
    return render_template('analytics.html', 
                         feedback=feedback_list, 
                         stats=stats,
                         translations=translations,
                         lang=get_language())

@app.route('/api/feedback', methods=['GET', 'POST'])
def feedback():
    """API endpoint to submit (POST) or retrieve (GET) feedback."""
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Validate input
            if not data.get('product') or not data.get('rating'):
                return jsonify({'error': 'Missing required fields'}), 400

            rating = int(data.get('rating'))
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400

            # Insert into database
            db = get_db()
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO feedback (product, rating, comment)
                VALUES (?, ?, ?)
            ''', (data['product'], rating, data.get('comment', '')))
            db.commit()
            db.close()

            return jsonify({'success': True, 'message': get_translation('success_msg')}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # GET — return recent feedback
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM feedback ORDER BY created_at DESC LIMIT 20')
    feedback_list = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(feedback_list), 200

@app.route('/api/stats')
def get_stats():
    """API endpoint to get statistics."""
    stats = get_descriptive_stats()
    if stats:
        return jsonify(stats), 200
    return jsonify({'error': 'No data available'}), 404

@app.route('/api/language/<lang>')
def set_language(lang):
    """Set the application language."""
    if lang in TRANSLATIONS:
        session['language'] = lang
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Language not supported'}), 400

@app.route('/api/export')
def export_data():
    """Export feedback data as JSON."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM feedback ORDER BY created_at DESC')
    feedback_list = [dict(row) for row in cursor.fetchall()]
    db.close()
    
    stats = get_descriptive_stats()
    
    export_data = {
        'exported_at': datetime.now().isoformat(),
        'statistics': stats,
        'feedback': feedback_list
    }
    
    return jsonify(export_data), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html', translations=TRANSLATIONS[get_language()]), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return render_template('500.html', translations=TRANSLATIONS[get_language()]), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
