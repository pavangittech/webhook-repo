function showAlert() {
    const alertBox = document.getElementById("alert-box");
    alertBox.classList.add("show");
    setTimeout(() => {
        alertBox.classList.remove("show");
    }, 2000); // Show for 2 seconds
}

let lastMessage = "";

function fetchEvents() {
    console.log("🔄 Polling...");
    fetch('/events')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('events-container');
            container.innerHTML = '';

            data.forEach((event, index) => {
                const div = document.createElement('div');
                div.className = 'event';

                let icon = '❔';
                let iconClass = '';

                if (event.message.includes("pushed to")) {
                    icon = '📤';
                    iconClass = 'push-icon';
                } else if (event.message.includes("submitted a pull request")) {
                    icon = '📥';
                    iconClass = 'pr-icon';
                } else if (event.message.includes("merged branch")) {
                    icon = '🔀';
                    iconClass = 'merge-icon';
                }

                div.innerHTML = `<span class="${iconClass}">${icon}</span><span>${event.message}</span>`;
                container.appendChild(div);
            });

            // Trigger alert if new message
            if (data[0] && data[0].message !== lastMessage) {
                lastMessage = data[0].message;
                showAlert();
            }
        })
        .catch(err => console.error("Error fetching events:", err));
}

// Theme toggle
document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById('theme-switch');
    toggle.addEventListener('change', () => {
        document.body.classList.toggle('dark');
    });
});


// Call immediately and every 15 seconds
fetchEvents();
setInterval(fetchEvents, 15000);
