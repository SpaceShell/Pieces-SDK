from pieces_copilot_sdk import PiecesClient
import streamlit as st

# Create an instance of PiecesClient
pieces_client = PiecesClient(
    config={
        'baseUrl': 'http://localhost:1000'
    }
)

st.title("MLH Demo - Pieces SDK")
st.write("Hi! Have any questions?")

#input box
query = st.chat_input("Enter your prompt here")

# 1. Create a new conversation
conversation_response = pieces_client.create_conversation(
    props={
        "name": "Test Conversation",
        "firstMessage": "Hello, what does Pieces SDK do?"
    }
)

# Check if the conversation was created successfully
if conversation_response:
    with st.spinner("Thinking..."):
        with st.chat_message("assistant"):
            st.write("First Message Response:", conversation_response['answer']['text'])

    # 2. Get the created conversation details
    conversation_id = conversation_response['conversation'].id
    conversation_details = pieces_client.get_conversation(
        conversation_id=conversation_id,
        include_raw_messages=True
    )