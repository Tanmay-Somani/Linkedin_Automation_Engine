import os
import sqlite3
from dotenv import load_dotenv
from lib.db_manager import init_db
from lib.llm_engine import ContentEngine
from lib.linkedin_api import LinkedInPublisher

load_dotenv()

def main():
    init_db()
    
    # 1. PRE-FLIGHT CHECK: Validate LinkedIn Version first!
    publisher = LinkedInPublisher(os.getenv("LINKEDIN_ACCESS_TOKEN"))
    is_valid, error_msg = publisher.check_connection()
    
    if not is_valid:
        print(f"🛑 POSTING CANCELLED: {error_msg}")
        return # Stops the script before Gemini is called

    # 2. Check for ideas
    conn = sqlite3.connect('data/engine.db')
    cur = conn.cursor()
    cur.execute("SELECT id, topic, context FROM ideas WHERE status='pending' LIMIT 1")
    row = cur.fetchone()
    
    if not row:
        print("Idea bank empty. Run 'python add_ideas.py' first.")
        return
    
    idea_id, topic, context = row

    # 3. ONLY NOW we call Gemini (Saving credits)
    print(f"🤖 LinkedIn is ready. Generating post for: {topic}...")
    engine = ContentEngine(os.getenv("GEMINI_API_KEY"))
    package = engine.generate(topic, context)
    
    # Assembly
    hook = package.get('hooks', ["No hook"])[0]
    body = package.get('post_body', "No body")
    tags = " ".join(package.get('hashtags', []))
    final_post = f"{hook}\n\n{body}\n\n{tags}"
    
    print("\n--- PREVIEW ---")
    print("\n--- OPTIONS ---")
    print("[y] Publish to LinkedIn")
    print("[s] Skip (Mark as skipped)")
    print("[q] Quit")
    
    choice = input("\nAction: ").lower()
    
    if choice == 'y':
        res = publisher.post(final_post)
        if res.status_code == 201:
            cur.execute("UPDATE ideas SET status='posted' WHERE id=?", (idea_id,))
            print("🚀 Successfully published!")
        else:
            print(f"❌ Error: {res.text}")
            
    elif choice == 's':
        cur.execute("UPDATE ideas SET status='skipped' WHERE id=?", (idea_id,))
        print("⏭️ Idea skipped. It won't appear again.")
        
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()