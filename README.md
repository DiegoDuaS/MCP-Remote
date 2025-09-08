# Guess Number MCP Server (Remote)

This project implements a remote MCP (Model Context Protocol) server for a simple number guessing game. The server is deployed on Google Cloud Run and allows a client chatbot to interact with it using JSON requests.

The server tracks game state per user and keeps a log of conversations.

## Project Structure
```
│── server/
│   └── mcp_server.py     # FastAPI server for the guessing game
│── requirements.txt      # Python dependencies
│── Dockerfile            # Container configuration for Cloud Run
```

## Configuration

1. Clone the repository:

```bash
git clone [<your-repo-url>](https://github.com/DiegoDuaS/MCP-Remote)
cd MCP-Remote
``` 
2. Install dependencies (for local testing):

```bash
pip install -r requirements.txt
```

### Running Locally

1. To run the server locally on port 8080:
```bash
python server/mcp_server.py
```

2. Access the endpoint at:

POST http://127.0.0.1:8080/guess

- JSON body format:

```
{
  "user_id": "default_user",
  "message": "start"
}
```

### Deploying to Google Cloud Run

1. Build the Docker image:

```bash
gcloud builds submit --tag gcr.io/<PROJECT_ID>/guess-game
```

2. Deploy to Cloud Run:

```bash
gcloud run deploy guess-game \
  --image gcr.io/<PROJECT_ID>/guess-game \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```


The server will be available at:

https://<SERVICE_NAME>-<PROJECT_NUMBER>.us-central1.run.app/guess
