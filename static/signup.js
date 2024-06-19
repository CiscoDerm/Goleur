document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password === confirmPassword) {
        // En pratique, envoyez les données à votre serveur ici
        alert('Inscription réussie !');
        // Redirection vers la page de connexion ou de tableau de bord
        // window.location.href = 'login.html';
    } else {
        alert('Les mots de passe ne correspondent pas.');
    }
});
