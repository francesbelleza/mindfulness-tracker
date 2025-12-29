import os
import json
import re
from pathlib import Path
from openai import OpenAI
from supabase import create_client, Client

# ElevenLabs TTS
from elevenlabs import ElevenLabs, VoiceSettings

def generate_practice_and_prompt(mood, body_feeling=None, time_of_day=None):
    """
    Generate personalized mindfulness practice and journal prompt using OpenAI.

    Args:
        mood (str): User's current mood (Happy, Calm, Anxious, Sad, Angry)
        body_feeling (str, optional): User's body sensations
        time_of_day (str, optional): When checking in (Morning or Night)

    Returns:
        dict: Contains 'practice' (dict with title, description, type) and 'journal_prompt' (str)
        None: If API call fails
    """

    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment variables")
        print("Please check your .env file")
        return None

    print(f"OpenAI API Key found: {api_key[:20]}...{api_key[-4:]}")  # Show partial key for debugging

    try:
        client = OpenAI(api_key=api_key)
        print("✓ OpenAI client initialized successfully")
    except Exception as e:
        print(f"ERROR: Failed to initialize OpenAI client: {e}")
        return None

    # Build the user message with mood, body feeling, and time of day
    user_message = f"User's mood: {mood}"
    if body_feeling:
        user_message += f"\nBody feeling: {body_feeling}"
    if time_of_day:
        user_message += f"\nTime of day: {time_of_day}"

    # System prompt for the AI
    system_prompt = """You are a compassionate mindfulness meditation teacher. Based on the user's mood, body sensations, and time of day, create:
1. A guided mindfulness practice (1 minute when spoken aloud, occasionally 1.5 minutes if absolutely necessary) with clear, spoken-style instructions
2. A thoughtful journal prompt for reflection

CRITICAL LENGTH REQUIREMENT: Keep meditations at EXACTLY 1 minute (80-120 words). Only extend to 1.5 minutes (up to 175 words) if the user's mood/situation absolutely requires more guidance. Default to 1 minute.

IMPORTANT: Write the practice description as if you're speaking directly to the user in a calm, guiding voice. Use "you" language and present tense. Write in complete, natural sentences with commas for flow.

NOTE: The user will also receive additional structured questions based on time of day:
- Morning: "What is your intention for the day?"
- Night: "What is one thing you did for yourself today?" and "What is one thing you'd like to accomplish tomorrow?"
So your journal prompt should complement (not duplicate) these questions. Focus on emotional reflection or deeper insights related to their mood and body sensations.

TIME OF DAY GUIDANCE:
- MORNING practices: Create energizing, grounding practices to start the day with intention. Focus on awakening the body gently, setting intentions, energizing breath work, or morning gratitude. Help them transition into their day with clarity and purpose.
- NIGHT practices: Create calming, reflective practices to wind down. Focus on releasing the day's tension, restorative breathing, body relaxation, or gentle self-compassion. Help them prepare for restful sleep and let go of the day.
- If no time specified, create a balanced practice suitable for any time.

CRITICAL PAUSE INSTRUCTIONS - USE PAUSES STRATEGICALLY:
Write in complete, flowing sentences with commas for natural speech rhythm. Use ellipses ONLY for intentional meditative pauses.

- Use COMMAS for natural speech flow (~0.2s pause, handled automatically):
  - "Find a comfortable position, either seated or lying down"
  - "Take a deep breath in, and slowly exhale"

- Use ... (single ellipsis) for BRIEF pauses (~0.3s):
  - End of complete phrases before moving to next instruction
  - After breathing cues: "exhale through your mouth... feeling your shoulders relax"

- Use ... ... (double ellipses) for MEDIUM pauses (~0.8s):
  - Between distinct instructions
  - Natural meditation pacing: "Notice the rhythm of your breath... ... Now bring attention to your body"

- Use ... ... ... (triple ellipses) for LONG pauses (~1.2s):
  - Major section transitions
  - Before/after breathing instructions
  - After key meditative moments

- For silent breathing rounds, use 6-8 sets of triple ellipses (creates ~7-10 second breathing space)

GOOD EXAMPLE (natural flow with strategic pauses):
"Find a comfortable seated position, whether sitting or lying down... ... ... When you're ready, gently close your eyes... ... ... Take a full breath in through your nose... ... and as you exhale slowly, allow your shoulders to soften and drop... ... ... Notice the natural rhythm of your breath, the gentle rise and fall of your chest... ... ... Simply observe for a few moments... ... ... ... ... ... ... ... ... ... ... Now bring your attention to the sensation of your feet on the ground, feeling supported and grounded... ... ... When you're ready, slowly open your eyes."

BAD EXAMPLE (too many pauses, robotic):
"Find a comfortable position... ... ... whether seated... ... ... or lying down... ... ... Allow your eyes... ... ... to gently close... ... ..."

Respond ONLY with valid JSON in this exact format:
{
  "practice": {
    "title": "Practice name (concise, under 50 characters)",
    "description": "Voice-guided instructions with natural sentence flow and strategic pauses (80-120 words for 1 minute, up to 175 words only if absolutely necessary)",
    "type": "breathing|meditation|movement|grounding"
  },
  "journal_prompt": "A thoughtful question or reflection prompt (1-2 sentences)"
}

CRITICAL: The "type" field MUST be EXACTLY one of these four words: breathing, meditation, movement, grounding
DO NOT use any other values like "mindfulness", "reflection", etc.

Guidelines:
- ALWAYS incorporate their body feelings into the practice if provided
- Write in complete sentences with natural commas for flow
- Use pauses strategically at transitions and breathing moments, NOT after every phrase
- For anxious moods + tense body: Focus on releasing tension, progressive relaxation
- For sad moods + heavy/tired body: Focus on gentle compassion, soft breathing
- For happy moods: Enhance and savor positive sensations
- For calm moods: Deepen present-moment awareness
- Practices should be STRICTLY mindfulness-based (breathing, body scans, awareness, meditation)
- NO exercise, yoga poses, or physical activities - only gentle awareness practices
- Keep it simple and accessible (seated or lying down)
- Target 1 minute spoken aloud (80-120 words), extend to 1.5 minutes (up to 175 words) only if absolutely necessary"""

    try:
        # Try GPT-4o first (optimized, high quality meditation scripts)
        try:
            print("Attempting GPT-4o API call...")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=600,  # Increased for longer, more detailed practices
                temperature=0.7
            )
            print("✓ GPT-4o API call successful")
        except Exception as gpt4_error:
            # If GPT-4o fails (access denied, not available, etc.), fall back to GPT-3.5-turbo
            print(f"GPT-4o failed: {gpt4_error}")
            print("Falling back to GPT-3.5-turbo...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=600,
                temperature=0.7
            )
            print("✓ GPT-3.5-turbo API call successful")

        # Parse the response
        ai_response = response.choices[0].message.content.strip()
        print(f"AI Response received: {ai_response[:100]}...")  # Print first 100 chars

        # Strip markdown code blocks if present (GPT-4 sometimes wraps JSON in ```json...```)
        if ai_response.startswith('```'):
            # Remove opening ```json or ```
            ai_response = ai_response.split('\n', 1)[1] if '\n' in ai_response else ai_response[3:]
            # Remove closing ```
            if ai_response.endswith('```'):
                ai_response = ai_response.rsplit('```', 1)[0]
            ai_response = ai_response.strip()
            print("Stripped markdown code blocks from response")

        # Parse JSON response
        result = json.loads(ai_response)

        # Validate response structure
        if not _validate_response(result):
            print("ERROR: AI response validation failed")
            print(f"Full response: {ai_response}")
            return None

        print("✓ AI response validated successfully")
        return result

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse AI response as JSON: {e}")
        print(f"Raw response: {ai_response if 'ai_response' in locals() else 'No response'}")
        return None

    except Exception as e:
        print(f"ERROR: OpenAI API call failed completely: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
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


def _convert_pauses_to_ssml(text):
    """
    Convert ellipsis pause notation to SSML break tags for natural meditation pacing.
    Ensures ALL literal dots are removed to prevent model from interpreting them as trailing off.

    Comma = natural speech pause (~0.2s, handled by TTS prosody)
    ... (single) = <break time="0.3s"/> (brief pause at end of phrase)
    ... ... (double) = <break time="0.8s"/> (medium pause between instructions)
    ... ... ... (triple) = <break time="1.2s"/> (long pause for breathing/transitions)
    4+ ellipses = extended breathing pauses (each adds 1.2s, e.g., 6 ellipses = 7.2s)

    Args:
        text (str): Practice text with ellipsis notation

    Returns:
        str: Text with SSML break tags only (no literal dots remaining)
    """
    # Count consecutive triple ellipses for extended breathing pauses
    # Each triple = 1.2s, so multiple triples create longer pauses for breathing rounds
    def replace_multiple_triples(match):
        count = match.group(0).count('...')
        total_time = count * 1.2  # 1.2 seconds per triple
        return f'<break time="{total_time}s"/>'

    # Replace patterns in order from longest to shortest to avoid partial matches
    # This ensures ALL dots are removed and replaced with SSML break tags only

    # First, handle sequences of 4+ ellipses (extended breathing rounds)
    # Each ellipsis adds 1.2s, so 6-8 ellipses = 7.2-9.6s breathing space
    text = re.sub(r'(?:\.{3}\s*){4,}', replace_multiple_triples, text)

    # Then replace exactly 3 ellipses (long pause - 1.2s)
    text = re.sub(r'\.{3}\s*\.{3}\s*\.{3}(?!\s*\.{3})', '<break time="1.2s"/>', text)

    # Replace exactly 2 ellipses (medium pause - 0.8s)
    text = re.sub(r'\.{3}\s*\.{3}(?!\s*\.{3})', '<break time="0.8s"/>', text)

    # Replace single ellipses (brief pause - 0.3s)
    text = re.sub(r'\.{3}', '<break time="0.3s"/>', text)

    # CRITICAL: Clean up any remaining problematic patterns that could cause trailing off
    # Remove any stray dots (4+ consecutive dots that aren't part of ellipses)
    text = re.sub(r'\.{4,}', '', text)

    # Remove spaced dots like ". . ." or ". . . ." that could sneak through
    text = re.sub(r'\.\s+\.\s+\.', '', text)

    # Remove any trailing dots at end of sentences (but keep normal periods)
    text = re.sub(r'\.{2,}\s*$', '.', text, flags=re.MULTILINE)

    # Final safety: ensure no sequences of multiple dots remain anywhere
    text = re.sub(r'\.{2,}', '.', text)

    return text


def generate_audio(practice_text, practice_id, mood):
    """
    Generate natural-sounding audio using ElevenLabs TTS and upload to Supabase Storage.
    Uses Lily (Velvety Actress) with eleven_multilingual_v2 model for calm meditation delivery.
    Settings: Stability 0.85, Style 0, Speed 0.8x for measured, non-dramatic tone.

    Args:
        practice_text (str): The practice description text with ellipsis notation
        practice_id (int): The practice ID for filename
        mood (str): User's mood (for logging)

    Returns:
        str: Public URL of the audio file on Supabase, or None if failed
    """
    try:
        # Get ElevenLabs API key
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            print("ERROR: ELEVENLABS_API_KEY not found in environment variables")
            return None

        # Get Supabase credentials
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        if not supabase_url or not supabase_key:
            print("ERROR: SUPABASE_URL or SUPABASE_KEY not found in environment variables")
            print("Please add these to your .env file. Get the key from Supabase dashboard > Settings > API")
            return None

        # Clean text for natural speech - keep ellipses for longer pauses
        # Replace ellipses with periods for better pause duration
        clean_text = practice_text.replace('...', '...')  # Keep ellipses for natural pauses

        print(f"\n{'='*80}")
        print("ELEVENLABS TTS CALL")
        print(f"{'='*80}")
        print(f"Voice: Lily - Velvety Actress")
        print(f"Model: eleven_multilingual_v2 (latest quality model)")
        print(f"Voice Settings: Stability 0.85, Similarity 0.8, Style 0, Speed 0.8")
        print(f"Text length: {len(clean_text)} characters")
        print(f"Text preview: {clean_text[:200]}...")
        print(f"{'='*80}\n")

        # Initialize ElevenLabs client and generate audio with Lily voice
        client = ElevenLabs(api_key=api_key)

        # Voice settings for calm, measured meditation delivery
        audio_generator = client.text_to_speech.convert(
            text=clean_text,
            voice_id="pFZP5JQG7iQjIQuC4Bku",  # Lily - Velvety Actress
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.85,         # Very high stability = calm, consistent, minimal variation
                similarity_boost=0.8,   # High similarity = clearer, more controlled
                style=0,                # No style = minimal expressiveness, very measured
                use_speaker_boost=True, # Enhances voice clarity
                speed=0.8               # 0.8 = 20% slower (0.25 to 4.0 range)
            )
        )

        # Collect audio bytes
        audio_bytes = b""
        for chunk in audio_generator:
            audio_bytes += chunk

        print(f"✓ Audio generated: {len(audio_bytes)} bytes (Voice: Lily - Velvety Actress @ 0.8x speed)")

        # Upload to Supabase Storage
        filename = f"practice_{practice_id}.mp3"

        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)

        # Upload to 'meditation-audio' bucket
        # Create bucket if it doesn't exist (first time setup)
        try:
            response = supabase.storage.from_('meditation-audio').upload(
                filename,
                audio_bytes,
                file_options={"content-type": "audio/mpeg", "upsert": "true"}
            )
            print(f"✓ Uploaded to Supabase Storage: {filename}")
        except Exception as upload_error:
            print(f"Upload error details: {upload_error}")
            # If bucket doesn't exist, you'll need to create it in Supabase dashboard
            print("NOTE: If bucket doesn't exist, create 'meditation-audio' bucket in Supabase Storage dashboard")
            raise

        # Get public URL
        public_url = supabase.storage.from_('meditation-audio').get_public_url(filename)
        print(f"✓ Public URL: {public_url}")

        return public_url

    except Exception as e:
        print(f"ERROR: Failed to generate/upload audio: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None


