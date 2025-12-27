import os
import json
from openai import OpenAI

def generate_practice_and_prompt(mood, body_feeling=None):
    """
    Generate personalized mindfulness practice and journal prompt using OpenAI.

    Args:
        mood (str): User's current mood (Happy, Calm, Anxious, Sad)
        body_feeling (str, optional): User's body sensations

    Returns:
        dict: Contains 'practice' (dict with title, description, type) and 'journal_prompt' (str)
        None: If API call fails
    """

    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment variables")
        return None

    client = OpenAI(api_key=api_key)

    # Build the user message with mood and optional body feeling
    user_message = f"User's mood: {mood}"
    if body_feeling:
        user_message += f"\nBody feeling: {body_feeling}"

    # System prompt for the AI
    system_prompt = """You are a compassionate mindful wellness coach. Based on the user's mood and body sensations, suggest:
1. A short mindfulness practice (2-3 minutes) that is specific and actionable
2. A thoughtful journal prompt for reflection

Respond ONLY with valid JSON in this exact format:
{
  "practice": {
    "title": "Practice name (concise, under 50 characters)",
    "description": "Step-by-step instructions (clear, numbered steps if applicable, 100-200 words)",
    "type": "breathing|meditation|movement|grounding"
  },
  "journal_prompt": "A thoughtful question or reflection prompt (1-2 sentences)"
}

Guidelines:
- For anxious/stressed moods: Focus on grounding, breathing exercises, calming techniques
- For sad/low moods: Focus on compassion, gentle movement, self-kindness
- For happy/content moods: Focus on gratitude, energizing practices, appreciation
- For calm moods: Focus on body awareness, mindfulness, meditation
- Keep practices simple and accessible (no equipment needed)
- Make journal prompts introspective but not overwhelming"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=400,
            temperature=0.7
        )

        # Parse the response
        ai_response = response.choices[0].message.content.strip()

        # Parse JSON response
        result = json.loads(ai_response)

        # Validate response structure
        if not _validate_response(result):
            print("ERROR: AI response validation failed")
            print(f"Response: {ai_response}")
            return None

        return result

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse AI response as JSON: {e}")
        print(f"Response: {ai_response}")
        return None

    except Exception as e:
        print(f"ERROR: OpenAI API call failed: {e}")
        return None


def _validate_response(result):
    """
    Validate that AI response has the correct structure.

    Args:
        result (dict): Parsed JSON response from AI

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Check top-level keys
        if 'practice' not in result or 'journal_prompt' not in result:
            return False

        # Check practice structure
        practice = result['practice']
        required_practice_keys = ['title', 'description', 'type']
        if not all(key in practice for key in required_practice_keys):
            return False

        # Check that values are non-empty strings
        if not all(isinstance(practice[key], str) and practice[key].strip() for key in required_practice_keys):
            return False

        # Check journal_prompt is a non-empty string
        if not isinstance(result['journal_prompt'], str) or not result['journal_prompt'].strip():
            return False

        # Check practice type is valid
        valid_types = ['breathing', 'meditation', 'movement', 'grounding']
        if practice['type'] not in valid_types:
            return False

        return True

    except Exception:
        return False


def get_fallback_content(mood):
    """
    Provide fallback practice and prompt if AI fails.

    Args:
        mood (str): User's current mood

    Returns:
        dict: Fallback practice and journal prompt
    """

    fallback_map = {
        'Happy': {
            'practice': {
                'title': 'Gratitude Breathing',
                'description': '1. Find a comfortable seated position.\n2. Take a deep breath in, thinking of one thing you\'re grateful for.\n3. As you exhale, let a smile naturally form.\n4. Repeat for 5-7 breaths, bringing to mind different things you appreciate.\n5. Notice the warmth of gratitude in your body.',
                'type': 'breathing'
            },
            'journal_prompt': 'What brought you joy today, and how did it feel in your body?'
        },
        'Calm': {
            'practice': {
                'title': 'Body Scan Meditation',
                'description': '1. Sit or lie down comfortably.\n2. Close your eyes and take three deep breaths.\n3. Bring your attention to your feet, noticing any sensations.\n4. Slowly move your awareness up through your legs, torso, arms, and head.\n5. Spend 10-15 seconds on each area, simply observing without judgment.\n6. End by taking three more deep breaths.',
                'type': 'meditation'
            },
            'journal_prompt': 'What does peace feel like in your body right now?'
        },
        'Anxious': {
            'practice': {
                'title': '4-7-8 Calming Breath',
                'description': '1. Sit comfortably with your back straight.\n2. Exhale completely through your mouth.\n3. Inhale through your nose for 4 counts.\n4. Hold your breath for 7 counts.\n5. Exhale through your mouth for 8 counts.\n6. Repeat this cycle 3-4 times.\n7. Return to normal breathing and notice how you feel.',
                'type': 'breathing'
            },
            'journal_prompt': 'What do you need to feel safe and grounded right now?'
        },
        'Sad': {
            'practice': {
                'title': 'Self-Compassion Hand on Heart',
                'description': '1. Place one or both hands over your heart.\n2. Feel the warmth and gentle pressure of your hands.\n3. Take slow, deep breaths.\n4. Silently say: "May I be kind to myself. May I accept myself as I am."\n5. Continue for 2-3 minutes, breathing gently.\n6. Notice any shift in how you feel.',
                'type': 'meditation'
            },
            'journal_prompt': 'What would you say to comfort a dear friend who felt this way?'
        }
    }

    # Return mood-specific fallback, or default to Calm if mood not found
    return fallback_map.get(mood, fallback_map['Calm'])
