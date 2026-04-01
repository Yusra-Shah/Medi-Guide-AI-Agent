# MediGuide AI (Medical Information Assistant)

A conversational multi-agent AI system that helps users 
understand their symptoms using real-time medical research.
Built with Google Agent Development Kit (ADK) and deployed 
live on Google Cloud Run.

## Live Demo
https://medi-guide-29194331602.europe-west1.run.app

## How It Works

1. User describes their symptoms
2. root_agent greets user and saves symptoms to shared state
3. symptom_researcher queries Wikipedia for related conditions
4. medical_advisor formats a clear, compassionate response
5. Always recommends consulting a real doctor

## Architecture
```
User Input
    ↓
root_agent (medi_greeter)
    ↓
SequentialAgent: medi_workflow
    ├── symptom_researcher → Wikipedia API
    └── medical_advisor → Gemini 2.5 Flash
    ↓
Response to User
```

## Tech Stack

- Google Agent Development Kit (ADK) v1.14.0
- Gemini 2.5 Flash via Vertex AI
- LangChain Community + Wikipedia API
- Google Cloud Run (serverless deployment)
- Docker + Artifact Registry
- Python 3.12

## Setup
```bash
git clone https://github.com/Yusra-Shah/Medi-Guide-AI-Agent
cd Medi-Guide-AI-Agent
cp .env.example .env
# Fill in your project details in .env
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
adk web
```

## Deployment
```bash
uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=europe-west1 \
  --service_name=medi-guide \
  --with_ui \
  .
```

## Screenshots

### Agent greeting and symptom capture
![Greeting](Screenshot%20(1209).png)

### save_symptoms_to_state tool invocation
![Tool Invocation](Screenshot%20(1210).png)

### Wikipedia research in action
![Wikipedia Research](Screenshot%20(1211).png)

### Medical conditions response
![Response](Screenshot%20(1212).png)

## Disclaimer

MediGuide AI is for informational purposes only.
Always consult a qualified healthcare professional 
for medical advice and treatment.

## Author

Yusra Batool
github.com/Yusra-Shah
