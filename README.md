# Northstar Homes AI

AI conversational sales assistant built for the Huvo AI Forward Deployed Engineer assignment.
The application supports text and voice interactions and is designed around prompt-driven sales-agent behaviour.

## Project

- Company: Northstar Homes
- Project: Northstar One
- Location: Sector 79, Gurugram
- Configurations: 2 BHK and 3 BHK

Starting prices:

- 2 BHK: ₹1.35 crore onwards
- 3 BHK: ₹1.75 crore onwards

## Features

- Text-based conversation
- Voice input using local Whisper
- Voice output using local text-to-speech
- English, Hindi and Hinglish support
- Conversation memory
- Budget-first qualification
- Configuration recommendation
- Customer objection handling
- Site-visit booking simulation
- Booking failure handling
- Lead analytics
- Follow-up detection
- Human escalation handling
- Demo booking-failure control

## Architecture

```text
                 Northstar Homes AI
                         |
             +-----------+-----------+
             |                       |
          Text Chat              Voice Input
             |                       |
             |                Faster-Whisper
             |                  (local, CPU)
             |                       |
             +-----------+-----------+
                         |
                  Conversation
                      Memory
                         |
                     Gemini
                         |
                  Agent Response
                         |
                 +-------+-------+
                 |               |
               Text          Voice Output
                               pyttsx3
```

## Project Structure

```
northstar-homes-ai/
│
├── app.py
├── voice.py
├── booking.py
├── analytics.py
├── prompt.txt
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── tests/
    └── test_cases.md
```

## Setup

### 1. Clone the repository

```
git clone <YOUR_GITHUB_REPOSITORY>
cd northstar-homes-ai
```

### 2. Create a virtual environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Create `.env`

Create a file named `.env` in the project root:

```
GEMINI_API_KEY=your_api_key
```

Never commit this file.

### 5. Run

```
python -m streamlit run app.py
```

## Voice Interaction

Voice input is processed locally using Faster-Whisper — no external speech-to-text
API or key is required. The first run downloads the Whisper model, which may take
a little longer than subsequent runs.

The current implementation uses:

- Whisper `small`
- Device: CPU
- Compute type: `int8`

Model size can be overridden with the `WHISPER_MODEL_SIZE` environment variable
(e.g. `large-v3` if running on a GPU with CUDA/cuDNN available — set
`device="cuda"` and `compute_type="float16"` in `voice.py` in that case).

Voice output uses the local system speech engine through pyttsx3.

## Agent Behaviour

The system prompt is designed to:

- Qualify customers naturally
- Ask for budget before revealing pricing when appropriate
- Recommend between 2 BHK and 3 BHK based on customer requirements
- Handle objections
- Support English, Hindi and Hinglish
- Avoid inventing unavailable information
- Handle site visits
- Handle booking failures
- Support follow-up requests
- Respect requests to stop communication
- Escalate appropriate questions to a human

## Important Assumptions

- Property information is limited to information provided in the assignment.
- Site visits are simulated.
- Booking availability is not connected to a real calendar.
- Pricing represents starting prices only.

## Known Limitations

- The site-visit booking system is simulated.
- Larger Whisper models can be CPU-intensive; `small` is used by default for
  responsiveness.
- Production telephony and CRM integrations are not implemented.

## AI Tools Used

- Google Gemini for conversational responses
- Faster-Whisper for local speech-to-text
- pyttsx3 for local text-to-speech

## Testing

Test cases are available in:

```
tests/test_cases.md
```

They cover:

- Budget-first qualification
- Higher-budget configuration recommendation
- Unknown information
- Customer objections
- Follow-up requests
- Site-visit booking
- Booking failure
- Hindi/Hinglish interaction
