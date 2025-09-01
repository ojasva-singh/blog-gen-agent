import os
import ast
import re
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables from a .env file
load_dotenv()

class PersonalizedPostAgent:
    def __init__(self):
        try:
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise RuntimeError(f"Failed to initialize AI agent: {e}")

    def analyze_profile(self, profile_text: str) -> str:

        if not profile_text or not profile_text.strip():
            raise ValueError("Profile text cannot be empty.")

        prompt = f"""
        Analyze the following professional text from a resume or LinkedIn profile.
        Your task is to create a concise summary of the user's professional persona.

        **Instructions:**
        1. Identify their industry and primary role (e.g., "Senior Software Engineer in FinTech").
        2. List their top 3-5 core competencies or skills.
        3. Describe their writing style and tone (e.g., "Formal and data-driven," "Casual and story-focused," "Technical and precise").
        4. Note their level of experience (entry-level, mid-level, senior, executive).
        5. Identify their likely audience (peers, clients, industry leaders, students).
        6. Keep the entire analysis under 150 words.

        **Profile Text:**
        ---
        {profile_text}
        ---

        **Analysis Summary:**
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error during profile analysis: {e}")
            return "Error: Could not analyze profile."

    def recommend_topics(self, analysis: str) -> list[str]:
        if "Error" in analysis:
            return []
            
        prompt = f"""
        Based on this professional profile analysis, suggest five engaging and relevant topics for a LinkedIn post.
        The topics should be distinct and align with the user's expertise and industry.

        **Profile Analysis:**
        ---
        {analysis}
        ---

        **CRITICAL INSTRUCTIONS:**
        - You MUST return ONLY a valid Python list format
        - Use exactly this format: ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
        - Do not include any additional text, explanations, or formatting
        - Each topic should be a complete, actionable phrase
        - Topics should be 5-15 words long
        
        Example response format:
        ["AI in Modern Software Development", "The Future of Remote Collaboration", "Building High-Performance Teams", "Data-Driven Decision Making", "Career Growth Strategies"]
        """
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean the response to extract just the list part
            if '[' in response_text and ']' in response_text:
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                list_text = response_text[start_idx:end_idx]
                recommended_list = ast.literal_eval(list_text)
                
                if isinstance(recommended_list, list) and len(recommended_list) >= 3:
                    return recommended_list[:5]  # Return max 5 topics
            
            # If parsing fails, try alternative parsing
            import re
            # Look for quoted strings in the response
            topics = re.findall(r'"([^"]*)"', response_text)
            if len(topics) >= 3:
                return topics[:5]
                
            # Final fallback - return default topics
            raise ValueError("Could not parse topics from response")
            
        except (ValueError, SyntaxError, TypeError) as e:
            print(f"Error parsing topic recommendations: {e}")
            print(f"Raw response: {response.text if 'response' in locals() else 'No response'}")
            # Return default topics based on analysis
            if "software" in analysis.lower() or "engineer" in analysis.lower() or "developer" in analysis.lower():
                return [
                    "The Evolution of Software Development Practices",
                    "Building Scalable and Maintainable Code",
                    "AI Tools Transforming Developer Workflows",
                    "Remote Team Collaboration Best Practices",
                    "Career Growth Strategies for Tech Professionals"
                ]
            elif "data" in analysis.lower() or "analyst" in analysis.lower():
                return [
                    "Data-Driven Decision Making in Modern Business",
                    "The Art of Data Storytelling and Visualization",
                    "Machine Learning Applications in Industry",
                    "Building Trust in Data Analytics",
                    "Career Pathways in Data Science"
                ]
            elif "marketing" in analysis.lower():
                return [
                    "Digital Marketing Trends Shaping 2025",
                    "Building Authentic Brand Connections",
                    "The Power of Content Marketing Strategy",
                    "Social Media Marketing Best Practices",
                    "Measuring Marketing ROI Effectively"
                ]
            else:
                return [
                    "Leadership Lessons from Industry Challenges",
                    "Building Resilient Professional Networks",
                    "Innovation Strategies for Competitive Advantage",
                    "Work-Life Balance in Modern Careers",
                    "Future Skills for Professional Success"
                ]

    def generate_posts(self, topic: str, analysis: str, tone: str, purpose: str, post_format: str, char_limit: int, include_hashtags: bool, hashtag_count: int = 5, num_posts: int = 3) -> dict:

        hashtag_instruction = f"Include {hashtag_count} relevant hashtags at the end." if include_hashtags else "Do not include hashtags."
        
        prompt = f"""
        Act as a LinkedIn ghostwriter and content strategist. Your task is to generate {num_posts} distinct LinkedIn post drafts.

        **CRUCIAL INSTRUCTIONS:**
        1. **Persona Adoption:** You MUST adopt the writing style and professional persona described in the 'Profile Analysis'. The posts must sound like the user wrote them.
        2. **Tone Alignment:** The posts MUST have a '{tone}' tone.
        3. **Purpose Fulfillment:** The primary goal of the posts is to '{purpose}'.
        4. **Format:** Use the '{post_format}' format structure.
        5. **Character Limit:** Keep each post under {char_limit} characters.
        6. **Hashtags:** {hashtag_instruction}
        7. **CRITICAL:** Separate each post with exactly this text: ===POST_SEPARATOR===

        **Profile Analysis (Your Writing Guide):**
        ---
        {analysis}
        ---

        **Topic to Write About:** "{topic}"

        **Post Format Guidelines:**
        - Story Format: Use narrative structure with personal anecdotes
        - Question Format: Start with an engaging question to drive discussion
        - List Format: Use numbered points or bullet-style content
        - How-to Format: Provide step-by-step guidance
        - Insight Format: Share professional observations and learnings
        - Problem-Solution Format: Identify a challenge and present solutions

        **Requirements:**
        - Create {num_posts} unique posts that correctly synthesize the persona, tone, purpose, and format.
        - Each post should feel authentic and engaging.
        - Vary the hooks and content structure across posts.
        - Use exactly ===POST_SEPARATOR=== between posts (no extra text or characters).
        - Do not include any preamble or explanation, just the posts separated by ===POST_SEPARATOR===.
        """
        
        media_prompt = f"""
        Based on the following topic and post content style, suggest appropriate visual media types for LinkedIn posts:

        **Topic:** "{topic}"
        **Tone:** "{tone}"
        **Format:** "{post_format}"
        **Purpose:** "{purpose}"

        Provide 3-4 specific media suggestions that would complement posts about this topic. For each suggestion, include:
        1. Media type (e.g., "Infographic", "Behind-the-scenes photo", "Video testimonial")
        2. Brief description of what it should show
        3. Why it would be effective for this topic

        Format as a JSON array of objects with keys: "type", "description", "rationale"
        """

        try:
            # Generate posts
            posts_response = self.model.generate_content(prompt)
            posts_text = posts_response.text.strip()
            
            # Split by separator and clean up posts
            posts = []
            if '===POST_SEPARATOR===' in posts_text:
                raw_posts = posts_text.split('===POST_SEPARATOR===')
            else:
                # Fallback: try to split by common separators
                for separator in ['\n---\n', '\n\n---\n\n', '---']:
                    if separator in posts_text:
                        raw_posts = posts_text.split(separator)
                        break
                else:
                    # If no separator found, treat as single post
                    raw_posts = [posts_text]
            
            for post in raw_posts:
                cleaned_post = post.strip()
                if cleaned_post and len(cleaned_post) > 50:  # Filter out very short fragments
                    posts.append(cleaned_post)
            
            posts = posts[:num_posts]  # Limit to requested number
            
            # Generate media suggestions
            media_response = self.model.generate_content(media_prompt)
            try:
                media_text = media_response.text.strip()
                # Try to extract JSON from response
                if '{' in media_text and '}' in media_text:
                    start_idx = media_text.find('[')
                    end_idx = media_text.rfind(']') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        json_text = media_text[start_idx:end_idx]
                        media_suggestions = json.loads(json_text)
                    else:
                        raise ValueError("No JSON array found")
                else:
                    raise ValueError("No JSON structure found")
            except:
                # Fallback media suggestions based on topic and tone
                if "technical" in tone.lower() or "data" in topic.lower():
                    media_suggestions = [
                        {"type": "Infographic or Data Visualization", "description": "Charts, graphs, or diagrams that illustrate your key points", "rationale": "Technical content is more engaging when visualized"},
                        {"type": "Code Screenshot or Architecture Diagram", "description": "Clean, well-formatted code snippets or system architecture", "rationale": "Shows expertise and provides concrete examples"},
                        {"type": "Professional Headshot", "description": "High-quality photo that builds personal connection", "rationale": "Adds human element to technical content"}
                    ]
                elif "story" in purpose.lower() or "personal" in purpose.lower():
                    media_suggestions = [
                        {"type": "Behind-the-scenes Photo", "description": "Authentic workplace moments or career journey highlights", "rationale": "Personal stories resonate better with visual context"},
                        {"type": "Before/After Comparison", "description": "Visual showing transformation or growth", "rationale": "Demonstrates impact and results of your experience"},
                        {"type": "Team Photo or Collaboration Shot", "description": "Images showing teamwork and professional relationships", "rationale": "Builds credibility and shows leadership skills"}
                    ]
                else:
                    media_suggestions = [
                        {"type": "Professional Headshot", "description": "High-quality image that represents your professional brand", "rationale": "Builds trust and personal connection"},
                        {"type": "Industry-related Visual", "description": "Photos or graphics related to your field", "rationale": "Provides context and demonstrates industry knowledge"},
                        {"type": "Quote Graphic or Key Insight", "description": "Visually appealing text overlay with main message", "rationale": "Makes your content more shareable and memorable"}
                    ]
            
            return {
                "posts": posts,
                "media_suggestions": media_suggestions,
                "character_counts": [len(post) for post in posts]
            }
            
        except Exception as e:
            print(f"Error during post generation: {e}")
            return {
                "posts": ["Error: Could not generate posts."],
                "media_suggestions": [],
                "character_counts": [0]
            }

    def get_format_suggestions(self) -> list[str]:
        return [
            "Story Format",
            "Question Format", 
            "List Format",
            "How-to Format",
            "Insight Format",
            "Problem-Solution Format"
        ]

    def estimate_engagement_potential(self, post_content: str) -> dict:
        prompt = f"""
        Analyze this LinkedIn post and provide engagement potential insights.

        **Post Content:**
        ---
        {post_content}
        ---

        **CRITICAL INSTRUCTIONS:**
        - Rate each aspect on a scale of 1-5 (1=poor, 5=excellent)
        - Provide specific, actionable reasoning for each score
        - Return ONLY valid JSON format with no additional text
        - Use exactly this structure:

        {{
            "hook_strength": {{"score": X, "reason": "Brief explanation of opening line effectiveness"}},
            "content_value": {{"score": X, "reason": "Assessment of educational or inspirational worth"}},
            "discussion_potential": {{"score": X, "reason": "Likelihood to generate meaningful comments"}},
            "shareability": {{"score": X, "reason": "Potential for shares and reposts"}}
        }}

        Analyze:
        1. Hook strength: How compelling is the opening? Does it grab attention?
        2. Content value: Does it teach, inspire, or provide useful insights?
        3. Discussion potential: Will people comment with questions/thoughts?
        4. Shareability: Is it worth sharing with others?
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean the response to extract JSON
            if '{' in response_text and '}' in response_text:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_text = response_text[start_idx:end_idx]
                parsed_data = json.loads(json_text)
                
                # Validate structure
                required_keys = ['hook_strength', 'content_value', 'discussion_potential', 'shareability']
                if all(key in parsed_data for key in required_keys):
                    # Ensure each item has score and reason
                    for key in required_keys:
                        if not isinstance(parsed_data[key], dict) or 'score' not in parsed_data[key] or 'reason' not in parsed_data[key]:
                            raise ValueError(f"Invalid structure for {key}")
                    return parsed_data
                    
            raise ValueError("Invalid JSON structure")
            
        except Exception as e:
            print(f"Error in engagement analysis: {e}")
            # Provide more meaningful fallback analysis based on post content
            word_count = len(post_content.split())
            has_question = '?' in post_content
            has_hashtags = '#' in post_content
            
            return {
                "hook_strength": {
                    "score": 4 if len(post_content.split('\n')[0]) < 100 else 3, 
                    "reason": "Opening line length suggests good attention-grabbing potential"
                },
                "content_value": {
                    "score": 4 if word_count > 50 else 3, 
                    "reason": f"Content length ({word_count} words) indicates substantial value"
                },
                "discussion_potential": {
                    "score": 4 if has_question else 3, 
                    "reason": "Question format encourages audience interaction" if has_question else "Content may generate thoughtful responses"
                },
                "shareability": {
                    "score": 4 if has_hashtags else 3, 
                    "reason": "Hashtags increase discoverability" if has_hashtags else "Valuable content with good share potential"
                }
            }