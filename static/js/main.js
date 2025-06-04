document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.toggle('hidden');
            mobileMenuButton.setAttribute('aria-expanded', !isHidden);
        });
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // Chatbot toggle
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');
    const chatButtons = document.querySelectorAll('.chat-btn');

    // Fonction pour fermer la fenêtre du chat
    const closeChatWindow = () => {
        chatWindow.classList.add('hidden');
        chatWindow.classList.add('translate-y-full');
    };

    // Fonction pour ouvrir la fenêtre du chat
    const openChatWindow = () => {
        chatWindow.classList.remove('hidden');
        chatWindow.classList.remove('translate-y-full');
        // Afficher le message de bienvenue si c'est la première fois
        if (chatMessages.children.length === 0) {
            addMessage('Chatbot', 'Bonjour ! Je suis le chatbot de BIRA Entreprise. Je peux vous renseigner sur nos produits, services et plus encore. Posez-moi une question ou utilisez les boutons ci-dessous.');
        }
        // Focus sur l'input après l'animation
        setTimeout(() => {
            chatInput.focus();
        }, 300);
    };

    if (chatToggle && chatWindow) {
        // Ouvrir/fermer la fenêtre avec animation
        chatToggle.addEventListener('click', () => {
            if (chatWindow.classList.contains('hidden')) {
                openChatWindow();
            } else {
                closeChatWindow();
            }
        });

        // Fermer avec le bouton de fermeture
        if (chatClose) {
            chatClose.addEventListener('click', closeChatWindow);
        }

        // Ajouter un message à la fenêtre avec animation
        const addMessage = (sender, message, link = '') => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex ${sender === 'Vous' ? 'justify-end' : 'justify-start'}`;
            
            const messageContent = document.createElement('div');
            messageContent.className = `max-w-[80%] p-3 rounded-lg ${
                sender === 'Vous' 
                    ? 'bg-gradient-to-r from-primary to-secondary text-white rounded-br-none' 
                    : 'bg-gray-100 text-gray-800 rounded-bl-none'
            }`;
            
            const senderSpan = document.createElement('span');
            senderSpan.className = 'block text-xs opacity-75 mb-1';
            senderSpan.textContent = sender;
            
            const messageText = document.createElement('div');
            messageText.innerHTML = message;
            
            messageContent.appendChild(senderSpan);
            messageContent.appendChild(messageText);
            
            if (link) {
                const linkElement = document.createElement('a');
                linkElement.href = link;
                linkElement.className = 'block mt-2 text-sm underline';
                linkElement.textContent = 'En savoir plus';
                messageContent.appendChild(linkElement);
            }
            
            messageDiv.appendChild(messageContent);
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        };

        // Envoyer un message
        const sendMessage = (question) => {
            if (!question.trim()) return;
            
            addMessage('Vous', question);
            chatInput.value = '';
            
            // Préparation des données
            const data = {
                question: question
            };
            
            // Configuration de la requête
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            };
            
            // Envoi de la requête
            axios.post('/chatbot/', JSON.stringify(data), config)
                .then(response => {
                    if (response.data && response.data.response) {
                        addMessage('Chatbot', response.data.response, response.data.link);
                    } else {
                        addMessage('Chatbot', 'Désolé, je n\'ai pas pu traiter votre question.');
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    addMessage('Chatbot', 'Désolé, une erreur est survenue. Veuillez réessayer.');
                });
        };

        // Envoyer avec le bouton d'envoi
        chatSend.addEventListener('click', () => {
            sendMessage(chatInput.value);
        });

        // Envoyer avec la touche Entrée
        chatInput.addEventListener('keypress', e => {
            if (e.key === 'Enter') {
                sendMessage(chatInput.value);
            }
        });

        // Boutons de questions rapides
        chatButtons.forEach(button => {
            button.addEventListener('click', () => {
                const question = button.getAttribute('data-question');
                sendMessage(question);
            });
        });
    }

    // Formulaires (simulation)
    const contactForm = document.querySelector('form[action="#contact"]');
    if (contactForm) {
        contactForm.addEventListener('submit', e => {
            e.preventDefault();
            alert('Message envoyé ! Merci de nous avoir contactés.');
        });
    }

    const newsletterForm = document.querySelector('form[action="#newsletter"]');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', e => {
            e.preventDefault();
            alert('Inscription réussie ! Vous recevrez nos nouveautés.');
        });
    }
});