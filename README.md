# 🚀 AI LinkedIn Post Generator

[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg)](https://www.python.org)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful AI-driven web application that generates personalized LinkedIn posts tailored to your unique professional voice and style. Built with advanced AI agents and modern web technologies.

## 🎯 Overview

Transform any topic into engaging LinkedIn content that authentically represents your professional brand. The AI analyzes your profile, understands your writing style, and creates multiple post variations optimized for maximum engagement.

### ✨ Key Features

- **🧠 Intelligent Profile Analysis** - AI understands your professional persona and writing style
- **📝 Multi-Format Post Generation** - Story, Question, List, How-to, Insight, and Problem-Solution formats
- **🎭 Tone Customization** - Professional, Casual, Inspirational, Humorous, Technical, and Thought-Provoking tones
- **📏 Character Limit Control** - Customizable limits (500-3000 characters) with visual indicators
- **#️⃣ Smart Hashtag Management** - Toggle hashtags with customizable count (3-10)
- **🎨 Media Suggestions** - AI-powered visual content recommendations
- **📊 Engagement Analysis** - Scoring for hook strength, content value, discussion potential, and shareability
- **📱 Responsive Design** - Beautiful, LinkedIn-inspired UI that works on all devices
- **🏥 Health Monitoring** - Built-in health check endpoints for deployment

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **AI Engine**: Google Gemini 1.5 Flash
- **Backend**: Python 3.9+
- **Document Processing**: PyPDF2 for resume analysis
- **Deployment Ready**: Works with Vercel, Railway, Render, Fly.io, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-linkedin-post-generator.git
   cd ai-linkedin-post-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   Open your browser and navigate to `http://localhost:8501`

## 📋 Requirements

Create a `requirements.txt` file with:

```
streamlit
google-generativeai
PyPDF2
python-dotenv
```

## 🎮 How to Use

### Step 1: Profile Analysis 📝
- **Option A**: Upload your resume (PDF format)
- **Option B**: Paste your LinkedIn profile text
- Click "Analyze My Profile" to let AI understand your professional persona

### Step 2: Topic Selection 🎯
- Choose from AI-recommended topics based on your profile
- Or enter your own custom topic
- Topics are tailored to your industry and expertise

### Step 3: Customize Settings ⚙️
- **Tone**: Select from 6 different tones
- **Format**: Choose from 6 post structures
- **Purpose**: Define your post's main goal
- **Character Limit**: Set between 500-3000 characters
- **Hashtags**: Toggle and customize count (3-10)
- **Variations**: Generate 3-5 different versions

### Step 4: Generate & Refine 🎉
- Review your personalized posts
- Check engagement potential scores
- Get media suggestions for enhanced reach
- Copy your favorite versions to LinkedIn

## 📁 Project Structure

```
ai-linkedin-post-generator/
├── app.py                 # Main Streamlit application
├── ai_agent.py           # AI agent with enhanced capabilities
├── health_check.py       # Health monitoring server
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md            # Project documentation
└── .gitignore           # Git ignore rules
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `HEALTH_PORT` | Health check server port | No (default: 8080) |

### Customization Options

- **Character Limits**: 500-3000 characters
- **Post Formats**: Story, Question, List, How-to, Insight, Problem-Solution
- **Tones**: Professional, Casual, Inspirational, Humorous, Technical, Thought-Provoking
- **Hashtag Count**: 3-10 hashtags
- **Post Variations**: 3-5 different versions

## 🌐 Deployment

### Health Check Endpoint

The application includes a health monitoring server for deployment platforms:

```bash
# Run health check server
python health_check.py

# Test endpoints
curl http://localhost:8080/health    # Simple health check
curl http://localhost:8080/status    # Detailed status
curl http://localhost:8080/          # Homepage check
```

**Made with ❤️ for the LinkedIn community**