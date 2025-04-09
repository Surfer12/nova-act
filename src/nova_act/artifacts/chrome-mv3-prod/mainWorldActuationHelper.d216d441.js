// Main world actuation helper
console.log('Nova ACT Extension main world actuation helper initialized');

// Create a global object to expose methods to the main world
window.novaActMain = {
  executeAction: function(action, params) {
    console.log('Executing action:', action, params);
    return { success: true, action, params };
  }
};