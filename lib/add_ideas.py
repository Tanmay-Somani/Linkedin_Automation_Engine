import sqlite3
import os

def add_idea(topic, context):
    # Ensure the directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect('/linkedin-engine/data/engine.db')
    cursor = conn.cursor()
    
    # Just in case you haven't run the init script yet
    cursor.execute('''CREATE TABLE IF NOT EXISTS ideas 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, context TEXT, status TEXT DEFAULT 'pending')''')
    
    cursor.execute(
        "INSERT INTO ideas (topic, context, status) VALUES (?, ?, ?)",
        (topic, context, 'pending')
    )
    conn.commit()
    conn.close()
    print(f"\n✅ Idea saved to the bank!")

def main():
    print("--- 💡 LinkedIn Idea Bank ---")
    print("Enter your ideas below. Type 'exit' to stop.\n")

    while True:
        topic = input("1. What is the main Topic/Title? ")
        if topic.lower() == 'exit':
            break
            
        context = input("2. Enter details, links, or technical notes: ")
        if context.lower() == 'exit':
            break
            
        add_idea(topic, context)
        
        print("-" * 30)
        cont = input("Add another? (y/n): ")
        if cont.lower() != 'y':
            break
            
    print("\nGoodbye! Run 'python main.py' when you're ready to generate posts.")

if __name__ == "__main__":
    main()