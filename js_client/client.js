const baseEndpoint = 'http://localhost:8000/api';

const loginForm = document.getElementById('login-form');
const searchForm = document.getElementById('search-form');
const contentContainer = document.getElementById('content-container');

if (loginForm) {
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const loginFormData = new FormData(loginForm);
        const data = Object.fromEntries(loginFormData);
        const loginEndpoint = `${baseEndpoint}/token/`;
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
        fetch(loginEndpoint, options)
            .then(res => res.json())
            .then(data => {
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                getProductList();
            })
            .catch(err => console.log(err));
    });
}

if (searchForm) {
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(searchForm);
        const data = Array.from(formData);
        const urlSearchParams = new URLSearchParams(data);
        const endpoint = `${baseEndpoint}/search?${urlSearchParams}`;
        const headers = {
            'Content-Type': 'application/json'
        };
        const token = localStorage.getItem('access');
        if (token) headers['Authorization'] = `Bearer ${token}`;
        const options = {
            method: 'GET',
            headers
        };
        fetch(endpoint, options)
            .then(res => res.json())
            .then(data => displayData(data))
            .catch(err => console.log(err));
    });
}

function displayData(data) {
    if (contentContainer) {
        contentContainer.innerHTML = '<pre>' + JSON.stringify(data) + '</pre>';
    }
}

function getProductList() {
    const endpoint = `${baseEndpoint}/products/`;
    const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access')}`
            },
        }
    fetch(endpoint, options)
            .then(res => res.json())
            .then(data => displayData(data))
            .catch(err => console.log(err));
}

const searchClient = algoliasearch('615T5O3I3E', 'f52a0c7fdd62b0904e83b5b0b93b6fd1');

const search = instantsearch({
    indexName: 'cfe_Product',
    searchClient,
});

search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
    }),

    instantsearch.widgets.clearRefinements({
        container: '#clear-refinements',
    }),

    instantsearch.widgets.refinementList({
        container: '#user-list',
        attribute: 'user'
    }),

    instantsearch.widgets.refinementList({
        container: '#public-list',
        attribute: 'public'
    }),

    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item: `
                <div>
                    <p>{{#helpers.highlight}}{"attribute": "title"}{{/helpers.highlight}}</p>
                    <p>{{#helpers.highlight}}{"attribute": "body"}{{/helpers.highlight}}</p>
                    <p>{{ user }}</p>
                    <p>\${{ price }}</p>
                </div>
            `
      }
    })
]);

search.start();
