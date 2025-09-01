import streamlit as st
import PyPDF2
from io import BytesIO
from ai_agent import PersonalizedPostAgent
import time
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="AI LinkedIn Post Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #0077B5;
        --secondary-color: #00A0DC;
        --accent-color: #F3F6F8;
        --text-dark: #2D2D2D;
        --success-color: #00C851;
        --warning-color: #FF8800;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling for the app */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,119,181,0.3);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 700 !important;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.2rem !important;
        margin: 0 !important;
    }
    
    /* Step indicators */
    .step-indicator {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        padding: 0;
    }
    
    .step {
        display: flex;
        align-items: center;
        margin: 0 1rem;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .step.active {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        box-shadow: 0 2px 10px rgba(0,119,181,0.3);
    }
    
    .step.completed {
        background: var(--success-color);
        color: white;
    }
    
    .step.inactive {
        background: var(--accent-color);
        color: #666;
    }
    
    /* Cards */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        color: #2D2D2D !important;
    }
    
    .info-card p, .info-card h4, .info-card strong {
        color: #2D2D2D !important;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
        transition: transform 0.2s ease;
        color: #2D2D2D !important;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-card p, .feature-card h4, .feature-card strong {
        color: #2D2D2D !important;
    }
    
    /* Post cards */
    .post-card {
        background: white;
        border: 1px solid #e1e5e9;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .post-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        transform: translateY(-1px);
    }
    
    .post-header {
        display: flex;
        justify-content: between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f1f3f4;
    }
    
    .char-count {
        background: var(--accent-color);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-dark);
    }
    
    .char-count.good {
        background: #d4edda;
        color: #155724;
    }
    
    .char-count.warning {
        background: #fff3cd;
        color: #856404;
    }
    
    .char-count.danger {
        background: #f8d7da;
        color: #721c24;
    }
    
    /* Media suggestions */
    .media-suggestion {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid var(--secondary-color);
        color: #2D2D2D !important;
    }
    
    .media-suggestion p, .media-suggestion h4, .media-suggestion strong {
        color: #2D2D2D !important;
    }
    
    /* Progress bar */
    .progress-container {
        margin: 2rem 0;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* Metrics */
    .metric-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        flex: 1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-score {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'input'
if 'profile_text' not in st.session_state:
    st.session_state.profile_text = ""
if 'analysis' not in st.session_state:
    st.session_state.analysis = ""
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = ""
if 'selected_tone' not in st.session_state:
    st.session_state.selected_tone = ""
if 'selected_purpose' not in st.session_state:
    st.session_state.selected_purpose = ""
if 'selected_format' not in st.session_state:
    st.session_state.selected_format = ""
if 'char_limit' not in st.session_state:
    st.session_state.char_limit = 1500
if 'include_hashtags' not in st.session_state:
    st.session_state.include_hashtags = True
if 'hashtag_count' not in st.session_state:
    st.session_state.hashtag_count = 5


# --- Helper Functions ---
def pdf_to_text(file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

def reset_app():
    """Resets the session state to start over."""
    for key in list(st.session_state.keys()):
        if key not in ['stage']:
            del st.session_state[key]
    st.session_state.stage = 'input'
    st.rerun()

def get_step_indicator():
    """Returns HTML for step indicator."""
    steps = [
        ("Profile", "input"),
        ("Topics", "recommend"), 
        ("Settings", "refine"),
        ("Generate", "generate")
    ]
    
    html = '<div class="step-indicator">'
    for i, (name, stage) in enumerate(steps):
        if st.session_state.stage == stage:
            status = "active"
        elif i < [s[1] for s in steps].index(st.session_state.stage):
            status = "completed"
        else:
            status = "inactive"
        
        html += f'<div class="step {status}">📍 {name}</div>'
        if i < len(steps) - 1:
            html += '<div style="margin: 0 0.5rem; color: #ccc;">→</div>'
    
    html += '</div>'
    return html

def get_char_count_class(count, limit):
    """Returns CSS class based on character count."""
    if count <= limit * 0.8:
        return "good"
    elif count <= limit * 0.95:
        return "warning"
    else:
        return "danger"

def display_engagement_metrics(engagement_data):
    """Display engagement potential metrics."""
    if not engagement_data:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("Hook Strength", engagement_data.get("hook_strength", {}).get("score", 0)),
        ("Content Value", engagement_data.get("content_value", {}).get("score", 0)),
        ("Discussion", engagement_data.get("discussion_potential", {}).get("score", 0)),
        ("Shareability", engagement_data.get("shareability", {}).get("score", 0))
    ]
    
    for i, (col, (label, score)) in enumerate(zip([col1, col2, col3, col4], metrics)):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-score">{score}/5</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


# --- Main App Header ---
st.markdown("""
<div class="main-header">
    <h1>🚀 AI LinkedIn Post Generator</h1>
    <p>Create personalized, engaging LinkedIn posts that match your unique voice and style</p>
</div>
""", unsafe_allow_html=True)

# Step indicator
st.markdown(get_step_indicator(), unsafe_allow_html=True)

# Get User Input -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if st.session_state.stage == 'input':
    st.markdown("## 📝 Step 1: Tell Me About Your Professional Background")
    
    st.markdown("""
    <div class="info-card">
        <h4>🎯 Why do I need your profile?</h4>
        <p>To generate posts that sound authentically like <strong>you</strong>, I analyze your professional background, writing style, and expertise. This ensures each post matches your unique voice and resonates with your audience.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📄 Option A: Upload Resume (PDF)")
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type="pdf",
            help="Your resume will be analyzed and then immediately discarded. No data is stored."
        )
        
        if uploaded_file:
            st.success("✅ Resume uploaded successfully!")
    
    with col2:
        st.markdown("### ✏️ Option B: Paste Profile Text")
        pasted_text = st.text_area(
            "Paste your LinkedIn About section and key experience details",
            height=200,
            placeholder="Example: I'm a Senior Data Scientist with 5+ years experience in ML/AI, passionate about transforming business challenges into data-driven solutions. Led cross-functional teams at Fortune 500 companies...",
            help="Include your role, industry, key skills, and any notable achievements"
        )

    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Analyze My Profile", type="primary", use_container_width=True):
            if uploaded_file:
                st.session_state.profile_text = pdf_to_text(BytesIO(uploaded_file.getvalue()))
            elif pasted_text:
                st.session_state.profile_text = pasted_text
            else:
                st.warning("⚠️ Please upload a PDF or paste some text to proceed.")

            if st.session_state.profile_text:
                with st.spinner("🧠 Analyzing your professional profile..."):
                    time.sleep(1)  # Visual feedback
                st.session_state.stage = 'recommend'
                st.rerun()

# Recommend Topics -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif st.session_state.stage == 'recommend':
    st.markdown("## 🎯 Step 2: Choose Your Post Topic")
    
    # Generate analysis and recommendations if not already done
    with st.spinner("🔍 Analyzing your profile and generating topic ideas..."):
        if not st.session_state.analysis:
            try:
                agent = PersonalizedPostAgent()
                st.session_state.analysis = agent.analyze_profile(st.session_state.profile_text)
                st.session_state.recommendations = agent.recommend_topics(st.session_state.analysis)
            except Exception as e:
                st.error(f"❌ Failed to initialize the AI Agent. Check your GEMINI_API_KEY. Error: {e}")
                st.session_state.stage = 'input'
    
    # Display analysis
    st.markdown("### 👤 Your Professional Persona")
    st.markdown(f"""
    <div class="info-card">
        {st.session_state.analysis}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Recommended Topics")
    st.markdown("Based on your profile, here are some engaging topic ideas:")
    
    # Display recommended topics in a grid
    if st.session_state.recommendations:
        num_cols = min(3, len(st.session_state.recommendations))
        cols = st.columns(num_cols)
        
        for i, topic in enumerate(st.session_state.recommendations):
            with cols[i % num_cols]:
                if st.button(f"📌 {topic}", key=f"topic_{i}", use_container_width=True):
                    st.session_state.selected_topic = topic
                    st.session_state.stage = 'refine'
                    st.rerun()

    st.markdown("### ✍️ Or Create Your Own Topic")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        custom_topic = st.text_input(
            "Enter your custom topic",
            placeholder="e.g., Building resilient teams in remote work environments",
            key="custom_topic_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        if st.button("✨ Use Custom Topic", type="primary"):
            if custom_topic:
                st.session_state.selected_topic = custom_topic
                st.session_state.stage = 'refine'
                st.rerun()
            else:
                st.warning("⚠️ Please enter a custom topic.")

# Refine Settings -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif st.session_state.stage == 'refine':
    st.markdown("## ⚙️ Step 3: Customize Your Post Settings")
    
    st.markdown(f"""
    <div class="info-card">
        <h4>🎯 Selected Topic</h4>
        <p><strong>{st.session_state.selected_topic}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎭 Tone & Style")
        
        st.session_state.selected_tone = st.selectbox(
            "Select Tone",
            ("Professional", "Casual", "Inspirational", "Humorous", "Technical", "Thought-Provoking"),
            index=0,
            help="The overall tone and mood of your posts"
        )

        agent = PersonalizedPostAgent()
        format_options = agent.get_format_suggestions()
        st.session_state.selected_format = st.selectbox(
            "Select Format",
            format_options,
            index=0,
            help="The structural approach for your posts"
        )

        st.session_state.selected_purpose = st.selectbox(
            "Primary Purpose",
            ("Educate the audience", "Share a personal story or experience", "Make a bold statement or prediction", 
             "Promote a product or service", "Ask an engaging question to start a discussion", "Provide industry insights"),
            index=0,
            help="The main goal you want to achieve with these posts"
        )
    
    with col2:
        st.markdown("### 📏 Content Specifications")
        
        st.session_state.char_limit = st.slider(
            "Character Limit",
            min_value=500,
            max_value=3000,
            value=1500,
            step=100,
            help="LinkedIn allows up to 3000 characters, but shorter posts often perform better"
        )
        
        st.markdown("**Hashtag Settings**")
        st.session_state.include_hashtags = st.checkbox(
            "Include hashtags", 
            value=True,
            help="Add relevant hashtags to increase discoverability"
        )
        
        if st.session_state.include_hashtags:
            st.session_state.hashtag_count = st.slider(
                "Number of hashtags",
                min_value=3,
                max_value=10,
                value=5,
                help="Optimal range is 3-5 hashtags for best engagement"
            )
        
        # Additional options
        num_posts = st.selectbox(
            "Number of post variations",
            [3, 4, 5],
            index=0,
            help="How many different versions to generate"
        )
        
        st.session_state.num_posts = num_posts
    
    # Format preview
    st.markdown("### 📋 Format Preview")
    format_descriptions = {
        "Story Format": "📖 Personal narrative with anecdotes and lessons learned",
        "Question Format": "❓ Engaging question to spark discussion and comments", 
        "List Format": "📝 Structured points or numbered insights",
        "How-to Format": "🔧 Step-by-step guidance and actionable advice",
        "Insight Format": "💡 Professional observations and industry knowledge",
        "Problem-Solution Format": "🎯 Identify challenges and present solutions"
    }
    
    st.markdown(f"""
    <div class="feature-card">
        <strong>{st.session_state.selected_format}:</strong> {format_descriptions.get(st.session_state.selected_format, "Custom format")}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate My Posts", type="primary", use_container_width=True):
            st.session_state.stage = 'generate'
            st.rerun()

# Generate and Display Posts -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif st.session_state.stage == 'generate':
    st.markdown("## 🎉 Step 4: Your Personalized LinkedIn Posts")
    
    # Settings summary
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <h4>📊 Post Settings</h4>
            <p><strong>Topic:</strong> {st.session_state.selected_topic}</p>
            <p><strong>Tone:</strong> {st.session_state.selected_tone}</p>
            <p><strong>Format:</strong> {st.session_state.selected_format}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <h4>⚙️ Configuration</h4>
            <p><strong>Character Limit:</strong> {st.session_state.char_limit}</p>
            <p><strong>Hashtags:</strong> {'Yes' if st.session_state.include_hashtags else 'No'} {f'({st.session_state.hashtag_count})' if st.session_state.include_hashtags else ''}</p>
            <p><strong>Variations:</strong> {st.session_state.num_posts}</p>
        </div>
        """, unsafe_allow_html=True)

    # Generate posts
    with st.spinner("✨ Creating personalized posts in your unique style..."):
        try:
            agent = PersonalizedPostAgent()
            result = agent.generate_posts(
                topic=st.session_state.selected_topic,
                analysis=st.session_state.analysis,
                tone=st.session_state.selected_tone,
                purpose=st.session_state.selected_purpose,
                post_format=st.session_state.selected_format,
                char_limit=st.session_state.char_limit,
                include_hashtags=st.session_state.include_hashtags,
                hashtag_count=st.session_state.hashtag_count,
                num_posts=st.session_state.num_posts
            )
            
            generated_posts = result["posts"]
            media_suggestions = result["media_suggestions"]
            character_counts = result["character_counts"]

            if generated_posts and "Error" not in generated_posts[0]:
                st.balloons()
                st.success(f"🎉 Successfully generated {len(generated_posts)} personalized post variations!")
                
                # Display posts
                for i, (post, char_count) in enumerate(zip(generated_posts, character_counts)):
                    st.markdown(f"### 📝 Post Option {i+1}")
                    
                    # Post header with character count
                    char_class = get_char_count_class(char_count, st.session_state.char_limit)
                    st.markdown(f"""
                    <div class="post-header">
                        <span class="char-count {char_class}">{char_count}/{st.session_state.char_limit} characters</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Post content
                    st.text_area(
                        f"Post Content {i+1}",
                        post,
                        height=250,
                        key=f"post_{i}",
                        label_visibility="collapsed"
                    )
                    
                    # Engagement analysis
                    with st.expander("📊 Engagement Potential Analysis"):
                        engagement_data = agent.estimate_engagement_potential(post)
                        display_engagement_metrics(engagement_data)
                    
                    # Copy button (simulated)
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        st.button(f"📋 Copy Post {i+1}", key=f"copy_{i}")
                
                # Media suggestions
                if media_suggestions:
                    st.markdown("## 🎨 Suggested Visual Content")
                    st.markdown("Consider adding these types of media to boost engagement:")
                    
                    for i, suggestion in enumerate(media_suggestions):
                        st.markdown(f"""
                        <div class="media-suggestion">
                            <h4>🎯 {suggestion.get('type', f'Media Suggestion {i+1}')}</h4>
                            <p><strong>Description:</strong> {suggestion.get('description', 'No description available')}</p>
                            <p><strong>Why it works:</strong> {suggestion.get('rationale', 'Enhances post engagement')}</p>
                        </div>
                        """, unsafe_allow_html=True)

            else:
                st.error("❌ Sorry, something went wrong during post generation. Please try again.")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Settings"):
            st.session_state.stage = 'refine'
            st.rerun()
    
    with col2:
        if st.button("🔄 Generate New Variations"):
            st.rerun()
    
    with col3:
        if st.button("🔁 Start Over"):
            reset_app()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 3rem;">
    <p>🚀 <strong>AI LinkedIn Post Generator</strong> - Create engaging, personalized content that resonates with your professional audience</p>
    <p>Built with ❤️ using Streamlit and Google's Gemini AI</p>
</div>
""", unsafe_allow_html=True)