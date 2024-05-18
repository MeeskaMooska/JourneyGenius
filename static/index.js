const SOURCE_SELECTOR = document.getElementById('source_selector');

function get_articles(source) {
    const url = `/api/articles/${source}`;

    fetch(url)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

document.getElementById('test_button').addEventListener('click', () => {get_articles(SOURCE_SELECTOR.value)});
