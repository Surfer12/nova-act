// Basic actuation helpers
console.log('Nova ACT Extension actuation helpers initialized');

// Helper functions for browser automation
const actuationHelpers = {
  click: function(selector) {
    const element = document.querySelector(selector);
    if (element) {
      element.click();
      return true;
    }
    return false;
  },
  
  type: function(selector, text) {
    const element = document.querySelector(selector);
    if (element) {
      element.value = text;
      return true;
    }
    return false;
  },
  
  scroll: function(x, y) {
    window.scrollTo(x, y);
    return true;
  }
};

window.actuationHelpers = actuationHelpers;