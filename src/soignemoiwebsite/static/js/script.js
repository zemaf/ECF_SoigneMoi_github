
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('id_specialite').addEventListener('change', function() {
        const specialiteId = this.value;
        const url = '{% url "ajax_load_medecins" %}?specialite=' + specialiteId;
        const csrftoken = getCookie('csrftoken');

        fetch(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfTokenValue,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json()) // Première instruction then
        .then(data => { // Seconde instruction then
            const medecinSelect = document.getElementById('id_medecin');
            medecinSelect.innerHTML = '<option value="">---------</option>';
            data.forEach(medecin => {
                medecinSelect.innerHTML += `<option value="${medecin.id}">${medecin.nom}</option>`;
            });
        });
    });
});