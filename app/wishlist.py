# app/wishlist.py

wishlist = []

def add_to_wishlist(item):
    """
    Adds an item to the wishlist.
    """
    wishlist.append(item)

def display_wishlist():
    """
    Displays all items in the wishlist as a Markdown string.
    """
    results = []
    for item in wishlist:
        results.append(f"**{item['name']}**\n{item['description']}\n**Prix**: {item['price']}\n![Image]({item['image']})")
    return "\n\n".join(results)