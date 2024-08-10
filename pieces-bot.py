from pieces_copilot_sdk import PiecesClient
import streamlit as st
import time

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
        "name": "First Conversation",
        # "firstMessage": ""
    }
)

# Check if the conversation was created successfully
if conversation_response:
    st.write("**Conversation Created:**", conversation_response['conversation'].id)
    # sl.write("First Message Response:", conversation_response['answer']['text'])

    # 2. Get the created conversation details
    conversation_id = conversation_response['conversation'].id
    conversation_details = pieces_client.get_conversation(
        conversation_id=conversation_id,
        include_raw_messages=True
    )

    # Access the conversation name using the key
    st.write("**Conversation Name:**", conversation_details.get('name'))

    # Initialize a session state variable to store the appended text
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(f"{message['content']}")

    if query:
        #Display user chat
        st.chat_message("user").markdown(query)
    #    Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("Thinking..."):
            with st.chat_message("assistant"):
                # 3. Ask a question within the created conversation
                question_response = pieces_client.prompt_conversation(
                    message=query,
                    conversation_id=conversation_id
                )

                def stream_data():
                    response = question_response['text']
                    for word in response.split(" "):
                        yield word + " "
                        time.sleep(0.02)


                st.write_stream(stream_data)
                
                st.session_state.messages.append({"role": "assistant", "content": question_response['text']})