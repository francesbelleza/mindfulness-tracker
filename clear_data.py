"""
Clear all database data except users
Run this script to reset check-ins, practices, journal entries, and feedback
"""
from app import create_app, db
from app.models import CheckIn, Practice, JournalEntry, PracticeFeedback

app = create_app()

with app.app_context():
    print("Clearing database data (keeping users)...")

    # Delete in correct order due to foreign key constraints
    deleted_feedback = PracticeFeedback.query.delete()
    print(f"✓ Deleted {deleted_feedback} feedback entries")

    deleted_journals = JournalEntry.query.delete()
    print(f"✓ Deleted {deleted_journals} journal entries")

    deleted_practices = Practice.query.delete()
    print(f"✓ Deleted {deleted_practices} practices")

    deleted_checkins = CheckIn.query.delete()
    print(f"✓ Deleted {deleted_checkins} check-ins")

    # Commit the changes
    db.session.commit()
    print("\n✅ Database cleared successfully! Users remain intact.")
