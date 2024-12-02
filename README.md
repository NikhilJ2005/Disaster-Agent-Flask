AI Disaster Preparedness Assistant
The AI Disaster Preparedness Assistant is a Flask-based web application designed to help communities, individuals, and organizations better prepare for, respond to, and recover from natural disasters. 

This project integrates advanced AI models to provide tailored responses and actionable insights through specialized agents.

Features
Community Education:

Generate disaster preparedness guides for specific community types and geographical locations.

Tailored responses based on cultural, social, and economic factors.

Risk Assessment:

Assess disaster risks for given locations and disaster types.
Provides predictive models and mitigation strategies.
Emergency Response:

Create detailed response plans for various disaster scenarios.
Includes evacuation routes, communication plans, and recovery strategies.


Live Updates:

Real-time disaster alerts and updates for specific locations.
Provides actionable information on ongoing emergencies.


Disaster History:

Retrieve historical data on specific disasters in given regions.
Includes a time-frame filter to focus on recent incidents.


Aid Resources:

Detailed information about insurance, government aid programs, and disaster relief schemes.
Includes eligibility criteria and application procedures.


Technologies Used
Backend
Flask: Web framework to handle routing and API endpoints.
LangChain: Framework for managing AI interactions and LLM chains.
OpenAI API: Integration with advanced language models.
Google Serper API: Provides real-time search results for live updates and disaster history.

Frontend
HTML & CSS (TailwindCSS): For responsive and modern UI.
JavaScript: Handles interactivity, form validation, and API requests.


Environment Variables:
SAMBANOVA_API_KEY: API key for SambaNova's OpenAI-like API.
SERPER_API_KEY: API key for Google Serper API.


Installation
Clone the Repository:

bash
Copy code

git clone https://github.com/your-username/ai-disaster-preparedness-assistant.git

cd ai-disaster-preparedness-assistant


Set Up a Virtual Environment:

bash
Copy code
python3 -m venv .venv
source .venv/bin/activate   # For Linux/Mac
.venv\Scripts\activate      # For Windows
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Environment Variables: Create a .env file in the root directory and add the following:

makefile
Copy code
SAMBANOVA_API_KEY=your_sambanova_api_key
SERPER_API_KEY=your_serper_api_key
Run the Application:

bash
Copy code
python main.py
Access the Application: Open your browser and navigate to:

arduino
Copy code
http://127.0.0.1:5000/
Usage
Select an Agent:

Navigate through the left sidebar to choose an agent.
Enter Input Fields:

Each agent provides placeholders and sample queries to guide you.
Submit Queries:

Enter your query in the input box and click "Send."
View Responses:

Responses are displayed in a clean, spaced format with bullet points for clarity.
Switch Agents:

Chat histories are saved for each agent, and switching between agents is seamless.
Sample Queries
Community Education:
"Create a flood preparedness guide for an urban community in Texas."
Risk Assessment:
"Assess the risk of earthquakes in San Francisco."
Emergency Response:
"Create a response plan for a hurricane in a coastal town."
Live Updates:
"Get live updates on the current wildfire in California."
Disaster History:
"Provide a history of landslides in Kerala over the past 5 years."
Aid Resources:
"What government aid is available for flood victims in Texas?"
