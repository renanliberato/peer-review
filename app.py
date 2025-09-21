import requests
import json
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

load_dotenv()

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    print("Error: Set OPENROUTER_API_KEY environment variable.")
    exit(1)

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash-lite"  # Cheap/fast model; change if needed

COMMON_PROMPT = "You work on casual mobile games built with Unity for Android and iOS, using C# for scripting. "

# Role-based system prompts (tailored for casual Unity mobile game dev)
ROLES = {
    "product manager": {
        "prompt": f"{COMMON_PROMPT}You are a chill Product Manager at a fun Unity mobile game studio. You're all about user joy, prioritizing features that boost retention and monetization without overcomplicating dev. Speak casually, like chatting over coffee—use emojis sparingly. Focus on task breakdowns: roadmap tweaks, A/B ideas, balancing biz goals with team bandwidth. Keep it actionable: suggest next steps, pros/cons, and quick wins for mobile players.",
        "emoji": "📱"
    },
    "game engineer": {
        "prompt": f"{COMMON_PROMPT}You are a laid-back Game Engineer in our cozy Unity mobile team. You're the go-to for scripting gameplay logic, integrating assets, and fixing weird Unity quirks on Android/iOS. You do not have access to any specific project code, so provide general advice, hypothetical C# code examples, or ask for more details about the user's code. Respond like a fellow dev in Slack: straightforward, code-snippet friendly, with a dash of 'aha!' humor. Dive into tasks like prototyping mechanics, debugging builds, or optimizing for 60fps. Always end with code ideas or questions to iterate fast.",
        "emoji": "🔧"
    },
    "graphics performance engineer": {
        "prompt": f"{COMMON_PROMPT}You are the performance wizard Graphics Engineer at our indie Unity mobile shop. Obsessed with smooth frames on budget phones—no stuttering shaders or battery hogs. Talk data-first: profile results, LOD tweaks, occlusion culling tips. Casual vibe like sharing war stories post-crunch: 'Ugh, that draw call spike? Here's the fix.' For tasks, analyze bottlenecks, suggest Unity Profiler hacks, and benchmark mobile-specific wins.",
        "emoji": "⚡"
    },
    "generalist artist": {
        "prompt": f"{COMMON_PROMPT}You are the versatile Generalist Artist in our creative Unity mobile crew—handling 2D sprites, UI polish, simple 3D models, all while keeping it pixel-perfect for touchscreens. You're bubbly and collaborative, like brainstorming in Figma over pizza: 'Love that vibe, but let's amp the juice!' For tasks, brainstorm visuals, workflow shortcuts in Photoshop/Procreate/Blender, asset optimization for mobile, and mood board vibes to spark ideas.",
        "emoji": "🎨"
    },
    "qa engineer": {
        "prompt": f"{COMMON_PROMPT}You are the eagle-eyed QA Engineer keeping our Unity mobile games bug-free and fun. Meticulous but fun-loving—spot edge cases on emulators and real devices, from touch glitches to save state fails. For any feature discussed, always list 3-5 important corner cases and common bugs (e.g., network interruptions, low-memory scenarios, device rotations, save/load failures, or platform-specific issues like iOS/Android differences). Prioritize high-impact bugs like crashes or progression blockers. Chat like a teammate venting tests: 'Tested on that ancient Samsung? Crashed—here's the repro.' For tasks, craft detailed test plans, automate with Unity Test Runner, prioritize crashes, and suggest player empathy checks with repro steps.",
        "emoji": "🧪"
    },
    "engineering manager": {
        "prompt": f"{COMMON_PROMPT}You are the supportive Engineering Manager at our tight-knit Unity mobile studio. You're the glue: mentoring juniors, juggling sprints, and shielding the team from scope creep. Warm and motivational, like a standup pep talk: 'Solid progress—let's unblock that.' For tasks, advise on hiring vibes, code reviews, burnout checks, or scaling prototypes. Focus on people + process: action items, retros, and celebrating small wins.",
        "emoji": "👥"
    }
    }

FIRST_PROMPT = """IMPORTANT: This is your very first response in this conversation. Before giving any suggestions or help, ask 2-3 specific clarification questions to better understand what the user is working on, their goals, and any challenges they face. Do not provide advice, code, or suggestions in this response. Focus only on gathering information."""

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # Optional: Add "HTTP-Referer": "http://localhost" and "X-Title": "Unity Game Bot" for leaderboard credits
}

def chat(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,  # Optional: Adjust for creativity (0-2)
        "max_tokens": 500    # Optional: Limit response length
    }
    
    response = requests.post(ENDPOINT, headers=HEADERS, data=json.dumps(payload))
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Main CLI
console = Console()
histories = {role: [{"role": "system", "content": data["prompt"]}] for role, data in ROLES.items()}

console.print(Panel("Unity Game Bot: Group chat with all roles!\nUse '@role: message' (e.g., '@game engineer: optimize this?') for specific follow-ups.\nType 'quit' to exit, 'history' to review chats.", title="Welcome", border_style="green"))

while True:
    user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
    user_input = user_input.strip()
    if not user_input:
        continue
    if user_input.lower() in ['quit', 'exit', 'bye']:
        console.print(Panel("Catch you on the next sprint! 🚀", title="Bot", border_style="yellow"))
        break
    if user_input.lower() == 'history':
        console.print(Panel("--- Chat History ---", style="bold yellow"))
        for role, data in ROLES.items():
            emoji = data["emoji"]
            hist = histories[role]
            console.print(f"\n[bold]{emoji} {role.title()}:[/bold]")
            # Show last two user-assistant pairs
            display_count = 0
            for i in range(len(hist) - 1, 0, -2):
                if display_count >= 2:
                    break
                if i >= 1 and hist[i-1]["role"] == "user":
                    console.print(f"  You: {hist[i-1]['content']}")
                    console.print(f"  {emoji} {role.title()}: {hist[i]['content']}")
                    display_count += 1
        console.print("--- End History ---")
        continue
    
        # Parse for targeted role
    is_targeted = False
    role_name = ""
    parsed_message = user_input
    if user_input.startswith("@") and ":" in user_input[1:]:
        parts = user_input.split(":", 1)
        role_name = parts[0][1:].strip().lower()
        parsed_message = parts[1].strip()
        if role_name in ROLES:
            is_targeted = True

    if is_targeted:
        console.print(f"\n[bold]--- Response from {role_name.title()} ---[/bold]")
        hist = histories[role_name]
        hist.append({"role": "user", "content": parsed_message})
        if len(hist) == 2:
            full_system = ROLES[role_name]["prompt"] + FIRST_PROMPT
            messages = [{"role": "system", "content": full_system}, {"role": "user", "content": parsed_message}]
        else:
            messages = hist
        response = chat(messages)
        hist.append({"role": "assistant", "content": response})
        emoji = ROLES[role_name]["emoji"]
        title = f"{emoji} {role_name.title()}"
        markdown = Markdown(response)
        panel = Panel(markdown, title=title, border_style="bright_blue", expand=False)
        console.print(panel)
        console.print("")  # separation

        if Confirm.ask("Share this with the group?"):
            console.print(f"\n[bold]--- Group Thoughts on Query to {role_name.title()} ---[/bold]")
            for r, data in ROLES.items():
                if r == role_name:
                    continue
                emoji_r = data["emoji"]
                hist_r = histories[r]
                hist_r.append({"role": "user", "content": parsed_message})
                if len(hist_r) == 2:
                    full_system = ROLES[r]["prompt"] + FIRST_PROMPT
                    messages = [{"role": "system", "content": full_system}, {"role": "user", "content": parsed_message}]
                else:
                    messages = hist_r
                resp = chat(messages)
                hist_r.append({"role": "assistant", "content": resp})
                title_r = f"{emoji_r} {r.title()}"
                markdown_r = Markdown(resp)
                panel_r = Panel(markdown_r, title=title_r, border_style="bright_blue", expand=False)
                console.print(panel_r)
                console.print("")  # separation
        continue

    # Process group message
    console.print("\n[bold]--- Group Chat Responses ---[/bold]")
    for role, data in ROLES.items():
        emoji = data["emoji"]
        hist = histories[role]
        hist.append({"role": "user", "content": user_input})
        if len(hist) == 2:
            full_system = data["prompt"] + FIRST_PROMPT
            messages = [{"role": "system", "content": full_system}, {"role": "user", "content": user_input}]
        else:
            messages = hist
        response = chat(messages)
        hist.append({"role": "assistant", "content": response})
        title = f"{emoji} {role.title()}"
        markdown = Markdown(response)
        panel = Panel(markdown, title=title, border_style="bright_blue", expand=False)
        console.print(panel)
        console.print("")  # separation
