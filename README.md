# AI LinkedIn Authority Engine ??

A scalable, technical content pipeline designed to build professional authority on LinkedIn. This is not a spam bot; it is a **Human-in-the-Loop (HITL) system** that uses LLMs to synthesize research and technical builds into high-engagement content.

## ?? System Architecture
Idea Bank (SQLite) ? LinkedIn Handshake (Pre-flight) ? Gemini 1.5 Flash (Synthesizer) ? Hook Optimizer ? Publisher (LinkedIn API v2026.02)

## ??? Tech Stack
- **AI:** Google Gemini 1.5 Flash (via `google-genai`)
- **Backend:** Python 3.14+ / SQLite
- **API:** LinkedIn REST API (Posts API v202602)
- **Validation:** Pydantic (Structured Outputs)

## ?? Getting Started

### 1. Prerequisites
- **Google AI Studio Key:** Get it from [aistudio.google.com](https://aistudio.google.com/)
- **LinkedIn Developer App:** 
    - Enable 'Share on LinkedIn' and 'Sign in with LinkedIn'.
    - Set redirect URI to `https://google.com`.

### 2. Installation
```bash
git clone https://github.com/yourusername/linkedin-engine.git
cd linkedin-engine
pip install -r requirements.txt
