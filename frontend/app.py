import streamlit as st
import requests

# Correct API Endpoints
ASK_API_URL = "http://18.217.194.58:8088/ask"
GOOGLE_API_URL = "https://9phsnnogsi.execute-api.us-east-1.amazonaws.com/default/Google"

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def fetch_langchain_response(question):
    try:
        payload = {"question": question}
        response = requests.post(ASK_API_URL, json=payload)
        response.raise_for_status()

        # Attempt to parse JSON response
        try:
            json_response = response.json()
            return json_response
        except ValueError:
            # Handle JSON decoding errors
            st.error("Failed to parse JSON response from LangChain API.")
            return f"Failed to parse response: {response.text}"
    except requests.RequestException as e:
        # Handle general request exceptions
        st.error(f"Error communicating with LangChain API: {e}")
        return f"Error communicating with LangChain API: {e}"


def fetch_google_conversion(text):
    try:
        payload = {"text": text}
        response = requests.post(GOOGLE_API_URL, json=payload)
        response.raise_for_status()

        try:
            json_response = response.json()
            if isinstance(json_response, dict) and 'candidates' in json_response:
                candidates = json_response.get('candidates', [])
                if candidates and 'content' in candidates[0]:
                    parts = candidates[0]['content'].get('parts', [])
                    if parts and 'text' in parts[0]:
                        return parts[0]['text']
            return str(json_response)
        except ValueError:
            return response.text
    except requests.RequestException as e:
        return f"Error fetching Google conversion: {e}"

def main():
    st.title("Tweet Chat Analysis")

    initialize_session_state()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the tweet or data analysis..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            langchain_response = fetch_langchain_response(prompt)
            processed_response = fetch_google_conversion(langchain_response)

            # Display the final response
            st.markdown(processed_response)
            st.session_state.messages.append({"role": "assistant", "content": processed_response})

if __name__ == "__main__":
    st.set_page_config(page_title="Tweet Chat Analysis", page_icon="🐦")
    main()
