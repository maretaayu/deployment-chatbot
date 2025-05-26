import streamlit as st
import requests
import datetime

# ========== CONFIG ==========
OPENROUTER_API_KEY = "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"  # Ganti dengan OpenRouter API Key-mu

# List model yang tersedia
AVAILABLE_MODELS = [
    "deepseek/deepseek-chat-v3-0324",
    "anthropic/claude-3-haiku",
]



HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost:8501",  # Ganti dengan domain kamu
    "X-Title": "AI Chatbot Streamlit"
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ========== STREAMLIT APP ==========
st.title("🧠 AI Chatbot Bubble Style")

# Simple model selection
selected_model = st.selectbox(
    "Select AI Model:",
    options=AVAILABLE_MODELS,
    index=0  # pilih yang pertama di list
)


# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tampilkan chat sebelumnya
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        
        # Display timestamp directly
        st.caption(f"{chat['timestamp']}")

# Input dari pengguna
user_input = st.chat_input("Tulis pesan di sini...")

if user_input:
    # Get current timestamp in simplified format
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Display user message with timestamp
    with st.chat_message("user"):
        st.markdown(user_input)
        st.caption(f"{current_time}")
    
    # Add to history with timestamp
    st.session_state.chat_history.append({
        "role": "user", 
        "content": user_input,
        "timestamp": current_time
    })

    # Kirim ke OpenRouter API
    with st.spinner("Mengetik..."):
        payload = {
            "model": selected_model,  # Use the selected model
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]  
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            bot_reply = response.json()['choices'][0]['message']['content']
        else:
            bot_reply = f"⚠️ Maaf, gagal mengambil respons dari OpenRouter. Status code: {response.status_code}"
    
    # Get response timestamp
    response_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Display assistant message with timestamp in a nicer format
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
        st.caption(f"{response_time}")
    
    # Add to history with timestamp
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": bot_reply,
        "timestamp": response_time
    })