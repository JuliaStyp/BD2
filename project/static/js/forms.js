function showMessage(message, id) {
    document.getElementById('popup-msg').textContent = message;
    document.getElementById('popup-id').textContent = id;
    popup.style.visibility = "visible"
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        fetch(API, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(json => {
            item_id = "item" in json ? "ID: " + json["item"]["id"] : "";
            showMessage(json["message"], item_id);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

document.getElementById('popup-button').addEventListener("click", function () {
    popup.style.visibility = "hidden";
})

