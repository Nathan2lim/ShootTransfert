// Sélectionne tous les éléments de message
const messages = document.querySelectorAll('.message');

messages.forEach((message) => {
    // Ajoute un gestionnaire d'événement pour cacher le message au clic
    message.addEventListener('click', () => {
        message.style.transition = 'opacity 0.5s ease';
        message.style.opacity = '0'; // Ajoute une transition pour un effet fluide
        setTimeout(() => message.remove(), 500); // Supprime l'élément après la transition
    });

    // Cache automatiquement le message après 15 secondes
    setTimeout(() => {
        message.style.transition = 'opacity 0.5s ease';
        message.style.opacity = '0'; // Transition fluide
        setTimeout(() => message.remove(), 500); // Supprime l'élément après la transition
    }, 15000);
});