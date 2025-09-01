# **LinkedIn Post Generator**

This project is a web application that generates LinkedIn post drafts based on a user-provided topic and other optional details. It uses an AI agent powered by the Gemini API to create multiple post options with different tones and styles.

## **Overview**

The goal of this assignment is to build and deploy a small web app that turns a topic into multiple LinkedIn post options using an AI agent. This demonstrates both web deployment skills and AI agent design skills.

### **Features**

* **Topic Input:** A required text area for the user to enter their desired post topic.  
* **Optional Inputs:**  
  * **Tone:** Select from a list of tones (e.g., Professional, Casual, Humorous).  
  * **Audience:** Specify the target audience for the post.  
  * **Number of Posts:** Choose how many post variations to generate (3 to 5).  
* **AI-Powered Generation:** Utilizes the Gemini API to generate contextually relevant and stylistically appropriate LinkedIn posts.  
* **Clear Output:** Displays the generated posts in individual, easy-to-read cards.

## **Tech Stack**

* **Frontend:** [Streamlit](https://streamlit.io/)  
* **AI Model:** [Google Gemini](https://ai.google.dev/)  
* **Deployment:** The app is designed to be deployed on any platform that supports Python applications, such as Streamlit Community Cloud, Vercel, Netlify, or Heroku.

## **Getting Started**

### **Prerequisites**

* Python 3.7+  
* A Google Gemini API Key.

### **Installation**

1. **Clone the repository:**  
   git clone \<repository-url\>  
   cd \<repository-directory\>

2. **Create a virtual environment and activate it:**  
   python \-m venv venv  
   source venv/bin/activate  \# On Windows, use \`venv\\Scripts\\activate\`

3. **Install the dependencies:**  
   pip install \-r requirements.txt

4. Set up your environment variables:  
   Create a .env file in the root directory and add your Gemini API key:  
   GEMINI\_API\_KEY="YOUR\_API\_KEY\_HERE"

### **Running the Application**

1. **Run the Streamlit app:**  
   streamlit run app.py

2. Open your web browser and navigate to http://localhost:8501.

### **Health Check**

A simple health check endpoint is available to confirm the server is running.

python health\_check.py

If successful, it will print Health check passed.

## **What I'd Do With More Time**

* **Implement Web Search:** Integrate a lightweight web search to ground the generated content in real-time information, including citations and relevant links.  
* **Advanced Style Control:** Allow users to provide examples of posts they like, and use the AI to mimic that style.  
* **Add Quality Guardrails:** Implement filters for profanity and factual inaccuracies before displaying results to the user.  
* **User Accounts & History:** Allow users to create accounts to save their generated posts and view their history.  
* **Cost & Latency Info:** Display token usage, request latency, and a simple cost estimate for each generation request.