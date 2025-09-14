import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyCM4vIdZylsML_EvYub0ky-ynPuJtYXvUE")  # apni API key lagao

# --- Pizza Hut Knowledge Base (Menu + Policies) ---
pizza_menu = {
    "Pizzas": {
        "Margherita": 8.99,
        "Pepperoni": 10.99,
        "BBQ Chicken": 11.99,
        "Veggie Supreme": 9.99,
        "Meat Lovers": 12.99
    },
    "Deals": {
        "Family Feast (2 Large Pizzas + Drinks)": 24.99,
        "Party Deal (3 Medium Pizzas + Garlic Bread)": 29.99,
        "Couple Deal (1 Medium Pizza + 2 Drinks)": 14.99
    },
    "Sides": {
        "Garlic Bread": 4.99,
        "Chicken Wings": 6.99,
        "Cheese Sticks": 5.49
    },
    "Drinks": {
        "Coke (1.5L)": 2.99,
        "Pepsi (1.5L)": 2.99,
        "Water Bottle": 1.49
    }
}

faq_knowledge = """
You are a Pizza Hut customer support & ordering assistant.

Company: Pizza Hut
Delivery Time: 30-45 minutes (home delivery)
Return/Refund Policy: Only for wrong/damaged items (within 24 hours)
Contact Email: support@pizzahut.com
Contact Number: +1 (800) 555-PIZZA
"""

# --- Function to Generate Response ---
def support_chatbot(user_query):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"{faq_knowledge}\n\nUser: {user_query}\nAssistant:")
    return response.text

# --- Streamlit UI ---
st.set_page_config(page_title="Pizza Hut Assistant", page_icon="🍕")

st.title("🍕 Pizza Hut Ordering & Support Assistant")
st.write("Welcome to Pizza Hut! You can browse our menu, order items, and get customer support.")

# --- Show Menu ---
st.subheader("📋 Menu")
for category, items in pizza_menu.items():
    st.markdown(f"### {category}")
    for item, price in items.items():
        st.write(f"- {item}: ${price:.2f}")

# --- Order Section ---
st.subheader("🛒 Place Your Order")
order = {}
for category, items in pizza_menu.items():
    st.markdown(f"**{category}**")
    selected_items = st.multiselect(f"Select {category}", list(items.keys()), key=category)
    for item in selected_items:
        qty = st.number_input(f"Quantity of {item}", min_value=1, max_value=10, value=1, key=item)
        order[item] = {"price": items[item], "qty": qty}

# --- Generate Receipt ---
if st.button("Generate Receipt"):
    if order:
        st.subheader("🧾 Order Receipt")
        total = 0
        for item, details in order.items():
            cost = details["price"] * details["qty"]
            total += cost
            st.write(f"{item} x {details['qty']} = ${cost:.2f}")
        st.markdown(f"**Total: ${total:.2f}**")
        
        st.success("✅ Your order has been placed! Estimated delivery: 30-45 minutes.")
    else:
        st.warning("Please select at least one item to order.")

# --- Support Chat ---
st.subheader("💬 Customer Support Chat")
user_query = st.text_input("Ask a question (delivery, refund, contact, etc.):")

if st.button("Ask Assistant"):
    if user_query.strip():
        with st.spinner("Assistant is typing..."):
            answer = support_chatbot(user_query)
        st.info(f"**Assistant:** {answer}")
    else:
        st.warning("Please enter a question.")
