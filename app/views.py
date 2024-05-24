from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from .models import Deck, Card

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    decks = Deck.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", decks=decks)

@views.route('/deck/<int:deck_id>')
@login_required
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        abort(403)
    cards = Card.query.filter_by(deck_id=deck_id).all()
    return render_template("deck.html", deck=deck, cards=cards)

@views.route('/deck/<int:deck_id>/study')
@login_required
def study_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        abort(403)
    cards = Card.query.filter_by(deck_id=deck_id).all()
    return render_template("study.html", deck=deck, cards=cards)
