import os
import hashlib

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from booking import book_site_visit
from analytics import generate_analytics
from voice import speech_to_text, text_to_speech


# --------------------------------------------------
# ENVIRONMENT
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

with open("prompt.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Northstar Homes AI",
    page_icon="🏠"
)

st.title("🏠 Northstar Homes AI")
st.caption("AI Sales Assistant | Northstar One | Sector 79, Gurugram")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "booking_step" not in st.session_state:
    st.session_state.booking_step = None

if "booking_date" not in st.session_state:
    st.session_state.booking_date = None

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None


# --------------------------------------------------
# DEMO CONTROLS
# --------------------------------------------------

st.sidebar.title("Demo Controls")

simulate_failure = st.sidebar.checkbox(
    "Simulate booking failure"
)

show_analytics = st.sidebar.button(
    "Generate Analytics"
)
voice_response = st.sidebar.checkbox(
    "Enable voice response"
)

# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

if show_analytics:

    analytics = generate_analytics(
        st.session_state.messages
    )

    st.sidebar.subheader("Lead Analytics")

    for key, value in analytics.items():
        st.sidebar.write(
            f"**{key.replace('_', ' ').title()}:** {value}"
        )


# --------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------------------------
# VOICE INPUT
# --------------------------------------------------

st.subheader("🎤 Voice Input")

audio_file = st.audio_input(
    "Record your message"
)

voice_message = None

if audio_file:

    audio_bytes = audio_file.getvalue()

    # Create a unique ID for this recording
    audio_hash = hashlib.md5(audio_bytes).hexdigest()

    # Only process a recording once
    if audio_hash != st.session_state.last_audio_hash:

        st.session_state.last_audio_hash = audio_hash

        audio_text, error = speech_to_text(audio_file)

        if audio_text:

            voice_message = audio_text

            st.success(
                f"Transcription: {audio_text}"
            )

        else:

            st.warning(error)


# --------------------------------------------------
# TEXT INPUT
# --------------------------------------------------

typed_message = st.chat_input(
    "Type your message..."
)


# --------------------------------------------------
# USE VOICE OR TEXT
# --------------------------------------------------

user_message = voice_message or typed_message


# --------------------------------------------------
# PROCESS MESSAGE
# --------------------------------------------------

if user_message:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_message)

    user_text = user_message.lower()


    # --------------------------------------------------
    # SITE VISIT BOOKING FLOW
    # --------------------------------------------------

    booking_keywords = [
    "site visit",
    "sitevisit",
    "visit the property",
    "visit property",
    "book a visit",
    "schedule a visit",
    "schedule site visit",
    "want to visit",
    "like to visit",
    "would like to visit"
]


    # Start booking
    if (
        st.session_state.booking_step is None
        and any(
            keyword in user_text
            for keyword in booking_keywords
        )
    ):

        st.session_state.booking_step = "date"

        assistant_message = (
            "Sure. What date would you prefer "
            "for the site visit?"
        )


    # Get booking date
    elif st.session_state.booking_step == "date":

        st.session_state.booking_date = user_message

        st.session_state.booking_step = "time"

        assistant_message = (
            "Sure. What time would be convenient for you?"
        )


    # Get booking time
    elif st.session_state.booking_step == "time":

        booking_result = book_site_visit(
            st.session_state.booking_date,
            user_message,
            should_succeed=not simulate_failure
        )

        if booking_result["success"]:

            assistant_message = (
                f"Great! Your site visit has been booked "
                f"for {st.session_state.booking_date} "
                f"at {user_message}."
            )

        else:

            assistant_message = (
                "I'm sorry, I couldn't complete the "
                "site-visit booking right now. "
                "Would you like to try another time?"
            )

        # Reset booking state
        st.session_state.booking_step = None
        st.session_state.booking_date = None


    # --------------------------------------------------
    # NORMAL AI CONVERSATION
    # --------------------------------------------------

    else:

        conversation = []

        for message in st.session_state.messages:

            conversation.append(
                types.Content(
                    role=(
                        "user"
                        if message["role"] == "user"
                        else "model"
                    ),
                    parts=[
                        types.Part.from_text(
                            text=message["content"]
                        )
                    ]
                )
            )

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=conversation,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=300,
                    thinking_config=types.ThinkingConfig(
                        thinking_level="minimal"
                    )
                )
            )

            assistant_message = response.text

            if not assistant_message:

                assistant_message = (
                    "Sorry, I couldn't generate a "
                    "response right now. Please try again."
                )

        except Exception as error:

            error_message = str(error)

            if (
                "RESOURCE_EXHAUSTED" in error_message
                or "429" in error_message
            ):

                assistant_message = (
                    "The AI service is temporarily busy. "
                    "Please try again in a little while."
                )

            else:

                assistant_message = (
                f"Gemini error: {error_message}"
            )


    # --------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message
    })


    # Display assistant response
    with st.chat_message("assistant"):

        st.write(assistant_message)

        if voice_response:
            text_to_speech(assistant_message)