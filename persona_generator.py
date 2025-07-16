import os
import argparse
import praw
import google.generativeai as genai
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found. Please set it in the .env file.")
genai.configure(api_key=GOOGLE_API_KEY)

def get_reddit_instance():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not all([client_id, client_secret, user_agent]):
        raise ValueError("Reddit API credentials not found in .env file.")

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

def scrape_user_data(reddit, username, limit=100):
    print(f"Scraping data for user: u/{username}...")
    try:
        redditor = reddit.redditor(username)
        activity_log = []
        base_url = "https://www.reddit.com"

        for comment in redditor.comments.new(limit=limit // 2):
            activity_log.append(
                f"Comment in r/{comment.subreddit.display_name} "
                f"(link: {base_url}{comment.permalink}):\n"
                f"{comment.body}\n---\n"
            )

        for submission in redditor.submissions.new(limit=limit // 2):
            activity_log.append(
                f"Post in r/{submission.subreddit.display_name} "
                f"(link: {base_url}{submission.permalink}):\n"
                f"Title: {submission.title}\n"
                f"Body: {submission.selftext}\n---\n"
            )

        if not activity_log:
            print(f"No recent activity found for u/{username}.")
            return None

        print(f"Found {len(activity_log)} recent activities.")
        return "".join(activity_log)
    except Exception as e:
        print(f"Error scraping u/{username}: {e}")
        return None

def generate_persona(user_data, username):
    print("Generating detailed persona with AI. This may take a moment...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are an expert user persona analyst. Your task is to create a detailed user persona for the Reddit user "u/{username}" based *only* on the provided data. Format your output *exactly* like the structure below, including the markdown headers.

    **CRITICAL INSTRUCTIONS:**
    1.  For EVERY point, inference, or observation you make, you MUST cite the source with the corresponding Reddit link from the data. Format citations like this: `[Source: https://...]`.
    2.  If you cannot find sufficient information for any field or section, you MUST explicitly write "Information not available in provided data." DO NOT INVENT DETAILS.
    3.  For personality sliders, estimate a position on a 0-100 scale. For example, `Introvert (80) <---> (20) Extrovert`.

    **--- START OF PERSONA TEMPLATE ---**

    # User Persona: u/{username}

    ## Profile Summary
    - **Age:** (Infer based on context like university, career, or life events. State the confidence level.)
    - **Occupation:** (Infer from discussions about work, industry, or skills.)
    - **Location:** (Infer from mentions of cities, countries, or local subreddits.)
    - **Status:** (Infer if they mention a partner, family, or being single.)
    - **Archetype:** (e.g., The Creator, The Helper, The Analyst, The Explorer. Choose one that best fits.)

    ---

    ## "I want to..."
    > (Create a representative quote that summarizes one of the user's key goals or frustrations found in the data.)

    ---

    ## Personality (MBTI-Style Inference)
    *(Based on their communication style, topic choices, and interactions)*
    - **Introvert / Extrovert:** `Introvert (...) <---> (...) Extrovert`
    - **Intuition / Sensing:** `Intuition (...) <---> (...) Sensing`
    - **Thinking / Feeling:** `Thinking (...) <---> (...) Feeling`
    - **Perceiving / Judging:** `Perceiving (...) <---> (...) Judging`

    ---

    ## Motivations
    *(Rate each as High, Medium, Low, or N/A based on their posts. Add citations.)*
    - **Convenience:**
    - **Wellness / Health:**
    - **Learning / Knowledge:**
    - **Community / Connection:**
    - **Entertainment:**

    ---

    ## Behaviour & Habits
    *(List specific, observable behaviors as bullet points. Add citations.)*
    -
    -
    -

    ---

    ## Goals & Needs
    *(List the user's explicit or implicit goals. What are they trying to achieve? Add citations.)*
    -
    -
    -

    ---

    ## Frustrations / Pain Points
    *(List challenges, complaints, or problems the user has mentioned. Add citations.)*
    -
    -
    -

    **--- END OF PERSONA TEMPLATE ---**


    **--- USER DATA TO ANALYZE ---**
    {user_data}
    **--- END OF USER DATA ---**

    Generate the persona now, strictly following the template and instructions.
    """

    try:
        response = model.generate_content(prompt)
        print("Detailed persona generated successfully.")
        return response.text
    except Exception as e:
        print(f"Error during persona generation: {e}")
        return "Error: Could not generate persona."

def main():
    parser = argparse.ArgumentParser(
        description="Generate a user persona from a Reddit profile."
    )
    parser.add_argument(
        "username_or_url", type=str, help="The Reddit username or the full URL to their profile."
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Optional: Path to the output text file."
    )
    args = parser.parse_args()

    input_value = args.username_or_url
    output_path = args.output
    
    username = ""
    if "reddit.com/user/" in input_value.lower():
        try:
            parsed_url = urlparse(input_value)
            path_parts = [part for part in parsed_url.path.split('/') if part]
            if path_parts and path_parts[0].lower() == 'user':
                username = path_parts[1]
                print(f"URL detected. Extracted username: u/{username}")
        except Exception as e:
            print(f"Could not parse username from URL: {e}")
            return
    else:
        username = input_value

    if not username:
        print("Invalid username or URL provided.")
        return

    if not output_path:
        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", f"{username}_persona.txt")

    reddit = get_reddit_instance()

    scraped_data = scrape_user_data(reddit, username, limit=100)
    if not scraped_data:
        return

    persona = generate_persona(scraped_data, username)
    if not persona:
        return

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(persona)
        print(f"Persona for u/{username} saved to: {output_path}")
    except IOError as e:
        print(f"Error writing to file {output_path}: {e}")

if __name__ == "__main__":
    main()