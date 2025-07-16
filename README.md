Reddit User Persona Generator
This script analyzes a Reddit user's recent activity (posts and comments) to generate a detailed user persona using the Google Gemini large language model. It scrapes data via the Reddit API, processes it, and outputs a structured persona that includes inferred demographics, personality traits, motivations, and more, with each point cited by the source comment or post.

This project was developed as part of the AI/LLM Engineer Intern assignment for BeyondChats.

Features
Dynamic Scraping: Fetches recent comments and posts for any given Reddit user.

AI-Powered Analysis: Leverages Google's Gemini model to create a nuanced and structured user persona based on a professional template.

Source Citations: Every inferred trait in the persona is backed by a citation linking to the original post or comment, ensuring verifiability.

Robust Input Handling: Accepts both plain usernames (e.g., kojied) and full profile URLs.

Secure API Key Management: Uses a .env file to keep credentials safe and out of the source code.

Project Structure
reddit-persona-generator/
├── output/
│   ├── kojied_persona.txt
│   └── ...
├── .env
├── .gitignore
├── persona_generator.py
├── README.md
└── requirements.txt

Setup and Installation
Follow these steps to get the project running on your local machine.

1. Clone the Repository
git clone https://github.com/YourUsername/your-repo-name.git
cd your-repo-name

(Replace YourUsername/your-repo-name with your actual repository path)

2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts.

On Windows:

python -m venv venv
venv\Scripts\activate

On macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Install the required Python libraries using the requirements.txt file.

pip install -r requirements.txt

4. Configure API Keys
The script requires API keys for both Reddit and Google.

Reddit: Create a "script" type application on your Reddit Apps page to get your client ID and client secret.

Google Gemini: Obtain your API key from Google AI Studio.

Create a file named .env in the project's root directory. Copy and paste the following, replacing the placeholder text with your actual credentials.

# .env file
REDDIT_CLIENT_ID="YOUR_REDDIT_CLIENT_ID_HERE"
REDDIT_CLIENT_SECRET="YOUR_REDDIT_CLIENT_SECRET_HERE"
REDDIT_USER_AGENT="PersonaGenerator/1.0 by YourUsername"
GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY_HERE"

How to Run
Execute the script from your terminal. The generated persona will be saved as a .txt file in the output/ directory.

Command
python persona_generator.py <username_or_url>

Examples
Using a plain username:

python persona_generator.py kojied

Using a full profile URL:

python persona_generator.py https://www.reddit.com/user/Hungry-Move-6603/

The script will print its progress to the console and notify you when the persona file has been successfully created.