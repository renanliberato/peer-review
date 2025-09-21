# 🎮 Unity Game Bot - AI-Powered Team Collaboration

Meet your virtual Unity mobile game development team! This CLI tool simulates a complete game dev studio with specialized AI roles that help you brainstorm, debug, and optimize your Unity mobile games.

Definitely glitchy, and do not substitute a great team on professional workflows, but fun to experiment and brain dump ideas at. =)

## 🚀 Features

- **6 Specialized AI Roles**: Each with unique personalities and expertise
- **Interactive CLI**: Beautiful terminal UI with Rich formatting
- **Targeted Conversations**: Message specific roles with `@role: message`
- **Group Chat Mode**: Get perspectives from all team members at once
- **Conversation History**: Review past interactions with `history` command

## 👥 Meet the Team

| Role | Emoji | Specialty |
|------|-------|-----------|
| **Product Manager** | 📱 | User retention, monetization, roadmap planning |
| **Game Engineer** | 🔧 | C# scripting, gameplay mechanics, Unity quirks |
| **Graphics Performance Engineer** | ⚡ | Mobile optimization, profiling, 60fps targets |
| **Generalist Artist** | 🎨 | 2D/3D assets, UI polish, visual design |
| **QA Engineer** | 🧪 | Bug hunting, test plans, device compatibility |
| **Engineering Manager** | 👥 | Team coordination, process, mentoring |

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- OpenRouter API key

### Quick Start
```bash
# Clone the repository
git clone <your-repo-url>
cd peer-review

# Run the setup script
./bin/peer-review
```

The setup script will:
1. Create a virtual environment
2. Install dependencies
3. Launch the application

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENROUTER_API_KEY=your_api_key_here" > .env

# Run the app
python app.py
```

## 🔧 Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
DEBUG=True  # Optional: Enable debug logs
```

Get your API key from [OpenRouter](https://openrouter.ai/)

## 💡 Usage Examples

### Group Chat
```
You: How can I optimize my Unity mobile game for better performance?

📱 Product Manager: Focus on the user experience impact...
🔧 Game Engineer: Here are some C# optimization patterns...
⚡ Graphics Performance Engineer: Profile your draw calls first...
🎨 Generalist Artist: Consider asset compression...
🧪 QA Engineer: Test on low-end devices...
👥 Engineering Manager: Let's prioritize the biggest wins...
```

### Targeted Questions
```
You: @graphics performance engineer: My game is running at 30fps on older Android devices

⚡ Graphics Performance Engineer: Ugh, that draw call spike? Here's the fix...
```

### Commands
- `quit` or `exit` - Leave the chat
- `history` - View recent conversations
- `@role: message` - Ask a specific team member

## 🎯 Perfect For

- **Indie Developers**: Get expert advice without hiring a full team
- **Game Jam Participants**: Quick brainstorming and problem-solving
- **Unity Learners**: Understand different aspects of game development
- **Mobile Game Studios**: Supplement your team with AI perspectives
- **Prototyping**: Fast iteration with diverse expert input

## 🧠 Under the Hood

- **AI Model**: Google Gemini Flash 2.5 Flash Lite (fast and cost-effective)
- **API**: OpenRouter for model access
- **UI**: Rich library for beautiful terminal output
- **Language**: Python

## 🎮 Sample Workflow

1. **Start with a broad question** to get all perspectives
2. **Follow up with specific roles** using `@role:message` syntax
3. **Build on suggestions** with iterative conversations
4. **Review history** to track your decisions