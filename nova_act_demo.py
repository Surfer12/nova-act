#!/usr/bin/env python3
"""
Nova Act Demo Script
This script demonstrates basic usage of the Nova Act browser automation tool.
"""
import os
import sys
from nova_act import NovaAct

# Create a NovaAct instance
nova = NovaAct(
    # Starting web page for the browser
    starting_page="https://www.google.com",
    # Set to False to see the browser in action
    headless=False,
    chrome_channel="chromium",
    screen_width=1600,
    screen_height=900,
    user_data_dir=None
)

try:
    # Start the browser
    print("Starting Nova Act browser...")
    nova.start()
    
    # Perform a search action
    print("Performing search action...")
    result = nova.act("Search for 'Nova Act browser automation'")
    
    # Print the result
    print(f"\nAction result: {result}")
    
    # You can perform additional actions
    # result2 = nova.act("Click on the first search result")
    
    # Keep the browser open for a while
    input("\nPress Enter to close the browser...")
    
except Exception as e:
    print(f"Error: {e}")

finally:
    # Always stop the client to clean up resources
    print("Stopping Nova Act browser...")
    nova.stop()
    print("Done!") 