function fetchEvents() {
    fetch('/events')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('events-container');
            container.innerHTML = '';
            data.forEach(event => {
                const div = document.createElement('div');
                div.className = 'event';
                div.textContent = event.message;
                container.appendChild(div);
            });
        });
}

fetchEvents();
setInterval(fetchEvents, 15000);  // Every 15 seconds
