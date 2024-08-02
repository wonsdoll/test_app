import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("스무고개")
st.write(
    "재미있는 스무고개, 진 사람 딱밤 맞기."
)

genre = st.radio(
    "Choose Your role",
    ["출제자", "도전자"],
    captions=[
        "문제를 내봅시다",
        "문제를 맞춰봅시다",
    ],
)
initial_added = True
if genre == "도전자":
    initial = "지금부터 스무고개를 할거야. 너는 출제자고, 스무고개를 진행할 단어를 생각해줘."
else:
    initial = "지금부터 스무고개를 할거야. 너는 도전자고, 20번 내에 내가 생각한 단어를 맞춰봐. 질문을 할때마다 몇 번째 질문인지 적어줘. 정답이야 라고 말하면 대화를 끝내줘"

st.write("Please enter your OpenAI API key below.")
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:


    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state or st.button("새로 시작", type= "primary"):
        st.session_state.messages = []
        initial_added = False
        st.session_state.initial_questioned = False

    if initial and initial_added == False :
        st.session_state.messages.append({"role": "system", "content": initial})
        initial_added = True

    if genre == "도전자":
         with st.chat_message("assistant"):
             st.markdown("답을 생각했습니다. 질문을 해주세요")

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if genre == "출제자" and st.session_state.initial_questioned == False :
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "assistant", "content": initial}
            ],
            stream=True,
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.initial_questioned = True

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("입력해주세요"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})