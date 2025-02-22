from src.llm_module import chat  # Import LLM chat function
from src import tools  # Import all tool functions
from loguru import logger
def format_reply(response_data):
    """Converts tool outputs into a conversational assistant response."""
    
    if "response" in response_data:  
        # LLM fallback response
        return f"🤖 {response_data['response']}"
    
    message = "🛍️ Here’s what I found for you:\n\n"

    if "products" in response_data:
        products = response_data["products"]
        for product in products:
            message += f"✨ {product['name']} - ${product['price']} (Size: {product.get('size', 'N/A')})\n"
    
    if "discount" in response_data:
        message += f"🎉 Discount available: {response_data['discount']['discount']} off!\n"
    
    if "shipping" in response_data:
        message += f"🚚 Estimated shipping time: {response_data['shipping']['shipping_time']}\n"

    if "competitor_price" in response_data:
        message += f"💰 Competitor price: ${response_data['competitor_price']['price']} at {response_data['competitor_price']['store']}\n"

    if "return_policy" in response_data:
        message += f"🔄 Return policy: {response_data['return_policy']['policy']}\n"

    return message.strip()

def react_reasoning(query):
    """Uses ReAct + Toolformer-style execution, returning assistant-like responses."""
    reasoning_steps = []
    query_lower = query.lower()

    if "find" in query_lower:
        reasoning_steps.append("Searching for matching products...")
        products = tools.search_products(query)
        logger.debug(f"{products=}")

        # Handle case when no matching products are found
        if isinstance(products, dict) and "competitor" in products:
            competitor_info = products["competitor"]
            reasoning_steps.append("No matching products found. Suggesting competitor option.")
            logger.debug(f"{reasoning_steps=}")
            return {
                "response": f"Sorry, we don’t have that, but another supplier ({competitor_info['store']}) offers it for ${competitor_info['price']}."
            }

        if not products:
            reasoning_steps.append("No products found. Switching to LLM response.")
            logger.debug(f"{reasoning_steps=}")
            return {"response": chat(query)}

        reasoning_steps.append("Products found. Checking additional details.")
        response_data = {"products": products}

        # Extract first product name
        product_name = products[0]["name"]

        # Check for price constraint (if "under" exists in the query)
        if "under" in query_lower:
            try:
                price_limit = int(next(word for word in query_lower.split() if word.isdigit()))
                filtered_products = [p for p in products if p["price"] <= price_limit]

                if not filtered_products:
                    reasoning_steps.append(f"No products under ${price_limit}. Suggesting competitor price.")
                    competitor_price = tools.compare_competitor_prices(product_name)
                    return {
                        "response": f"Sorry, we don’t have that, but another supplier offers it for ${competitor_price}."
                    }

                response_data["products"] = filtered_products
            except StopIteration:
                reasoning_steps.append("Failed to extract price limit. Proceeding normally.")

        # Additional tool-based responses
        if "discount" in query_lower:
            reasoning_steps.append("Checking for discounts...")
            response_data["discount"] = tools.check_discount(product_name)

        if "shipping" in query_lower:
            reasoning_steps.append("Checking estimated shipping time...")
            response_data["shipping"] = tools.estimate_shipping_time(product_name)

        if "compare price" in query_lower:
            reasoning_steps.append("Comparing competitor prices...")
            response_data["competitor_price"] = tools.compare_competitor_prices(product_name)

        if "return policy" in query_lower:
            reasoning_steps.append("Checking return policy...")
            response_data["return_policy"] = tools.check_return_policy(product_name)

        return response_data

    reasoning_steps.append("No relevant tool found. Using LLM to generate response.")
    return {"response": chat(query)}


if __name__ == "__main__":
    user_query = "what is a shoe? "
    response = react_reasoning(user_query)
    logger.info(format_reply(response))
