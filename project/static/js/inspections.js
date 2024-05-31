function fetchElements(api_url, fields, numeric_fields) {
    fetch(api_url)
        .then(response => response.json())
        .then(json => {
            const list_container = document.getElementById('list-container');
            json.forEach(item => {
                var ul = document.createElement('ul');
                var item_class = API.split("/").slice(-1);
                ul.className = "values-list " + item_class;
                list_container.appendChild(ul);
                fields.forEach(key => {
                    addSpan(ul, item, key, numeric_fields.has(key));
                })
                addDeleteButton(api_url, ul, item['id']);
            });
        })
        .catch(error => console.error(error));
}

function addSpan(ul, item, key, numeric) {
    var span = document.createElement('span');
    if (numeric) {
        span.className = "numeric";
    }
    span.textContent = item[key];
    ul.appendChild(span);
}

function addDeleteButton(api_url, ul, itemID) {
    var a = document.createElement('a');
    a.textContent = "usuń";
    a.className = "del-button";
    a.addEventListener("click", function () {
        deleteRequest(api_url, itemID);
    })
    ul.appendChild(a);
}

function deleteRequest(api_url, id) {
    fetch(api_url + "/" + id, {
        method: "DELETE"
    })
        .then(response => response.json())
        .then(json => {
            document.getElementById('popup-msg').textContent = json["message"];
            popup.style.visibility = "visible"
        })
        .catch(error => console.error(error));

}

const popup = document.getElementById('popup');
document.getElementById('popup-button').addEventListener("click", function () {
    popup.style.visibility = "hidden";
})

document.getElementById('next-page').addEventListener("click", function () {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('page', parseInt(page) + 1);
    window.location.href = currentUrl.toString();
})

document.getElementById('prev-page').addEventListener("click", function () {
    const currentUrl = new URL(window.location.href);
    if (page > 1) {
        currentUrl.searchParams.set('page', parseInt(page) - 1);
        window.location.href = currentUrl.toString();
    }
})

var params = new URLSearchParams(window.location.search)
page = params.has('page') ? params.get('page') : 1
api = API + "?page=" + page;
fetchElements(api, FIELDS, NUMERIC_FIELDS);






