document.addEventListener('DOMContentLoaded', () => {
    const addButton = document.querySelector('.search-button');
    addButton.addEventListener('click', () => {
        const username = input.value.trim();
        if (!username) return;
        fetch('/api/add_friend', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username})
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('Friend added!');
                input.value = '';
            } else {
                alert(data.message || 'Could not add friend.');
            }
        });
    });
    const input = document.querySelector('.search-input[placeholder="add friend"]');
    const suggestionsList = document.getElementById('suggestions-list');

    input.addEventListener('input', () => {
        const query = input.value.trim();
        if (!query) {
            suggestionsList.innerHTML = '';
            suggestionsList.style.display = 'none';
            return;
        }

        fetch(`/api/search_users?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = '';
                if (data.length === 0) {
                    suggestionsList.style.display = 'none';
                    return;
                }
                data.forEach(username => {
                    const li = document.createElement('li');
                    li.textContent = username;
                    li.classList.add('suggestion-item');
                    li.addEventListener('click', () => {
                        input.value = username;
                        suggestionsList.innerHTML = '';
                        suggestionsList.style.display = 'none';
                    });
                    suggestionsList.appendChild(li);
                });
                suggestionsList.style.display = 'block';
            })
            .catch(err => {
                console.error('Error fetching suggestions:', err);
                suggestionsList.innerHTML = '';
                suggestionsList.style.display = 'none';
            });
    });

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !suggestionsList.contains(e.target)) {
            suggestionsList.innerHTML = '';
            suggestionsList.style.display = 'none';
        }
    });
});
