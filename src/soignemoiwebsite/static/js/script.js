document.getElementById('id_specialite').addEventListener('change', function() {
        const specialiteId = this.value;
        let csrfTokenValue = document.querySelector("[name=csrfmiddlewaretoken]").value;
        const url = '{% url "soignemoiwebsite:ajax_load_medecins" %}';


        fetch(url, {
            method: 'POST',
	        headers: {
                'content-type': 'application/json',
		        'X-CSRFToken': csrfTokenValue,
	        },
	        body: JSON.stringify({specialite: specialiteId}) // il faut stringifier les données pour les exploiter
        })
        .then(response => response.json()) // Première instruction then
        .then(data => { // Seconde instruction then
            const medecinSelect = document.getElementById('id_medecin');
            medecinSelect.innerHTML = '<option value="">----------</option>'; // affiche les tirets en attendant la sélection
            // On boucle sur le queryset medecins de la spécialité pour les afficher
	        data.forEach(medecin => {
                medecinSelect.innerHTML += `<option value="${medecin.id}">${medecin.nom}</option>`;
            });
        });
    });
