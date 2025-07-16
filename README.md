Reddit User Persona Generator (Gemini API)
This project generates a detailed user persona for any public Reddit user by analyzing their comments and posts. It uses the Google Gemini API for generating insights and summaries.
🔧 Features
Fetches Reddit user posts and comments using praw.
Cleans and compiles text content into a single data block for analysis.
Uses the Google Gemini API to generate a detailed persona based on a professional template.
Cites every inferred trait with a direct link back to the source post or comment.
Accepts both plain usernames and full Reddit profile URLs as input.
Securely manages API keys using a .env file.
🛠️ Setup & Installation
Clone the repository:
git clone https://github.com/YourUsername/your-repo-name.git
cd your-repo-name


Create a virtual environment (recommended):
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate


Install dependencies:
pip install -r requirements.txt


Add API Keys:
Create a .env file in the root directory and add your keys from Reddit and Google AI Studio.
# .env file
REDDIT_CLIENT_ID="YOUR_REDDIT_CLIENT_ID_HERE"
REDDIT_CLIENT_SECRET="YOUR_REDDIT_CLIENT_SECRET_HERE"
REDDIT_USER_AGENT="PersonaGenerator/1.0 by YourUsername"
GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY_HERE"


▶️ How to Run
Execute the script from the command line, providing a Reddit username or profile URL as an argument.
Command:
python persona_generator.py <username_or_url>


Examples:
# Provide a username
python persona_generator.py kojied

# Provide a full URL
python persona_generator.py https://www.reddit.com/user/Hungry-Move-6603/


The generated persona will be saved in the output/ directory.
