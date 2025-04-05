# Examples

Here are some examples of how to use Nova ACT in different scenarios.

## Basic Web Navigation

```python
from nova_act import NovaAct

with NovaAct() as nova:
    # Search for something on Google
    nova.act("search for python programming")
    
    # Click a specific link
    nova.act("click the link to python.org")
    
    # Fill out a form
    nova.act("fill out the search form with 'getting started' and submit")
```

## E-commerce Automation

```python
from nova_act import NovaAct

def order_coffee_maker():
    with NovaAct(starting_page="https://amazon.com") as nova:
        # Search for a product
        nova.act("search for a coffee maker")
        
        # Select a product
        nova.act("select the first result")
        
        # Add to cart
        nova.act("scroll down or up until you see 'add to cart' and then click 'add to cart'")

if __name__ == "__main__":
    order_coffee_maker()
```

## Form Filling

```python
from nova_act import NovaAct

def fill_contact_form():
    with NovaAct(starting_page="https://example.com/contact") as nova:
        # Fill out a complex form
        nova.act("""
            Fill out the contact form with the following information:
            - Name: John Doe
            - Email: john@example.com
            - Subject: General Inquiry
            - Message: Hello, I would like more information about your services.
        """)
        
        # Submit the form
        nova.act("click the submit button")

if __name__ == "__main__":
    fill_contact_form()
```

## Using JSON Schema

```python
from nova_act import NovaAct, BOOL_SCHEMA

def check_login_status():
    with NovaAct() as nova:
        # Check if we're logged in
        result = nova.act(
            "Are we logged in to the website?",
            schema=BOOL_SCHEMA
        )
        
        if result.matches_schema and result.parsed_response:
            print("We are logged in!")
        else:
            print("We are not logged in.")

if __name__ == "__main__":
    check_login_status()
```

## Error Handling

```python
from nova_act import NovaAct
from nova_act.types.errors import StartFailed, StopFailed

try:
    nova = NovaAct()
    nova.start()
    
    try:
        result = nova.act("perform some action")
        print(f"Action completed: {result}")
    except Exception as e:
        print(f"Error during action: {e}")
    finally:
        nova.stop()
except StartFailed as e:
    print(f"Failed to start Nova ACT: {e}")
except StopFailed as e:
    print(f"Failed to stop Nova ACT: {e}")
``` 