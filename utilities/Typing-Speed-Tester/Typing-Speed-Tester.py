import time
import random
import urllib.request
import json
import sys
import os
import asyncio
import aiohttp

# Local fallback sentences
fallback_sentences = [
    "Python is fun to learn",
    "Open source is amazing",
    "Practice makes perfect",
    "Typing speed improves daily",
    "Consistency beats motivation",
    "The quick brown fox jumps over the lazy dog",
    "Code is like humor; when you have to explain it, it's bad",
    "Success is not final, failure is not fatal",
    "Keep it simple, stupid is a design principle",
    "Life is what happens when you're busy making other plans",
    "Every day is a second chance to improve yourself",
    "Technology is best when it brings people together",
    "Stay hungry, stay foolish was a famous advice",
    "An apple a day keeps the doctor away",
    "The best way to predict the future is to create it"
]

async def fetch_url(session, url):
    try:
        async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3) as resp:
            if resp.status == 200:
                data = await resp.json()
                phrase = data.get('quote') or data.get('content')
                if phrase:
                    return phrase
    except Exception:
        pass
    return None

async def fetch_phrase_async():
    urls = [
        "https://dummyjson.com/quotes/random",
        "https://api.quotable.io/random"
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        # Gather them concurrently
        results = await asyncio.gather(*tasks)
        for res in results:
            if res:
                return res
    return None

print("\n⌨️ ===============================")
print("   WELCOME TO TYPING SPEED TESTER")
print("================================ ⌨️\n")

while True:
    print("🌐 Fetching a fresh phrase for you...")
    
    sentence = asyncio.run(fetch_phrase_async())
            
    if not sentence:
        print("📴 Offline or API unavailable. Using a classic phrase instead.")
        sentence = random.choice(fallback_sentences)

    print("\n📌 Type the following sentence:\n")
    print(f"👉 {sentence}\n")
    
    input("Press Enter when you are ready... 🚀")
    
    # Start timer
    start_time = time.time()
    
    # User input
    typed_text = input("\n⌨️ Start Typing:\n")
    
    # End timer
    end_time = time.time()
    
    # Calculate time
    time_taken = end_time - start_time
    
    # Calculate words per minute
    words = len(sentence.split())
    wpm = (words / time_taken) * 60 if time_taken > 0 else 0
    
    # Calculate accuracy
    correct_chars = 0
    for i in range(min(len(sentence), len(typed_text))):
        if sentence[i] == typed_text[i]:
            correct_chars += 1
            
    accuracy = (correct_chars / len(sentence)) * 100 if len(sentence) > 0 else 0
    
    # Results
    print("\n🎉 ===== TEST COMPLETED ===== 🎉")
    print(f"⏱️ Time Taken : {time_taken:.2f} seconds")
    print(f"🚀 Typing Speed : {wpm:.2f} WPM")
    print(f"🎯 Accuracy : {accuracy:.2f}%")
    
    # Performance feedback
    if accuracy == 100:
        print("🏆 Perfect Typing!")
    elif accuracy >= 80:
        print("👏 Great Job!")
    elif accuracy >= 50:
        print("👍 Good Attempt!")
    else:
        print("💡 Keep Practicing!")
        
    again = input("\n🔄 Do you want to test again? (y/n): ").strip().lower()
    if again != 'y':
        print("\n👋 Thanks for testing your typing speed! Goodbye!\n")
        break