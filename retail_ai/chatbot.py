import re

def get_chatbot_response(user_query, products_df):
    """
    A simple rule-based and keyword-matching chatbot.
    """
    query = user_query.lower()
    
    # Simple FAQ matching
    faq_responses = {
        r"return|refund": "We offer a 30-day return policy. Items must be in their original condition.",
        r"delivery|shipping|track": "Standard delivery takes 3-5 business days. Express shipping is 1-2 days.",
        r"contact|support|phone|email": "You can reach us at support@retailapp.com or call 1-800-RETAIL-AI.",
        r"hi|hello|hey": "Hello! I am your AI retail assistant. How can I help you today? You can ask about our return policy, delivery, or specific products.",
        r"thank": "You're welcome! Let me know if you need anything else.",
    }
    
    for pattern, response in faq_responses.items():
        if re.search(pattern, query):
            return response
            
    # Simple product search based on query keywords
    # For example: "Do you have laptops?" -> "laptop"
    words = query.split()
    matched_products = []
    
    for _, row in products_df.iterrows():
        # Check if any word from query is in product name or category
        product_name_words = row['name'].lower().split()
        category_words = row['category'].lower().split()
        
        for word in words:
            if len(word) > 3 and (word in row['name'].lower() or word in row['category'].lower()):
                matched_products.append(row)
                break
                
    if matched_products:
        response = "I found these products that might interest you: "
        # Just return top 2 matches to keep it readable
        items = [f"{p['name']} (${p['price']})" for p in matched_products[:2]]
        response += ", ".join(items) + "."
        return response
        
    return "I'm not quite sure about that. Could you try asking something else, or ask about returns, shipping, or our catalog?"
