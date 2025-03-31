from flask import Flask, render_template, request, jsonify, session
import random
import os
from card_utils import get_card_frame

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Pour les sessions Flask

class BatailleGameWeb:
    def __init__(self):
        # Initialize game properties but don't use session yet
        # We'll initialize the actual game state only when handling a request
        self.jeu_A = []
        self.jeu_B = []
        self.score_A = 0
        self.score_B = 0
        self.pile_bataille = []
        self.en_bataille = False
        self.mode_jeu = 'basic'  # Par défaut

    def creation_jeu32(self):
        """Create a 32-card deck"""
        couleurs = ("pique", "coeur", "carreau", "trèfle")
        
        # Le jeu de base a 8 cartes par couleur
        if self.mode_jeu == 'basic':
            valeurs = ("R", "D", "V", 10, 9, 8, 7, 1)
        # Le jeu avancé a 13 cartes par couleur (jeu complet)
        elif self.mode_jeu == 'advanced':
            valeurs = ("R", "D", "V", 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
        # Partie complémentaire avec un jeu personnalisé
        elif self.mode_jeu == 'complement':
            valeurs = ("R", "D", "V", "C", 10, 9, 8, 7, 6, 5)  # Ajout d'un Cavalier
        else:
            valeurs = ("R", "D", "V", 10, 9, 8, 7, 1)
            
        return [(v, c) for v in valeurs for c in couleurs]

    def melange(self, jeu):
        """Shuffle the deck"""
        random.shuffle(jeu)
        return jeu

    def carte_hasard(self, jeu):
        """Draw a random card from the deck"""
        if jeu:
            return jeu.pop(0)  # Take from the top of the deck
        return None

    def force(self, carte):
        """Calculate the strength of a card"""
        # Valeurs et forces différentes selon le mode de jeu
        if self.mode_jeu == 'basic':
            valeurs = (1, "R", "D", "V", 10, 9, 8, 7)
            forces = (8, 7, 6, 5, 4, 3, 2, 1)
        elif self.mode_jeu == 'advanced':
            valeurs = (1, "R", "D", "V", 10, 9, 8, 7, 6, 5, 4, 3, 2)
            forces = (13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
        elif self.mode_jeu == 'complement':
            valeurs = (1, "R", "D", "C", "V", 10, 9, 8, 7, 6, 5)
            forces = (11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
        else:
            valeurs = (1, "R", "D", "V", 10, 9, 8, 7)
            forces = (8, 7, 6, 5, 4, 3, 2, 1)
            
        try:
            indice = valeurs.index(carte[0])
            return forces[indice]
        except (ValueError, IndexError):
            return 0

    def compare(self, carte1, carte2):
        """Compare two cards"""
        if carte1 is None or carte2 is None:
            return None
            
        force1 = self.force(carte1)
        force2 = self.force(carte2)
        
        if force1 > force2:
            return "Joueur A"
        elif force2 > force1:
            return "Joueur B"
        return "Égalité"

    def jouer(self):
        """Play a round"""
        # Get game state from session
        self.jeu_A = session.get('jeu_A', [])
        self.jeu_B = session.get('jeu_B', [])
        self.score_A = session.get('score_A', 0)
        self.score_B = session.get('score_B', 0)
        self.pile_bataille = session.get('pile_bataille', [])
        self.en_bataille = session.get('en_bataille', False)
        self.mode_jeu = session.get('mode_jeu', 'basic')
        
        # Check if game is over
        if not self.jeu_A or not self.jeu_B:
            return self.get_resultat_final()
        
        # Draw cards
        carte_A = self.carte_hasard(self.jeu_A)
        carte_B = self.carte_hasard(self.jeu_B)
        
        # Add cards to the battle pile
        self.pile_bataille.append(carte_A)
        self.pile_bataille.append(carte_B)
        
        # Compare cards
        gagnant = self.compare(carte_A, carte_B)
        
        # Process card display info
        carte_A_info = self.get_card_info(carte_A)
        carte_B_info = self.get_card_info(carte_B)
        
        # Initialize result text
        result_text = ""
        bataille_text = ""
        
        # Handle comparison result
        if gagnant == "Égalité":
            self.en_bataille = True
            result_text = "Égalité! C'est la BATAILLE!"
            bataille_text = f"Cartes en jeu: {len(self.pile_bataille)}"
        else:
            # Attribute cards to winner
            if gagnant == "Joueur A":
                self.jeu_A.extend(self.pile_bataille)
                if self.en_bataille:
                    result_text = "Joueur A remporte la bataille!"
                    self.score_A += len(self.pile_bataille) // 2
                else:
                    result_text = "Joueur A remporte le tour!"
                    self.score_A += 1
            else:  # Joueur B
                self.jeu_B.extend(self.pile_bataille)
                if self.en_bataille:
                    result_text = "Joueur B remporte la bataille!"
                    self.score_B += len(self.pile_bataille) // 2
                else:
                    result_text = "Joueur B remporte le tour!"
                    self.score_B += 1
            
            # Reset battle
            self.pile_bataille = []
            self.en_bataille = False
        
        # Save game state to session
        session['jeu_A'] = self.jeu_A
        session['jeu_B'] = self.jeu_B
        session['score_A'] = self.score_A
        session['score_B'] = self.score_B
        session['pile_bataille'] = self.pile_bataille
        session['en_bataille'] = self.en_bataille
        session['mode_jeu'] = self.mode_jeu
        
        # Prepare response
        return {
            'carte_A': carte_A_info,
            'carte_B': carte_B_info,
            'result': result_text,
            'bataille': bataille_text,
            'score': f"Score : Joueur A {self.score_A} - Joueur B {self.score_B}",
            'cartes_A': len(self.jeu_A),
            'cartes_B': len(self.jeu_B),
            'game_over': not self.jeu_A or not self.jeu_B
        }

    def get_card_info(self, carte):
        """Get display info for a card"""
        if not carte:
            return {'value': '', 'symbol': '', 'color': ''}
            
        value, symbol, color = get_card_frame(carte)
        return {
            'value': value,
            'symbol': symbol,
            'color': color
        }

    def get_resultat_final(self):
        """Generate final result data"""
        message = f"Fin de partie! Score final : Joueur A {self.score_A} - Joueur B {self.score_B}"
        
        if self.score_A > self.score_B:
            message += " - Joueur A remporte la partie!"
        elif self.score_B > self.score_A:
            message += " - Joueur B remporte la partie!"
        else:
            message += " - Match nul!"
            
        return {
            'game_over': True,
            'message': message,
            'score': f"Score : Joueur A {self.score_A} - Joueur B {self.score_B}",
            'cartes_A': len(self.jeu_A),
            'cartes_B': len(self.jeu_B)
        }
        
    def jouer_jusqua_fin(self):
        """Simulate playing until the game is over"""
        # Get game state from session
        self.jeu_A = session.get('jeu_A', [])
        self.jeu_B = session.get('jeu_B', [])
        self.score_A = session.get('score_A', 0)
        self.score_B = session.get('score_B', 0)
        self.pile_bataille = session.get('pile_bataille', [])
        self.en_bataille = session.get('en_bataille', False)
        self.mode_jeu = session.get('mode_jeu', 'basic')
        
        # Limite de tours pour éviter une boucle infinie
        max_tours = 1000
        tours_joues = 0
        
        # Jouons jusqu'à ce qu'un joueur n'ait plus de cartes ou jusqu'à la limite de tours
        while self.jeu_A and self.jeu_B and tours_joues < max_tours:
            # Tirage des cartes
            carte_A = self.carte_hasard(self.jeu_A)
            carte_B = self.carte_hasard(self.jeu_B)
            
            # Ajout des cartes à la pile de bataille
            self.pile_bataille.append(carte_A)
            self.pile_bataille.append(carte_B)
            
            # Comparaison des cartes
            gagnant = self.compare(carte_A, carte_B)
            
            # Traitement du résultat
            if gagnant == "Égalité":
                self.en_bataille = True
            else:
                # Attribution des cartes au gagnant
                if gagnant == "Joueur A":
                    self.jeu_A.extend(self.pile_bataille)
                    if self.en_bataille:
                        self.score_A += len(self.pile_bataille) // 2
                    else:
                        self.score_A += 1
                else:  # Joueur B
                    self.jeu_B.extend(self.pile_bataille)
                    if self.en_bataille:
                        self.score_B += len(self.pile_bataille) // 2
                    else:
                        self.score_B += 1
                
                # Réinitialisation de la bataille
                self.pile_bataille = []
                self.en_bataille = False
            
            tours_joues += 1
        
        # Si on a atteint la limite de tours sans finir, on détermine le gagnant par le nombre de cartes
        if tours_joues >= max_tours and self.jeu_A and self.jeu_B:
            if len(self.jeu_A) > len(self.jeu_B):
                self.jeu_B = []  # Joueur A gagne
            else:
                self.jeu_A = []  # Joueur B gagne
        
        # Sauvegarde de l'état du jeu dans la session
        session['jeu_A'] = self.jeu_A
        session['jeu_B'] = self.jeu_B
        session['score_A'] = self.score_A
        session['score_B'] = self.score_B
        session['pile_bataille'] = self.pile_bataille
        session['en_bataille'] = self.en_bataille
        
        # Retourne le résultat final
        return self.get_resultat_final()

    def initialiser_jeu(self, mode='basic'):
        """Initialize or reset the game"""
        # Set game mode
        self.mode_jeu = mode
        
        # Create and shuffle deck
        jeu = self.melange(self.creation_jeu32())
        
        # Calculate half for card distribution
        milieu = len(jeu) // 2
        
        # Deal cards
        self.jeu_A = jeu[:milieu]
        self.jeu_B = jeu[milieu:]
        self.score_A = 0
        self.score_B = 0
        self.pile_bataille = []
        self.en_bataille = False


# Create game instance
game = BatailleGameWeb()

@app.route('/')
def index():
    # Reset game for new session if needed
    if 'jeu_A' not in session:
        # Initialize game state in session with default mode
        game.initialiser_jeu('basic')
        session['jeu_A'] = game.jeu_A
        session['jeu_B'] = game.jeu_B
        session['score_A'] = game.score_A
        session['score_B'] = game.score_B
        session['pile_bataille'] = game.pile_bataille
        session['en_bataille'] = game.en_bataille
        session['mode_jeu'] = game.mode_jeu
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    return jsonify(game.jouer())

@app.route('/reset', methods=['POST'])
def reset():
    # Get data from request if available
    data = request.json
    mode = data.get('mode', 'basic') if data else 'basic'
    
    # Reset game state with specified mode
    game.initialiser_jeu(mode)
    
    # Update session with new game state
    session['jeu_A'] = game.jeu_A
    session['jeu_B'] = game.jeu_B
    session['score_A'] = game.score_A
    session['score_B'] = game.score_B
    session['pile_bataille'] = game.pile_bataille
    session['en_bataille'] = game.en_bataille
    session['mode_jeu'] = game.mode_jeu
    
    return jsonify({'status': 'success'})

@app.route('/finish', methods=['POST'])
def finish():
    """Simule rapidement la partie jusqu'à la fin"""
    return jsonify(game.jouer_jusqua_fin())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)