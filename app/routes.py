from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import db, Deck, Card, StudyHistory
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    decks = Deck.query.all()
    return render_template('index.html', decks=decks)

@main_bp.route('/create_deck', methods=['GET', 'POST'])
def create_deck():
    if request.method == 'POST':
        name = request.form['name']
        new_deck = Deck(name=name)
        db.session.add(new_deck)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_deck.html')

@main_bp.route('/create_card/<int:deck_id>', methods=['GET', 'POST'])
def create_card(deck_id):
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        hint = request.form['hint']
        new_card = Card(question=question, answer=answer, hint=hint, deck_id=deck_id)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_card.html', deck_id=deck_id)

@main_bp.route('/study/<int:deck_id>', methods=['GET', 'POST'])
def study(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if request.method == 'POST':
        card_id = request.form['card_id']
        correct = request.form['correct'] == 'true'
        history = StudyHistory(card_id=card_id, correct=correct)
        db.session.add(history)
        db.session.commit()
        return redirect(url_for('main.study', deck_id=deck_id))
    cards = Card.query.filter_by(deck_id=deck_id).all()
    return render_template('study.html', deck=deck, cards=cards)
