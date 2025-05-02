// Dynamically load the navigation bar and highlight the current tab
document.addEventListener('DOMContentLoaded', () => {
    fetch('navigation-bar.html') // Load the navigation bar HTML
        .then(response => response.text())
        .then(data => {
            // Insert the navigation bar into the placeholder
            document.getElementById('navbar-placeholder').innerHTML = data;

            // Highlight the current tab
            const currentPage = window.location.pathname.split('/').pop(); // Get the current page filename
            const navLinks = document.querySelectorAll('.navbar a'); // Select all navbar links

            navLinks.forEach(link => {
                if (link.getAttribute('href') === currentPage) {
                    link.classList.add('active'); // Add the 'active' class to the matching link
                } else {
                    link.classList.remove('active'); // Remove 'active' class from non-matching links
                }
            });
        })
        .catch(error => console.error('Error loading navbar:', error));
});