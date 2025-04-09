document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    const resultsContainer = document.getElementById("results-container");
    const resultsTable = document.getElementById("results-table");
    const resultsTableBody = resultsTable.querySelector("tbody");

    function performSearch(full = false) {
        const query = searchInput.value.trim();
        const url = `/search-users/?q=${encodeURIComponent(query)}&full=${full}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                resultsTableBody.innerHTML = ""; // Réinitialiser les résultats

                if (data.results.length > 0) {
                    resultsTable.classList.remove("hidden");
                    resultsTable.style.display = "table"; // Assurer l'affichage du tableau

                    data.results.forEach(user => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${user.alias || 'Aucun alias'}</td>
                            <td>${user.email}</td>
                            <td>
                                <a href="${user.profile_url}" class="btn btn-primary">Voir le profil</a>
                            </td>
                        `;
                        resultsTableBody.appendChild(row);
                    });

                    // Adapter la largeur du conteneur
                    if (full) {
                        resultsContainer.classList.add("full-screen");
                    } else {
                        resultsContainer.classList.remove("full-screen");
                    }

                } else {
                    resultsTable.classList.add("hidden");
                    resultsTable.style.display = "none";
                }
            })
            .catch(error => console.error("Erreur :", error));
    }

    // Charger les 3 premiers utilisateurs au début
    performSearch(false);

    searchInput.addEventListener("input", () => performSearch());
    searchButton.addEventListener("click", () => performSearch(true));
});
