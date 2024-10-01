// Function to toggle dark mode for the body and background color for other elements
function toggleTheme() {
  const isChecked = document.getElementById('theme-switch').checked;
  const newMode = isChecked ? 'dark' : 'light';

  // Toggle the theme on the body element
  document.body.classList.toggle('dark-mode', isChecked);
  document.body.classList.toggle('light-mode', !isChecked);
 // Get all elements with class 'card-body' and toggle dark mode
  const cardBodies = document.querySelectorAll('.card-body');
  cardBodies.forEach(card => {
    card.classList.toggle('dark-mode');
  });
  // Save the new mode to local storage
  localStorage.setItem('theme', newMode);
}

// Function to initialize theme and background color based on local storage
function initializeTheme() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  const isDarkMode = savedTheme === 'dark';

  // Set initial theme on the body element
  document.body.classList.add(isDarkMode ? 'dark-mode' : 'light-mode');
  document.body.classList.remove(isDarkMode ? 'light-mode' : 'dark-mode');

 // Get all elements with class 'card-body' and toggle dark mode
  const cardBodies = document.querySelectorAll('.card-body');
  cardBodies.forEach(card => {
    card.classList.toggle(isDarkMode ? 'dark-mode' : 'light-mode');
  });
  // Set checkbox state
  document.getElementById('theme-switch').checked = isDarkMode;
}

// Add event listener to the checkbox
document.getElementById('theme-switch').addEventListener('change', toggleTheme);

// Initialize the theme and colors when the page loads
initializeTheme();
