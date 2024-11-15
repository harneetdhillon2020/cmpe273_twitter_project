import streamlit as st
import time

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'url_submitted' not in st.session_state:
        st.session_state.url_submitted = False

def check_url_validity(url):
    # Add your URL validation logic here
    return "twitter.com" in url or "x.com" in url

def process_tweet(url):
    # Add our tweet processing logic here
    # Placeholder to simulate processing
    time.sleep(1)
    return f"Processed tweet from URL: {url}"

def main():
    st.title("Tweet Chat Analysis")
    
    # Initialize session state
    initialize_session_state()
    
    # If URL hasn't been submitted yet, show the URL input interface
    if not st.session_state.url_submitted:
        with st.form(key='url_form'):
            url = st.text_input("Enter Tweet URL", placeholder="https://twitter.com/username/status/123456789")
            submit_button = st.form_submit_button("Analyze Tweet")
            
            if submit_button:
                if check_url_validity(url):
                    st.session_state.url_submitted = True
                    # Process the tweet and add initial message
                    result = process_tweet(url)
                    st.session_state.messages.append({"role": "assistant", "content": f"I've analyzed the tweet. {result}\nWhat would you like to know about it?"})
                    st.rerun()
                else:
                    st.error("Please enter a valid Twitter/X URL")
    
    # If URL has been submitted, show the chat interface
    else:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about the tweet..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Response
            with st.chat_message("assistant"):
                response = f"Let me help you with your question about: '{prompt}'"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Add a button to analyze a new tweet
        if st.button("Analyze Another Tweet"):
            st.session_state.url_submitted = False
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    st.set_page_config(page_title="Tweet Chat Analysis", page_icon="🐦")
    main()