// Basic content script
console.log('Nova ACT Extension content script initialized');

// Add a listener for commands
window.addEventListener('nova-act-command', (event) => {
  console.log('Received command:', event.detail);
  // Process the command
});

// Create a marker element to signal that the listeners are registered
const marker = document.createElement('div');
marker.id = 'autonomy-listeners-registered';
marker.style.display = 'none';
document.body.appendChild(marker);