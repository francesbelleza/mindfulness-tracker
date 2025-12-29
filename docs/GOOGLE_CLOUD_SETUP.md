# Google Cloud Text-to-Speech Setup Guide

## {NOT USED ANYMORE SWITCHED BACK TO ELEVEN LABS}
## Quick Setup Steps

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Note your Project ID

### 2. Enable the Text-to-Speech API
1. Go to [Text-to-Speech API page](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
2. Click "Enable API"

### 3. Create Service Account Credentials
1. Go to [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click "Create Service Account"
3. Name it: `recalibrate-tts` (or any name you prefer)
4. Grant role: **Text-to-Speech User** (or Editor for full access)
5. Click "Create and Continue"
6. Click "Done"

### 4. Download the Credentials JSON
1. Click on your newly created service account
2. Go to the "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" format
5. Click "Create"
6. Save the downloaded JSON file to your project directory as `google-credentials.json`

### 5. Set Environment Variable

**Option A: Using .env file (Recommended for development)**
Add to your `.env` file:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/your/google-credentials.json
```

**Option B: Export in terminal**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/your/google-credentials.json"
```

### 6. Add credentials file to .gitignore
Make sure `google-credentials.json` is in your `.gitignore`:
```
google-credentials.json
```

## Pricing

Google Cloud TTS is **much cheaper** than ElevenLabs:

- **WaveNet voices**: $16 per 1 million characters
- **Free tier**: 1 million characters per month for WaveNet voices

For reference:
- A typical 500-character practice costs $0.008 (less than 1 cent)
- 1000 practices = ~$8 with WaveNet voices
- **vs ElevenLabs**: Same would cost hundreds of dollars

## Testing

Test the setup:
```bash
source venv/bin/activate
python -c "from app.ai_service import generate_audio; print(generate_audio('Test audio', 1000, 'Calm'))"
```

If successful, you'll see: `✓ Audio generated: practice_1000.mp3`

## Troubleshooting

### Error: "Could not automatically determine credentials"
- Make sure `GOOGLE_APPLICATION_CREDENTIALS` is set correctly
- Verify the path to your JSON file is absolute (not relative)
- Try restarting your terminal/IDE after setting the variable

### Error: "Permission denied"
- Make sure the service account has "Text-to-Speech User" role
- Try using "Editor" role if issues persist

### Error: "API not enabled"
- Go to the Text-to-Speech API page and click "Enable"
- Wait a few minutes for the API to activate

## Production Deployment

For production (e.g., Render, Heroku):
1. Copy the entire contents of your `google-credentials.json`
2. Add as an environment variable named `GOOGLE_CREDENTIALS_JSON`
3. In your app initialization, write this to a file:
```python
import json
import os

# In production, write credentials from env var to file
if os.getenv('GOOGLE_CREDENTIALS_JSON'):
    creds = json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON'))
    with open('google-credentials.json', 'w') as f:
        json.dump(creds, f)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
```
