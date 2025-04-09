# Examples

This page provides examples using the Python SDK. For examples using other implementations, see:
- [Java SDK Examples](java-examples.md)
- [Web Frontend Examples](web-frontend-examples.md)

For details about which implementation best suits your needs, see the [Project Structure](project-structure.md) documentation.

This document provides practical examples of using Nova ACT for various automation scenarios.

## Basic Usage

### Simple Web Navigation

```python
from nova_act import NovaAct

with NovaAct() as nova:
    # Search on Google
    nova.act("search for python programming")
    
    # Click a specific link
    nova.act("click the link to python.org")
    
    # Navigate back
    nova.act("go back to the previous page")
```

### Form Interaction

```python
from nova_act import NovaAct

def fill_contact_form():
    with NovaAct(starting_page="https://example.com/contact") as nova:
        # Fill out a form with structured data
        nova.act("""
            Fill out the contact form with:
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

## Advanced Usage

### E-commerce Automation

```python
from nova_act import NovaAct
from typing import Optional

def order_product(product_name: str, quantity: int = 1) -> Optional[str]:
    """
    Order a product from Amazon.
    
    Args:
        product_name: Name of the product to order
        quantity: Number of items to order
        
    Returns:
        Order confirmation number if successful, None otherwise
    """
    with NovaAct(
        starting_page="https://amazon.com",
        headless=True  # Run in headless mode for production
    ) as nova:
        try:
            # Search for product
            nova.act(f"search for {product_name}")
            
            # Select product
            nova.act("select the first result")
            
            # Set quantity
            if quantity > 1:
                nova.act(f"set quantity to {quantity}")
            
            # Add to cart
            nova.act("click add to cart")
            
            # Proceed to checkout
            nova.act("proceed to checkout")
            
            # Get order confirmation
            result = nova.act("what is the order confirmation number?")
            return result.response
            
        except Exception as e:
            print(f"Error during order process: {e}")
            return None

if __name__ == "__main__":
    confirmation = order_product("coffee maker", quantity=2)
    if confirmation:
        print(f"Order placed successfully! Confirmation: {confirmation}")
```

### Data Scraping with Schema Validation

```python
from nova_act import NovaAct
from typing import List, Dict
import json

def scrape_product_details(url: str) -> List[Dict]:
    """
    Scrape product details from an e-commerce page.
    
    Args:
        url: URL of the product page
        
    Returns:
        List of product details
    """
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
                "description": {"type": "string"},
                "rating": {"type": "number"},
                "reviews": {"type": "integer"}
            },
            "required": ["name", "price"]
        }
    }
    
    with NovaAct(starting_page=url) as nova:
        result = nova.act(
            "extract all product details including name, price, description, rating, and number of reviews",
            schema=schema
        )
        
        if result.matches_schema:
            return result.parsed_response
        else:
            print("Failed to validate response against schema")
            return []

if __name__ == "__main__":
    products = scrape_product_details("https://example.com/products")
    print(json.dumps(products, indent=2))
```

### Error Handling and Recovery

```python
from nova_act import NovaAct
from nova_act.types.errors import StartFailed, StopFailed, ActFailed
import time

def robust_automation(max_retries: int = 3):
    """
    Perform automation with retry logic and error handling.
    
    Args:
        max_retries: Maximum number of retry attempts
    """
    for attempt in range(max_retries):
        try:
            with NovaAct() as nova:
                # Perform actions
                nova.act("search for python programming")
                nova.act("click the first result")
                
                # Validate the result
                result = nova.act("is this a python programming website?")
                if not result.response.lower().startswith("yes"):
                    raise ActFailed("Wrong website loaded")
                
                return  # Success, exit the function
                
        except (StartFailed, StopFailed, ActFailed) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying after 5 seconds...")
                time.sleep(5)
            else:
                print("Max retries reached. Giving up.")
                raise

if __name__ == "__main__":
    robust_automation()
```

## Best Practices

1. **Use Context Manager**: Always use the `with` statement for proper resource management
2. **Handle Errors**: Implement appropriate error handling and recovery mechanisms
3. **Validate Responses**: Use schema validation for structured data extraction
4. **Add Timeouts**: Set reasonable timeouts for long-running actions
5. **Log Actions**: Implement logging for debugging and monitoring
6. **Clean Up**: Ensure proper cleanup of resources in all scenarios

For more examples and use cases, check out our [GitHub repository](https://github.com/your-org/nova-act). 