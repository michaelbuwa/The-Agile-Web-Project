/*A function to generate a random color in hex format
and set it as the background color of the page on load.*/
const getRandomColor = () => `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;

// Set random background color on page load
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.backgroundColor = getRandomColor();
});

// Handle form submission
document.getElementById('upload-form').addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent page refresh

  const formData = new FormData(event.target);
  console.log('Color Name:', formData.get('color-name'));
  console.log('Associations:', formData.get('associations'));

  event.target.reset(); // Reset form fields
  document.body.style.backgroundColor = getRandomColor(); // Set new random background color
});