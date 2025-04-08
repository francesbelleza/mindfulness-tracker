# database schema

## 1. `user_checkins` (mood log)
Stores each check-in where a user selects a mood and gets a recommended practice.

| Column Name         | Type                  | Description |
|---------------------|-----------------------|-------------|
| id                  | Integer (Primary Key) | Unique identifier for each check-in |
| user_id             | Integer (Foreign Key) | Identifies the user (if we add accounts later) |
| mood                | String                | Mood selected (`Happy`, `Calm`, `Anxious`, `Sad`) |
| exercise_id         | Integer (Foreign Key) | Links to a suggested yoga, breathing, or meditation exercise |
| journal_prompt_id   | Integer (Foreign Key) | Links to a suggested journal prompt |
| timestamp           | DateTime              | When the user checked in |

### example data in `user_checkins`
| id | user_id | mood     | exercise_id | journal_prompt_id | timestamp           |
|----|---------|----------|-------------|--------------------|---------------------|
| 1  | 101     | Happy    | 5           | 3                  | 2024-03-05 08:15:00 |
| 2  | 101     | Anxious  | 2           | 8                  | 2024-03-06 12:30:00 |
| 3  | 102     | Sad      | 7           | 1                  | 2024-03-07 21:10:00 |

---

## 2. `mindfulness_practices` (yoga, breathing, & meditations)
Stores all mindfulness exercises (yoga, breathing, meditations) that users can receive.

| Column Name   | Type                  | Description |
|---------------|-----------------------|-------------|
| id            | Integer (Primary Key) | Unique identifier for each practice |
| category      | String                | Type of practice (`Yoga`, `Breathing`, `Meditation`) |
| name          | String                | Name of the exercise (e.g., “Tree Pose”, “Box Breathing”) |
| description   | Text                  | Instructions for the practice |

### example data
| id | category   | name            | description              |
|----|------------|-----------------|--------------------------|
| 1  | Yoga       | Tree Pose       | Stand tall, balance on…  |
| 2  | Breathing  | Box Breathing   | Inhale 4 sec, hold 4 sec…|
| 3  | Meditation | Loving-Kindness | Close your eyes, send…   |

---

## 3. `journal_entries` (user reflections & gratitude)
Stores user-written responses to journal prompts and gratitude reflections.

| Column Name   | Type                  | Description |
|---------------|-----------------------|-------------|
| id            | Integer (Primary Key) | Unique ID for each entry |
| user_id       | Integer (Foreign Key) | Identifies the user |
| checkin_id    | Integer (Foreign Key) | Links to the mood check-in |
| prompt_id     | Integer (Foreign Key) | Links to the journal prompt |
| response      | Text                  | The user’s written reflection |
| timestamp     | DateTime              | When the user wrote the entry |

---

## 4. `journal_prompts` (reflection & gratitude prompts)
Stores all pre-written journal prompts, including gratitude prompts.

| Column Name   | Type                  | Description |
|---------------|-----------------------|-------------|
| id            | Integer (Primary Key) | Unique identifier for each prompt |
| category      | String                | Type (`Reflection`, `Gratitude`) |
| text          | Text                  | The journal prompt text |

### example data
| id | category   | text                                 |
|----|------------|--------------------------------------|
| 1  | Reflection | What made you smile today?           |
| 2  | Gratitude  | List three things you're grateful for.|

---

## 5. `users` (optional for future)
If we later add user accounts, this table will store user profiles.

| Column Name | Type                  | Description |
|--------------|-----------------------|-------------|
| id           | Integer (Primary Key) | Unique user ID |
| username     | String                | User's name |
| password     | String                | Encrypted password (if login is needed) |
| email        | String                | User’s email (optional) |

---

## relationships between tables

- `user_checkins` links to:
  - `mindfulness_practices` (suggested yoga/breathing/meditation)
  - `journal_prompts` (suggested prompt)
  - `journal_entries` (if the user writes a reflection)

- `journal_entries` links to:
  - `journal_prompts` (to show what the prompt was)
  - `user_checkins` (to match the reflection to a mood check-in)

---

## templates list (required html files)

- index.html – home screen
- signup.html – sign up form
- login.html – login form
- check_in.html – mood check-in form
- already_checked_in.html – message when user already checked in
- practice.html – ai-powered suggestion (practice + journal prompt)
- reflect.html – journal entry form
- feedback.html – emoji/rating form
- thank_you.html – completion/affirmation screen
