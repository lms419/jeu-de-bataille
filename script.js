document.addEventListener('DOMContentLoaded', function() {
    // Variables du jeu
    let gameMode = 'basic'; // 'basic' ou 'advanced'
    let playComplement = false;
    let autoPlayInterval = null;
    let animationSpeed = 800; // ms
    
    // Éléments du menu de démarrage
    const startMenu = document.getElementById('start-menu');
    const basicModeBtn = document.getElementById('basic-mode-btn');
    const advancedModeBtn = document.getElementById('advanced-mode-btn');
    const complementToggle = document.getElementById('complement-toggle');
    const complementStatus = document.getElementById('complement-status');
    const gameContainer = document.getElementById('game-container');
    
    // Éléments du jeu
    const playBtn = document.getElementById('play-btn');
    const resetBtn = document.getElementById('reset-btn');
    const autoPlayBtn = document.getElementById('auto-play-btn');
    const stopAutoBtn = document.getElementById('stop-auto-btn');
    const finishBtn = document.getElementById('finish-btn');
    const newGameBtn = document.getElementById('new-game-btn');
    const nextGameBtn = document.getElementById('next-game-btn');
    const speedSlider = document.getElementById('speed-slider');
    const speedValue = document.getElementById('speed-value');
    
    const cardAValue = document.getElementById('card-a-value');
    const cardBValue = document.getElementById('card-b-value');
    const cardA = document.getElementById('card-a');
    const cardB = document.getElementById('card-b');
    const result = document.getElementById('result');
    const bataille = document.getElementById('bataille');
    const score = document.getElementById('score');
    const cardsA = document.getElementById('cards-a');
    const cardsB = document.getElementById('cards-b');
    const gameOverModal = document.getElementById('game-over-modal');
    const gameOverMessage = document.getElementById('game-over-message');
    
    // Initialisations du jeu
    initEventListeners();
    
    // Initialiser les écouteurs d'événements
    function initEventListeners() {
        // Écouteurs pour le menu de démarrage
        if (basicModeBtn) {
            basicModeBtn.onclick = function() {
                gameMode = 'basic';
                startGame();
            };
        }
        
        if (advancedModeBtn) {
            advancedModeBtn.onclick = function() {
                gameMode = 'advanced';
                startGame();
            };
        }
        
        if (complementToggle) {
            complementToggle.onchange = function() {
                playComplement = this.checked;
                complementStatus.textContent = playComplement ? 'Oui' : 'Non';
            };
        }
        
        // Écouteurs pour le jeu
        if (playBtn) {
            playBtn.onclick = playRound;
        }
        
        if (resetBtn) {
            resetBtn.onclick = resetGame;
        }
        
        if (autoPlayBtn) {
            autoPlayBtn.onclick = startAutoPlay;
        }
        
        if (stopAutoBtn) {
            stopAutoBtn.onclick = stopAutoPlay;
        }
        
        if (finishBtn) {
            finishBtn.onclick = finishGame;
        }
        
        if (newGameBtn) {
            newGameBtn.onclick = function() {
                resetGame();
                gameOverModal.style.display = 'none';
            };
        }
        
        if (nextGameBtn) {
            nextGameBtn.onclick = function() {
                startSecondGame();
                gameOverModal.style.display = 'none';
            };
        }
        
        if (speedSlider) {
            speedSlider.oninput = function() {
                animationSpeed = this.value;
                speedValue.textContent = (this.value / 1000).toFixed(1) + 's';
                if (autoPlayInterval) {
                    stopAutoPlay();
                    startAutoPlay();
                }
            };
        }
    }
    
    // Démarrer le jeu après sélection du mode
    function startGame() {
        startMenu.style.display = 'none';
        gameContainer.style.display = 'block';
        
        // Initialiser le jeu avec le mode sélectionné
        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mode: gameMode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Reset UI for new game
                resetUI();
                
                // Mettre à jour le titre du jeu selon le mode
                document.querySelector('h1').textContent = 
                    gameMode === 'basic' ? 'Jeu de la Bataille - Version Standard' : 'Jeu de la Bataille - Version Avancée';
            }
        })
        .catch(error => {
            console.error('Erreur lors de l\'initialisation du jeu:', error);
        });
    }
    
    // Démarrer une deuxième partie
    function startSecondGame() {
        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mode: 'complement' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                resetUI();
                document.querySelector('h1').textContent = 'Jeu de la Bataille - Partie Complémentaire';
            }
        })
        .catch(error => {
            console.error('Erreur lors de l\'initialisation de la partie complémentaire:', error);
        });
    }
    
    // Jouer un tour
    function playRound() {
        // Ajouter une animation aux cartes
        cardA.classList.add('animated');
        cardB.classList.add('animated');
        
        // Simuler un délai pour l'animation
        setTimeout(() => {
            fetch('/play', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                updateGameDisplay(data);
                
                if (data.game_over) {
                    showGameOverModal(data.message);
                    stopAutoPlay();
                }
                
                // Retirer l'animation après un court délai
                setTimeout(() => {
                    cardA.classList.remove('animated');
                    cardB.classList.remove('animated');
                }, 300);
            })
            .catch(error => {
                console.error('Erreur pendant le tour:', error);
                stopAutoPlay();
            });
        }, 100);
    }
    
    // Réinitialiser le jeu
    function resetGame() {
        stopAutoPlay();
        
        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mode: gameMode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                resetUI();
            }
        })
        .catch(error => {
            console.error('Erreur lors de la réinitialisation du jeu:', error);
        });
    }
    
    // Réinitialiser l'interface utilisateur
    function resetUI() {
        cardAValue.innerHTML = '';
        cardBValue.innerHTML = '';
        result.textContent = 'Cliquez sur "Jouer un tour" pour commencer';
        bataille.textContent = '';
        score.textContent = 'Score : Joueur A 0 - Joueur B 0';
        cardsA.textContent = 'Cartes: 16';
        cardsB.textContent = 'Cartes: 16';
        
        gameOverModal.style.display = 'none';
    }
    
    // Démarrer le mode automatique
    function startAutoPlay() {
        if (autoPlayInterval) return;
        
        autoPlayBtn.style.display = 'none';
        stopAutoBtn.style.display = 'inline-block';
        
        autoPlayInterval = setInterval(playRound, animationSpeed);
    }
    
    // Arrêter le mode automatique
    function stopAutoPlay() {
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
            autoPlayInterval = null;
        }
        
        autoPlayBtn.style.display = 'inline-block';
        stopAutoBtn.style.display = 'none';
    }
    
    // Simuler jusqu'à la fin de la partie
    function finishGame() {
        // Désactiver le bouton pour éviter les clics multiples
        finishBtn.disabled = true;
        result.textContent = "Simulation en cours...";
        
        // Arrêter l'animation automatique si elle est en cours
        stopAutoPlay();
        
        // Demander au serveur de simuler la partie jusqu'à la fin
        fetch('/finish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            // Mettre à jour le score et l'état du jeu
            score.textContent = data.score;
            cardsA.textContent = `Cartes: ${data.cartes_A}`;
            cardsB.textContent = `Cartes: ${data.cartes_B}`;
            
            // Effacer les cartes en cours
            cardAValue.innerHTML = '';
            cardBValue.innerHTML = '';
            
            // Afficher le résultat final
            result.textContent = "Simulation terminée!";
            showGameOverModal(data.message);
            
            // Réactiver le bouton
            finishBtn.disabled = false;
        })
        .catch(error => {
            console.error('Erreur lors de la simulation:', error);
            result.textContent = "Une erreur est survenue pendant la simulation.";
            finishBtn.disabled = false;
        });
    }
    
    // Mettre à jour l'affichage du jeu
    function updateGameDisplay(data) {
        // Mettre à jour l'affichage des cartes
        if (data.carte_A) {
            cardAValue.innerHTML = `${data.carte_A.value}<br>${data.carte_A.symbol}`;
            cardAValue.className = data.carte_A.color;
        }
        
        if (data.carte_B) {
            cardBValue.innerHTML = `${data.carte_B.value}<br>${data.carte_B.symbol}`;
            cardBValue.className = data.carte_B.color;
        }
        
        // Mettre à jour les textes
        if (data.result) {
            result.textContent = data.result;
        }
        
        if (data.bataille) {
            bataille.textContent = data.bataille;
        } else {
            bataille.textContent = '';
        }
        
        score.textContent = data.score;
        cardsA.textContent = `Cartes: ${data.cartes_A}`;
        cardsB.textContent = `Cartes: ${data.cartes_B}`;
    }
    
    // Afficher la modal de fin de jeu
    function showGameOverModal(message) {
        gameOverMessage.textContent = message;
        
        // Afficher le bouton de partie suivante si l'option est activée
        if (playComplement) {
            nextGameBtn.style.display = 'inline-block';
        } else {
            nextGameBtn.style.display = 'none';
        }
        
        gameOverModal.style.display = 'flex';
    }
});