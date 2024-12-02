import os
import secrets
from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
from langchain_community.llms import openai
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.utilities import GoogleSerperAPIWrapper
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Configure OpenAI (SambaNova) API
openai.api_key = os.environ.get("SAMBANOVA_API_KEY")
openai.api_base = "https://api.sambanova.ai/v1"
Serper_API_KEY = os.environ.get("SERPER_API_KEY")

# Initialize LLM
llm = ChatOpenAI(
    model_name='Llama-3.2-90B-Vision-Instruct',
    temperature=0.1,
    openai_api_key=openai.api_key,
    openai_api_base=openai.api_base
)

# Agent Classes
class CommunityEducationAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate(
            input_variables=['community_type', 'disaster_type'],
            template="""As a disaster preparedness expert, develop a comprehensive guide tailored for a {community_type} community, addressing the risks associated with {disaster_type}. The guide should include:

1. An overview of the specific risks and challenges posed by {disaster_type} in {community_type} communities.
2. Detailed preparedness steps that individuals and community organizations can take.
3. Cultural, social, and economic factors to consider for effective engagement.
4. Resources and recommendations for enhancing community resilience.

Ensure the guide is accessible, actionable, and considers the unique characteristics of {community_type} communities."""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def generate_content(self, community_type, disaster_type):
        return self.chain.run({
            'community_type': community_type, 
            'disaster_type': disaster_type
        })

class RiskAssessmentAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate(
            input_variables=['location', 'disaster_type'],
            template="""You are a risk assessment specialist. Provide a detailed risk assessment report for {location} focusing on {disaster_type}. The report should cover:

1. Current and historical data on {disaster_type} occurrences in {location}.
2. Geographical and environmental factors contributing to vulnerability.
3. Potential impact scenarios and affected areas.
4. Predictive models or forecasts indicating future risks.
5. Recommended strategies for mitigation and preparedness.

Present the information in a clear and professional manner suitable for local authorities and community leaders."""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def assess_risks(self, location, disaster_type):
        return self.chain.run({
            'location': location, 
            'disaster_type': disaster_type
        })

class EmergencyResponseAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate(
            input_variables=['scenario', 'community_size'],
            template="""As an emergency response coordinator, develop a comprehensive response plan for a {community_size} community facing a {scenario} scenario. The plan should include:

1. Immediate actions to take upon awareness of the {scenario}.
2. Evacuation routes and shelter locations.
3. Communication plans for disseminating information to the public.
4. Coordination with local agencies and emergency services.
5. Special considerations for vulnerable populations.
6. Post-event recovery and support strategies.

Ensure the plan is practical, detailed, and considers the specific needs of a {community_size} community."""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def create_response_plan(self, scenario, community_size):
        return self.chain.run({
            'scenario': scenario, 
            'community_size': community_size
        })

class LiveUpdatesAgent:
    def __init__(self, llm):
        self.llm = llm
        self.search = GoogleSerperAPIWrapper(serper_api_key=Serper_API_KEY)
        self.prompt = PromptTemplate(
            input_variables=['location', 'search_results'],
            template="""You are a disaster alert assistant. Based on the following search results for {location}, summarize the live updates and alerts related to any disasters or emergencies. Be concise and provide actionable information.

Search Results:
{search_results}
"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def get_live_updates(self, location):
        # Use the search wrapper to get live updates
        query = f"{location} disaster alerts"
        search_results = self.search.run(query)
        # Run the LLM chain with the search results
        return self.chain.run({
            'location': location,
            'search_results': search_results
        })

class DisasterHistoryAgent:
    def __init__(self, llm):
        self.llm = llm
        self.search = GoogleSerperAPIWrapper(serper_api_key=Serper_API_KEY)
        self.prompt = PromptTemplate(
            input_variables=['location', 'search_results'],
            template="""You are a historian specializing in natural disasters. Based on the following search results for {location}, provide a detailed history of significant natural disasters that have occurred in the region. Include dates, impacts, and any notable aftermaths.

Search Results:
{search_results}
"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def get_disaster_history(self, location):
        query = f"History of natural disasters in {location}"
        search_results = self.search.run(query)
        return self.chain.run({
            'location': location,
            'search_results': search_results
        })

class AidResourcesAgent:
    def __init__(self, llm):
        self.llm = llm
        self.search = GoogleSerperAPIWrapper(serper_api_key=Serper_API_KEY)
        self.prompt = PromptTemplate(
            input_variables=['location', 'search_results'],
            template="""You are an advisor on disaster relief resources. Based on the following search results for {location}, provide detailed information about insurance options, government aid programs, and other assistance schemes available to residents in case of a disaster. Include eligibility criteria and how to access these resources.

Search Results:
{search_results}
"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def get_aid_resources(self, location):
        query = f"Disaster insurance and government aid schemes in {location}"
        search_results = self.search.run(query)
        return self.chain.run({
            'location': location,
            'search_results': search_results
        })

# Removed NaturalDisasterExpertAgent class

# Initialize agents
community_education_agent = CommunityEducationAgent(llm)
risk_assessment_agent = RiskAssessmentAgent(llm)
emergency_response_agent = EmergencyResponseAgent(llm)
live_updates_agent = LiveUpdatesAgent(llm)
disaster_history_agent = DisasterHistoryAgent(llm)
aid_resources_agent = AidResourcesAgent(llm)

#  function to handle agent-specific routes
def handle_agent(agent_key, agent):
    agent_name = agent_key.replace("_", " ").title()
    if 'chat_histories' not in session:
        session['chat_histories'] = {}
    
    if agent_key not in session['chat_histories']:
        session['chat_histories'][agent_key] = []
    
    if request.method == "POST":
        try:
            data = request.get_json()
            user_message = data.get('message')
            
            if not user_message:
                return jsonify({'success': False, 'error': 'Missing message parameter'}), 400

            # Agent Inputs
            if agent_key == "community_education":
                community_type = data.get('community_type')
                disaster_type = data.get('disaster_type')
                if not community_type or not disaster_type:
                    return jsonify({'success': False, 'error': 'Missing community_type or disaster_type'}), 400
                response = agent.generate_content(community_type, disaster_type)
            
            elif agent_key == "risk_assessment":
                location = data.get('location')
                disaster_type = data.get('disaster_type')
                if not location or not disaster_type:
                    return jsonify({'success': False, 'error': 'Missing location or disaster_type'}), 400
                response = agent.assess_risks(location, disaster_type)
            
            elif agent_key == "emergency_response":
                scenario = data.get('scenario')
                community_size = data.get('community_size')
                if not scenario or not community_size:
                    return jsonify({'success': False, 'error': 'Missing scenario or community_size'}), 400
                response = agent.create_response_plan(scenario, community_size)
            
            elif agent_key == "live_updates":
                location = data.get('location')
                if not location:
                    return jsonify({'success': False, 'error': 'Missing location'}), 400
                response = agent.get_live_updates(location)
            
            elif agent_key == "disaster_history":
                location = data.get('location')
                if not location:
                    return jsonify({'success': False, 'error': 'Missing location'}), 400
                response = agent.get_disaster_history(location)
            
            elif agent_key == "aid_resources":
                location = data.get('location')
                if not location:
                    return jsonify({'success': False, 'error': 'Missing location'}), 400
                response = agent.get_aid_resources(location)
            
            else:
                response = "Unknown agent."

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save chat entry in session
            chat_entry = {
                "user_message": user_message,
                "response": response,
                "timestamp": timestamp
            }
            session['chat_histories'][agent_key].append(chat_entry)
            session.modified = True

            return jsonify({'success': True, 'result': response, 'timestamp': timestamp})
        
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # For GET requests, render the template with the agent's chat history
    chat_history = session['chat_histories'][agent_key]
    return render_template("index.html", agent_name=agent_name, chat_history=chat_history)

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    agent_name = "Disaster Preparedness Agent"
    if request.method == "POST":
        # Handle any POST requests for the home page if necessary
        pass
    return render_template("index.html", agent_name=agent_name, chat_history=[])

@app.route("/community-education", methods=["GET", "POST"])
def community_education():
    return handle_agent("community_education", community_education_agent)

@app.route("/risk-assessment", methods=["GET", "POST"])
def risk_assessment():
    return handle_agent("risk_assessment", risk_assessment_agent)

@app.route("/emergency-response", methods=["GET", "POST"])
def emergency_response():
    return handle_agent("emergency_response", emergency_response_agent)

@app.route("/live-updates", methods=["GET", "POST"])
def live_updates():
    return handle_agent("live_updates", live_updates_agent)

@app.route("/disaster-history", methods=["GET", "POST"])
def disaster_history():
    return handle_agent("disaster_history", disaster_history_agent)

@app.route("/aid-resources", methods=["GET", "POST"])
def aid_resources():
    return handle_agent("aid_resources", aid_resources_agent)

# Utility route to clear all chat histories (optional)
@app.route("/clear-all", methods=["POST"])
def clear_all():
    session.pop('chat_histories', None)
    return jsonify({'success': True, 'message': 'All chat histories cleared.'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
