import tkinter as tk
from tkinter import messagebox, font
from random import shuffle
from card_utils import get_card_frame

class BatailleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de la Bataille")
        self.root.geometry("500x600")
        self.root.configure(bg="#1e3d59")
        
        # Initialize game state
        self.jeu_A = []
        self.jeu_B = []
        self.score_A = 0
        self.score_B = 0
        self.pile_bataille = []
        self.en_bataille = False
        
        # Configure fonts
        self.title_font = font.Font(family="Arial", size=24, weight="bold")
        self.card_font = font.Font(family="Arial", size=36, weight="bold")
        self.text_font = font.Font(family="Arial", size=14)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")
        
        # Create UI elements
        self.create_widgets()
        
        # Initialize game
        self.initialiser_jeu()

    def create_widgets(self):
        """Create all UI elements"""
        # Title
        self.label_titre = tk.Label(
            self.root, 
            text="Jeu de la Bataille", 
            font=self.title_font,
            fg="#ffffff",
            bg="#1e3d59",
            pady=15
        )
        self.label_titre.pack()

        # Game status frame
        self.status_frame = tk.Frame(self.root, bg="#1e3d59")
        self.status_frame.pack(pady=10)
        
        # Cards remaining indicators
        self.cards_frame = tk.Frame(self.status_frame, bg="#1e3d59")
        self.cards_frame.pack()
        
        self.label_cards_A = tk.Label(
            self.cards_frame, 
            text="Cartes: 16", 
            font=self.text_font,
            fg="#ffffff",
            bg="#1e3d59",
            width=10
        )
        self.label_cards_A.grid(row=0, column=0, padx=20)
        
        self.label_cards_B = tk.Label(
            self.cards_frame, 
            text="Cartes: 16", 
            font=self.text_font,
            fg="#ffffff",
            bg="#1e3d59",
            width=10
        )
        self.label_cards_B.grid(row=0, column=1, padx=20)
        
        # Cards display frame
        self.card_display_frame = tk.Frame(self.root, bg="#1e3d59")
        self.card_display_frame.pack(pady=20)
        
        # Player labels
        self.label_player_A = tk.Label(
            self.card_display_frame, 
            text="Joueur A", 
            font=self.text_font,
            fg="#ffffff",
            bg="#1e3d59"
        )
        self.label_player_A.grid(row=0, column=0, padx=30)
        
        self.label_player_B = tk.Label(
            self.card_display_frame, 
            text="Joueur B", 
            font=self.text_font,
            fg="#ffffff",
            bg="#1e3d59"
        )
        self.label_player_B.grid(row=0, column=1, padx=30)
        
        # Card placeholders
        self.card_A_frame = tk.Frame(
            self.card_display_frame, 
            width=120, 
            height=180, 
            bg="#ffffff",
            highlightbackground="#000000",
            highlightthickness=2
        )
        self.card_A_frame.grid(row=1, column=0, padx=30, pady=10)
        self.card_A_frame.grid_propagate(False)
        
        self.label_card_A_value = tk.Label(
            self.card_A_frame,
            text="",
            font=self.card_font,
            bg="#ffffff"
        )
        self.label_card_A_value.place(relx=0.5, rely=0.5, anchor="center")
        
        self.card_B_frame = tk.Frame(
            self.card_display_frame, 
            width=120, 
            height=180, 
            bg="#ffffff",
            highlightbackground="#000000",
            highlightthickness=2
        )
        self.card_B_frame.grid(row=1, column=1, padx=30, pady=10)
        self.card_B_frame.grid_propagate(False)
        
        self.label_card_B_value = tk.Label(
            self.card_B_frame,
            text="",
            font=self.card_font,
            bg="#ffffff"
        )
        self.label_card_B_value.place(relx=0.5, rely=0.5, anchor="center")
        
        # Result label
        self.label_result = tk.Label(
            self.root, 
            text="", 
            font=self.text_font,
            fg="#ffffff",
            bg="#1e3d59",
            height=2
        )
        self.label_result.pack()
        
        # Score display
        self.label_score = tk.Label(
            self.root, 
            text="Score : Joueur A 0 - Joueur B 0", 
            font=self.text_font,
            fg="#ffffff",
            bg="#1e3d59",
            pady=10
        )
        self.label_score.pack()
        
        # Battle indicator
        self.label_bataille = tk.Label(
            self.root, 
            text="", 
            font=self.text_font,
            fg="#ffc13b",
            bg="#1e3d59"
        )
        self.label_bataille.pack()
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.root, bg="#1e3d59")
        self.buttons_frame.pack(pady=20)
        
        # Play button
        self.btn_jouer = tk.Button(
            self.buttons_frame, 
            text="Jouer un tour", 
            command=self.jouer,
            font=self.button_font,
            bg="#ffc13b",
            fg="#000000",
            width=15,
            height=2,
            borderwidth=0
        )
        self.btn_jouer.grid(row=0, column=0, padx=10)
        
        # Reset button
        self.btn_reinitialiser = tk.Button(
            self.buttons_frame, 
            text="Recommencer", 
            command=self.initialiser_jeu,
            font=self.button_font,
            bg="#f5f5f5",
            fg="#000000",
            width=15,
            height=2,
            borderwidth=0
        )
        self.btn_reinitialiser.grid(row=0, column=1, padx=10)

    def creation_jeu32(self):
        """Create a 32-card deck"""
        couleurs = ("pique", "coeur", "carreau", "trèfle")
        valeurs = ("R", "D", "V", 10, 9, 8, 7, 1)
        return [(v, c) for v in valeurs for c in couleurs]

    def melange(self, jeu):
        """Shuffle the deck"""
        shuffle(jeu)
        return jeu

    def carte_hasard(self, jeu):
        """Draw a random card from the deck"""
        if jeu:
            return jeu.pop(0)  # Take from the top of the deck
        return None

    def force(self, carte):
        """Calculate the strength of a card"""
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
        if not self.jeu_A or not self.jeu_B:
            self.afficher_resultat_final()
            return
        
        # Draw cards
        carte_A = self.carte_hasard(self.jeu_A)
        carte_B = self.carte_hasard(self.jeu_B)
        
        # Add cards to the battle pile if we're in a battle
        self.pile_bataille.append(carte_A)
        self.pile_bataille.append(carte_B)
        
        # Compare cards
        gagnant = self.compare(carte_A, carte_B)
        
        # Update display
        self.afficher_cartes(carte_A, carte_B)
        self.mettre_a_jour_cartes_restantes()
        
        # Handle comparison result
        if gagnant == "Égalité":
            self.en_bataille = True
            self.label_result.config(text="Égalité! C'est la BATAILLE!")
            self.label_bataille.config(text=f"Cartes en jeu: {len(self.pile_bataille)}")
        else:
            # Attribute cards to winner
            if gagnant == "Joueur A":
                self.jeu_A.extend(self.pile_bataille)
                if self.en_bataille:
                    self.label_result.config(text="Joueur A remporte la bataille!")
                    self.score_A += len(self.pile_bataille) // 2
                else:
                    self.label_result.config(text="Joueur A remporte le tour!")
                    self.score_A += 1
            else:  # Joueur B
                self.jeu_B.extend(self.pile_bataille)
                if self.en_bataille:
                    self.label_result.config(text="Joueur B remporte la bataille!")
                    self.score_B += len(self.pile_bataille) // 2
                else:
                    self.label_result.config(text="Joueur B remporte le tour!")
                    self.score_B += 1
            
            # Reset battle
            self.pile_bataille = []
            self.en_bataille = False
            self.label_bataille.config(text="")
        
        # Update score
        self.label_score.config(text=f"Score : Joueur A {self.score_A} - Joueur B {self.score_B}")
        
        # Check if game is over
        if not self.jeu_A or not self.jeu_B:
            self.afficher_resultat_final()

    def afficher_cartes(self, carte_A, carte_B):
        """Display the drawn cards"""
        if carte_A:
            value_A, symbol_A, color_A = get_card_frame(carte_A)
            self.label_card_A_value.config(
                text=f"{value_A}\n{symbol_A}",
                fg=color_A
            )
        
        if carte_B:
            value_B, symbol_B, color_B = get_card_frame(carte_B)
            self.label_card_B_value.config(
                text=f"{value_B}\n{symbol_B}",
                fg=color_B
            )

    def mettre_a_jour_cartes_restantes(self):
        """Update the card count display"""
        self.label_cards_A.config(text=f"Cartes: {len(self.jeu_A)}")
        self.label_cards_B.config(text=f"Cartes: {len(self.jeu_B)}")

    def afficher_resultat_final(self):
        """Display the final result"""
        message = f"Fin de partie!\nScore final : Joueur A {self.score_A} - Joueur B {self.score_B}\n\n"
        
        if self.score_A > self.score_B:
            message += "Joueur A remporte la partie!"
        elif self.score_B > self.score_A:
            message += "Joueur B remporte la partie!"
        else:
            message += "Match nul!"
        
        messagebox.showinfo("Fin de partie", message)
        
        # Disable play button
        self.btn_jouer.config(state=tk.DISABLED)

    def initialiser_jeu(self):
        """Initialize or reset the game"""
        # Reset game state
        jeu = self.melange(self.creation_jeu32())
        self.jeu_A = jeu[:16]
        self.jeu_B = jeu[16:]
        self.score_A = 0
        self.score_B = 0
        self.pile_bataille = []
        self.en_bataille = False
        
        # Reset display
        self.label_card_A_value.config(text="")
        self.label_card_B_value.config(text="")
        self.label_result.config(text="Cliquez sur 'Jouer un tour' pour commencer")
        self.label_score.config(text="Score : Joueur A 0 - Joueur B 0")
        self.label_bataille.config(text="")
        self.mettre_a_jour_cartes_restantes()
        
        # Enable play button
        self.btn_jouer.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = BatailleGame(root)
    root.mainloop()
