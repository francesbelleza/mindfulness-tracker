import os
import json
from pathlib import Path
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import save

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
    system_prompt = """You are a compassionate mindfulness meditation teacher. Based on the user's mood and body sensations, create:
1. A guided mindfulness practice (2-4 minutes) with clear, spoken-style instructions
2. A thoughtful journal prompt for reflection

IMPORTANT: Write the practice description as if you're speaking directly to the user in a calm, guiding voice. Use "you" language and present tense. Make it sound like guided meditation audio that will be read aloud with natural pauses.

CRITICAL PAUSE INSTRUCTIONS - VERY IMPORTANT:
- Use THREE ellipses (...) for long 3-5 second meditative pauses for breathing (e.g., "Close your eyes... ... ... Take a deep breath")
- Use TWO ellipses (... ...) for medium 2-3 second pauses (e.g., "Notice your breath... ... Feel the rise and fall")
- Use ONE ellipsis (...) for brief 1-2 second pauses (e.g., "Breathe in... and breathe out")
- Use commas ONLY within the same sentence, not for pauses between instructions
- Add MANY pauses - meditation should feel spacious, not rushed
- Example: "Find a comfortable position... ... ... When you're ready... ... gently close your eyes... ... ... Take a deep, slow breath in... ... ... and exhale fully... ... ... Notice the sensation of your breath... ... ... Continue breathing naturally... ... ..."

Respond ONLY with valid JSON in this exact format:
{
  "practice": {
    "title": "Practice name (concise, under 50 characters)",
    "description": "Voice-guided instructions with natural pauses using ellipses and punctuation (150-250 words, very slow meditative pacing)",
    "type": "breathing|meditation|movement|grounding"
  },
  "journal_prompt": "A thoughtful question or reflection prompt (1-2 sentences)"
}

Guidelines:
- ALWAYS incorporate their body feelings into the practice if provided
- Use calm, soothing language with strategic pauses throughout
- Example: "Gently close your eyes... Notice the sensation of..." NOT "1. Close eyes 2. Notice..."
- For anxious moods + tense body: Focus on releasing tension, progressive relaxation with longer pauses
- For sad moods + heavy/tired body: Focus on gentle compassion, soft breathing with nurturing pauses
- For happy moods: Enhance and savor positive sensations with appreciative pauses
- For calm moods: Deepen present-moment awareness with spacious pauses
- Practices should be STRICTLY mindfulness-based (breathing, body scans, awareness, meditation)
- NO exercise, yoga poses, or physical activities - only gentle awareness practices
- Keep it simple and accessible (seated or lying down)
- Use ellipses generously to create meditative breathing space"""

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
                'description': 'Find a comfortable place to sit... When you\'re ready, gently close your eyes... Take a deep breath in through your nose... and as you do, bring to mind one thing you\'re grateful for today... As you exhale slowly, let a gentle smile form on your face... Feel the warmth of gratitude spreading through your chest... Take another breath in... thinking of something else you appreciate... With each exhale, notice how gratitude feels in your body... Continue this for five to seven breaths... savoring each moment of appreciation... When you\'re ready... slowly open your eyes... carrying this gratitude with you.',
                'type': 'breathing'
            },
            'journal_prompt': 'What brought you joy today, and where did you feel it in your body?'
        },
        'Calm': {
            'practice': {
                'title': 'Body Scan Meditation',
                'description': 'Settle into a comfortable position... either sitting or lying down... Gently close your eyes... and take three slow, deep breaths... Now, bring your awareness to your feet... Notice any sensations there... warmth, coolness, tingling... or perhaps nothing at all... There\'s no right or wrong... Slowly move your attention up to your ankles... then your calves... Take your time with each area... Continue scanning upward through your legs... your hips... your abdomen... Notice your chest rising and falling with each breath... Bring awareness to your shoulders... your arms... your hands... Finally, notice sensations in your neck... your face... the top of your head... Take three more deep breaths... feeling your whole body present and relaxed.',
                'type': 'meditation'
            },
            'journal_prompt': 'What does peace feel like in your body right now?'
        },
        'Anxious': {
            'practice': {
                'title': '4-7-8 Calming Breath',
                'description': 'Find a comfortable seated position... and rest your hands gently in your lap... Let\'s begin by exhaling completely through your mouth... making a soft whoosh sound... Now, close your mouth... and inhale quietly through your nose for a count of four... one, two, three, four... Hold your breath gently for seven counts... one, two, three, four, five, six, seven... Now exhale completely through your mouth for eight counts... one, two, three, four, five, six, seven, eight... This completes one cycle... Continue this rhythm for three more cycles... allowing each breath to calm your nervous system... Notice how your body begins to relax with each exhale... When you\'re done... return to your natural breathing... and notice how you feel.',
                'type': 'breathing'
            },
            'journal_prompt': 'What do you need to feel safe and grounded right now?'
        },
        'Sad': {
            'practice': {
                'title': 'Self-Compassion Practice',
                'description': 'Gently place one or both hands over your heart... Feel the warmth and gentle pressure of your hands resting there... Take a slow, deep breath in... and as you exhale, let your shoulders soften... With each breath... notice the rise and fall of your chest beneath your hands... Silently, with kindness, say to yourself... "May I be kind to myself in this moment... May I accept myself just as I am..."... Continue breathing slowly... feeling your hands over your heart... If it feels right... you might say... "May I give myself the compassion I need..."... Stay here for a few minutes... breathing gently... holding yourself with care... Notice any shifts, however subtle, in how you feel... You are worthy of this kindness.',
                'type': 'meditation'
            },
            'journal_prompt': 'What would you say to comfort a dear friend who felt this way?'
        }
    }

    # Return mood-specific fallback, or default to Calm if mood not found
    return fallback_map.get(mood, fallback_map['Calm'])


def generate_audio(practice_text, practice_id, mood):
    """
    Generate natural-sounding audio for a practice using ElevenLabs TTS.
    Uses a single calm, meditative voice for all moods.

    Args:
        practice_text (str): The practice description text
        practice_id (int): The practice ID for filename
        mood (str): User's mood (not used for voice selection, kept for compatibility)

    Returns:
        str: Filename of the generated audio, or None if failed
    """
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY not found")
        return None

    # Use single meditative voice for all moods
    # Lily: Velvety Actress - calm, soothing, perfect for meditation
    voice_id = 'pFZP5JQG7iQjIQuC4Bku'  # Lily
    voice_name = 'Lily'

    try:
        # Create audio directory if it doesn't exist
        audio_dir = Path("app/static/audio")
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Generate audio filename
        audio_filename = f"practice_{practice_id}.mp3"
        audio_path = audio_dir / audio_filename

        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=api_key)

        # Generate audio with ElevenLabs TTS (returns a generator)
        # Using higher stability, lower similarity, and slower speed for meditative voice
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            text=practice_text,
            model_id="eleven_multilingual_v2",  # High-quality model with natural prosody
            voice_settings={
                "stability": 0.75,  # Higher stability = more consistent, calmer delivery
                "similarity_boost": 0.5,  # Lower boost = softer, less harsh voice
                "speed": 0.85  # Slower speed for more meditative pacing
            }
        )

        # Save the audio file (save() handles the generator)
        save(audio_generator, str(audio_path))

        print(f"✓ Audio generated: {audio_filename} (Voice: {voice_name} - calm meditative voice)")
        return audio_filename

    except Exception as e:
        print(f"ERROR: Failed to generate audio with ElevenLabs: {e}")
        return None
