// Basic background script
console.log('Nova ACT Extension background script initialized');

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Received message:', message);
  // Send a response
  sendResponse({ status: 'ok' });
  return true;
});