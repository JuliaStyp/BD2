const list_container = document.getElementById('list-container');
const popup = document.getElementById('popup');

function fetchElements() {
    fetch(API)
        .then(response => response.json())
        .then(json => {
            json.forEach(item => {
                var ul = document.createElement('ul');
                ul.className = "values-list " + CLASS;
                list_container.appendChild(ul);
                FIELDS.forEach(key => {
                    addSpan(ul, item, key);
                })
                addDeleteButton(ul, item['id']);
            });
        })
        .catch(error => console.error(error));
}

function addSpan(ul, item, key) {
    var span = document.createElement('span');
    if (NUMERIC_FIELDS.has(key)) {
        span.className = "numeric";
    }
    span.textContent = item[key];
    ul.appendChild(span);
}

function addDeleteButton(ul, itemID) {
    var a = document.createElement('a');
    a.textContent = "usuń";
    a.className = "del-button";
    a.addEventListener("click", function () {
        deleteRequest(itemID);
    })
    ul.appendChild(a);
}

function deleteRequest(id) {
    fetch(API + "/" + id, {
        method: "DELETE"
    })
        .then(response => response.json())
        .then(json => {
            document.getElementById('popup-msg').textContent = json["message"];
            popup.style.visibility = "visible"
        })
        .catch(error => console.error(error));

}

document.getElementById('popup-button').addEventListener("click", function () {
    popup.style.visibility = "hidden";
})

fetchElements();






