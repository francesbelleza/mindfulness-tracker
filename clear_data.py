"""
Clear all database data except users
Run this script to reset check-ins, practices, journal entries, and feedback
Optionally delete audio files from Supabase Storage
"""
import os
from app import create_app, db
from app.models import CheckIn, Practice, JournalEntry, PracticeFeedback
from supabase import create_client

app = create_app()

def delete_audio_files_from_supabase():
    """Delete all audio files from Supabase Storage"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            print("⚠ Supabase credentials not found. Skipping audio deletion from cloud.")
            return 0

        # Get all practices to find audio files
        practices = Practice.query.all()
        audio_files = [p.audio_file for p in practices if p.audio_file]

        if not audio_files:
            print("No audio files to delete from Supabase.")
            return 0

        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)

        # Delete each audio file from Supabase Storage
        deleted_count = 0
        for audio_url in audio_files:
            try:
                # Extract filename from URL
                # URL format: https://.../meditation-audio/practice_123.mp3
                filename = audio_url.split('/')[-1]

                # Delete from storage
                supabase.storage.from_('meditation-audio').remove([filename])
                deleted_count += 1
                print(f"  ✓ Deleted {filename} from Supabase Storage")
            except Exception as e:
                print(f"  ⚠ Failed to delete {audio_url}: {e}")

        return deleted_count

    except Exception as e:
        print(f"⚠ Error deleting audio files from Supabase: {e}")
        return 0

with app.app_context():
    print("="*80)
    print("MINDFULNESS TRACKER - DATA CLEANUP UTILITY")
    print("="*80)
    print("\nThis will clear all check-ins, journal entries, and feedback.")
    print("Users will remain intact.")
    print()

    # Ask about practices and audio
    clear_practices = input("Do you want to also clear practices and delete audio files? (y/n): ").strip().lower()

    if clear_practices == 'y':
        print("\n⚠ WARNING: This will delete all practices AND their audio files from Supabase Storage.")
        confirm = input("Are you sure? Type 'yes' to confirm: ").strip().lower()

        if confirm != 'yes':
            print("\n❌ Operation cancelled.")
            exit(0)

        print("\nClearing database data...")

        # Delete in correct order due to foreign key constraints
        deleted_feedback = PracticeFeedback.query.delete()
        print(f"✓ Deleted {deleted_feedback} feedback entries")

        deleted_journals = JournalEntry.query.delete()
        print(f"✓ Deleted {deleted_journals} journal entries")

        # Delete audio files from Supabase before deleting practices
        print("\nDeleting audio files from Supabase Storage...")
        deleted_audio = delete_audio_files_from_supabase()
        print(f"✓ Deleted {deleted_audio} audio files from Supabase")

        deleted_practices = Practice.query.delete()
        print(f"✓ Deleted {deleted_practices} practices from database")

        deleted_checkins = CheckIn.query.delete()
        print(f"✓ Deleted {deleted_checkins} check-ins")

        # Commit the changes
        db.session.commit()
        print("\n✅ Database and audio files cleared successfully! Users remain intact.")

    else:
        print("\n❌ Operation cancelled.")
        print("\nNote: Practices and check-ins are linked by foreign keys.")
        print("To clear check-ins, you must also delete practices (choose 'y' next time).")
        print("Users and all data remain intact.")
