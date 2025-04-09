# Nova Act Quick Start Guide

Nova Act is an early research preview of an SDK + model for building agents designed to reliably take actions in web browsers. This guide will help you get started quickly.

## Prerequisites

1. Operating System: MacOS or Ubuntu
2. Python 3.10 or above
3. Nova Act API key (obtain from https://nova.amazon.com/act)

## Installation

```bash
pip install nova-act
```

## Authentication

Set your API key as an environment variable:

```bash
export NOVA_ACT_API_KEY="YOUR_API_KEY"
```

## Basic Usage

### Simple Script Example

```python
from nova_act import NovaAct

with NovaAct(starting_page="https://www.amazon.com") as nova:
    nova.act("search for a coffee maker")
    nova.act("select the first result")
    nova.act("scroll down or up until you see 'add to cart' and then click 'add to cart'")
```

### Interactive Mode

```python
from nova_act import NovaAct

# Create and start a NovaAct instance
nova = NovaAct(starting_page="https://www.amazon.com")
nova.start()

# Execute actions one by one
nova.act("search for a coffee maker")
nova.act("select the first result")
nova.act("scroll down or up until you see 'add to cart' and then click 'add to cart'")

# Close the browser when done
nova.stop()
```

## Effective Prompting Strategies

### Be Prescriptive and Succinct

❌ DON'T
```python
nova.act("From my order history, find my most recent order from India Palace and reorder it")
```

✅ DO
```python
nova.act("Click the hamburger menu icon, go to Order History, find my most recent order from India Palace and reorder it")
```

### Break Up Large Tasks into Smaller Steps

❌ DON'T
```python
nova.act("book me a hotel that costs less than $100 with the highest star rating")
```

✅ DO
```python
nova.act(f"search for hotels in Houston between {startdate} and {enddate}")
nova.act("sort by avg customer review")
nova.act("hit book on the first hotel that is $100 or less")
nova.act(f"fill in my name, address, and DOB according to {blob}")
```

## Extracting Information

Use Pydantic models to extract structured data:

```python
from pydantic import BaseModel
from nova_act import NovaAct, BOOL_SCHEMA

class Book(BaseModel):
    title: str
    author: str

class BookList(BaseModel):
    books: list[Book]

with NovaAct(starting_page="https://example.com/books") as nova:
    # Extract structured data
    result = nova.act("Return all books on this page", schema=BookList.model_json_schema())
    if result.matches_schema:
        book_list = BookList.model_validate(result.parsed_response)
        print(f"Found {len(book_list.books)} books")
    
    # Simple boolean response
    is_logged_in = nova.act("Am I logged in?", schema=BOOL_SCHEMA)
    if is_logged_in.matches_schema and is_logged_in.parsed_response:
        print("User is logged in")
```

## Parallel Processing

Run multiple browser sessions in parallel:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from nova_act import NovaAct, ActError

def process_url(url):
    with NovaAct(starting_page=url) as nova:
        result = nova.act("extract the main heading")
        return result.response

urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]
results = []

with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_url = {executor.submit(process_url, url): url for url in urls}
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result = future.result()
            results.append({"url": url, "heading": result})
        except ActError as e:
            print(f"Error processing {url}: {e}")

print(results)
```

## Handling Authentication

Create a persistent browser profile:

```python
import os
from nova_act import NovaAct

user_data_dir = "/path/to/your/profile"
os.makedirs(user_data_dir, exist_ok=True)

with NovaAct(starting_page="https://amazon.com/", user_data_dir=user_data_dir, clone_user_data_dir=False):
    input("Log into your websites, then press enter...")

print(f"User data dir saved to {user_data_dir}")
```

Then use this profile in your scripts:

```python
from nova_act import NovaAct

with NovaAct(starting_page="https://amazon.com", user_data_dir="/path/to/your/profile") as nova:
    # You're already logged in
    nova.act("go to my orders")
```

## Handling Sensitive Information

Never include sensitive information in prompts:

```python
from getpass import getpass
from nova_act import NovaAct

with NovaAct(starting_page="https://example.com/login") as nova:
    nova.act("enter username janedoe and click on the password field")
    # Get password securely and type it directly
    nova.page.keyboard.type(getpass())
    nova.act("click the login button")
```

## Handling Captchas

Let the user solve captchas:

```python
from nova_act import NovaAct, BOOL_SCHEMA

with NovaAct(starting_page="https://example.com") as nova:
    nova.act("click the submit button")
    
    # Check for captcha
    result = nova.act("Is there a captcha on the screen?", schema=BOOL_SCHEMA)
    if result.matches_schema and result.parsed_response:
        input("Please solve the captcha and hit return when done")
    
    nova.act("continue with the form submission")
```

## Recording Sessions

Record browser sessions for debugging:

```python
from nova_act import NovaAct

with NovaAct(
    starting_page="https://example.com",
    logs_directory="/path/to/logs",
    record_video=True
) as nova:
    nova.act("perform some actions")
    # Video will be saved to the logs directory
```

## Known Limitations

- Cannot interact with non-browser applications
- Unreliable with high-level prompts
- Cannot interact with elements hidden behind mouseovers
- Cannot interact with browser window modals (like location access requests)

## Getting Help

If you encounter issues, submit a bug report to nova-act@amazon.com with:
- Description of the issue
- Session ID (from console logs)
- Script of the workflow you're using
