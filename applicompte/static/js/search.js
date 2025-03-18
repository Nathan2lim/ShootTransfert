document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    const resultsTable = document.getElementById("results-table");
    const resultsTableBody = resultsTable.querySelector("tbody");

    function performSearch(full = false) {
        const query = searchInput.value.trim();
        if (query) {
            const url = `/search-users/?q=${encodeURIComponent(query)}&full=${full}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resultsTableBody.innerHTML = ""; // Réinitialiser les résultats
                    if (data.results.length > 0) {
                        resultsTable.classList.remove("hidden");
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
                    } else {
                        resultsTable.classList.add("hidden"); // Cacher le tableau si aucun résultat
                        resultsTableBody.innerHTML = "<p>Aucun résultat trouvé.</p>";
                    }
                })
                .catch(error => console.error("Erreur :", error));
        } else {
            resultsTable.classList.add("hidden"); // Cacher le tableau si le champ est vide
        }
    }

    searchInput.addEventListener("input", () => performSearch());
    searchButton.addEventListener("click", () => performSearch(true));
});


