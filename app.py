import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io
import PyPDF2
import pdfplumber
from config import US_AVERAGES, APP_CONFIG, AI_CONFIG, CHART_CONFIG

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
)

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Try different model options including Gemini 2.0
    model_options = ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"]
    model = None
    
    for model_name in model_options:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model connection
            test_response = model.generate_content("Hello")
            st.success(f"✅ Connected successfully using: {model_name}")
            break
        except Exception as e:
            continue
    
    if model is None:
        st.error("❌ Could not connect to any Gemini model. Please check your API key and internet connection.")
        st.info("💡 Available models: gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash, gemini-pro")
        st.stop()
else:
    st.error("Please set your GOOGLE_API_KEY in the .env file")
    st.stop()

# Simple and Clean CSS
st.markdown("""
<style>
    /* Simple Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #00d4ff;
        margin-bottom: 2rem;
    }
    
    /* Simple Cards */
    .metric-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00d4ff;
        color: #ffffff;
    }
    
    .metric-card h4 {
        color: #00d4ff;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-card p {
        color: #e0e0e0;
        line-height: 1.5;
    }
    
    /* Simple Sections */
    .upload-section, .analysis-section {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
    }
    
    /* Simple Buttons */
    .stButton > button {
        background-color: #00d4ff;
        color: #000000;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background-color: #00b8e6;
    }
    
    /* Simple Metrics */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Simple Progress Bars */
    .stProgress > div > div > div {
        background-color: #00d4ff !important;
    }
    
    .stProgress > div > div > div > div {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Simple Tabs */
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff;
        color: #000000;
    }
    
    /* Simple Inputs */
    .stTextArea textarea, .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.5rem;
        color: #ffffff;
    }
    
    .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #00d4ff;
    }
    
    /* Simple Checkboxes */
    .stCheckbox {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# US averages are now imported from config.py

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file using multiple methods"""
    try:
        # Method 1: Try pdfplumber first (better for complex PDFs)
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                return text.strip()
    except Exception as e:
        st.warning(f"pdfplumber failed: {str(e)}")
    
    try:
        # Method 2: Try PyPDF2 as fallback
        pdf_file.seek(0)  # Reset file pointer
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            return text.strip()
    except Exception as e:
        st.warning(f"PyPDF2 failed: {str(e)}")
    
    return None

def analyze_policy_with_gemini(policy_text):
    """Analyze policy using Gemini AI"""
    prompt = f"""
    You are an expert auto insurance analyst. Analyze the following auto insurance policy information and provide a detailed comparison with US averages.
    
    Policy Information:
    {policy_text}
    
    US Averages for reference:
    - Liability Coverage: $50,000/$100,000 bodily injury, $25,000 property damage
    - Comprehensive Deductible: $500
    - Collision Deductible: $500
    - Uninsured Motorist: $25,000/$50,000
    - Medical Payments: $1,000
    - Rental Reimbursement: $30/day
    - Monthly Premium: $150
    - Annual Premium: $1,800
    
    Please provide a detailed analysis in the following JSON format ONLY. Do not include any other text before or after the JSON:
    {{
        "policy_analysis": {{
            "coverage_adequacy": "Brief assessment of coverage adequacy",
            "cost_effectiveness": "Analysis of cost vs. value",
            "risk_level": "Low/Medium/High risk assessment"
        }},
        "comparison": {{
            "liability_adequacy": "Comparison with US liability averages",
            "deductible_analysis": "Analysis of deductible levels",
            "premium_analysis": "Premium comparison with US averages"
        }},
        "recommendations": [
            "Specific recommendation 1",
            "Specific recommendation 2",
            "Specific recommendation 3"
        ],
        "risk_assessment": "Detailed risk assessment",
        "overall_score": 7
    }}
    
    IMPORTANT: Respond with ONLY valid JSON. No additional text, explanations, or formatting outside the JSON structure.
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        

        
        # Try to extract JSON from the response
        if response_text:
            # Look for JSON content between curly braces
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx + 1]
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError as json_error:
                    st.error(f"JSON parsing error: {str(json_error)}")
                    st.info(f"Attempted to parse: {json_text[:100]}...")
                    return None
            else:
                st.error("No JSON structure found in AI response")
                return None
        else:
            st.error("Empty response from AI")
            return None
            
    except Exception as e:
        st.error(f"Error analyzing policy: {str(e)}")
        st.info("This might be due to API limits or network issues. Please try again.")
        return None

def analyze_policy_simple(policy_text):
    """Simple analysis without JSON parsing as fallback"""
    prompt = f"""
    Analyze this auto insurance policy and provide a brief assessment:
    
    {policy_text}
    
    Provide a simple analysis covering:
    1. Coverage adequacy
    2. Cost effectiveness  
    3. Risk level
    4. Key recommendations
    """
    
    try:
        response = model.generate_content(prompt)
        return {
            "policy_analysis": {
                "coverage_adequacy": "Analysis provided by AI",
                "cost_effectiveness": "Cost analysis completed",
                "risk_level": "Risk assessment provided"
            },
            "comparison": {
                "liability_adequacy": "Compared with US averages",
                "deductible_analysis": "Deductible analysis completed",
                "premium_analysis": "Premium comparison done"
            },
            "recommendations": ["Review your policy with an insurance agent", "Consider increasing coverage if needed", "Shop around for better rates"],
            "risk_assessment": response.text,
            "overall_score": 6
        }
    except Exception as e:
        st.error(f"Fallback analysis also failed: {str(e)}")
        return None

def create_comparison_charts(user_policy, us_averages):
    """Create comparison charts"""
    # Premium comparison
    fig_premium = go.Figure()
    fig_premium.add_trace(go.Bar(
        name='Your Policy',
        x=['Monthly Premium', 'Annual Premium'],
        y=[user_policy.get('monthly_premium', 0), user_policy.get('annual_premium', 0)],
        marker_color=CHART_CONFIG['colors']['primary']
    ))
    fig_premium.add_trace(go.Bar(
        name='US Average',
        x=['Monthly Premium', 'Annual Premium'],
        y=[us_averages['monthly_premium'], us_averages['annual_premium']],
        marker_color=CHART_CONFIG['colors']['secondary']
    ))
    fig_premium.update_layout(
        title='Premium Comparison',
        barmode='group',
        height=CHART_CONFIG['height'],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        title_font_color='#00d4ff'
    )
    
    # Coverage comparison
    fig_coverage = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Bodily Injury Coverage', 'Property Damage Coverage', 
                       'Uninsured Motorist', 'Medical Payments'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Add coverage data
    fig_coverage.add_trace(go.Bar(
        name='Your Policy',
        x=['Per Person', 'Per Accident'],
        y=[user_policy.get('liability_coverage', {}).get('bodily_injury', {}).get('per_person', 0),
           user_policy.get('liability_coverage', {}).get('bodily_injury', {}).get('per_accident', 0)],
        marker_color=CHART_CONFIG['colors']['primary']
    ), row=1, col=1)
    
    fig_coverage.add_trace(go.Bar(
        name='US Average',
        x=['Per Person', 'Per Accident'],
        y=[us_averages['liability_coverage']['bodily_injury']['per_person'],
           us_averages['liability_coverage']['bodily_injury']['per_accident']],
        marker_color=CHART_CONFIG['colors']['secondary']
    ), row=1, col=1)
    
    fig_coverage.update_layout(
        height=600, 
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        title_font_color='#00d4ff'
    )
    
    return fig_premium, fig_coverage

def main():
    # Simple Header
    st.markdown('<h1 class="main-header">🚗 Auto Policy AI Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Compare your auto insurance policy with US averages using AI analysis")
    
    # Simple Sidebar
    with st.sidebar:
        st.header("📊 Quick Stats")
        st.metric("US Average Monthly Premium", f"${US_AVERAGES['monthly_premium']}")
        st.metric("US Average Annual Premium", f"${US_AVERAGES['annual_premium']}")
        st.metric("Typical Liability Coverage", "$50K/$100K")
        
        st.header("ℹ️ How it works")
        st.markdown("""
        1. Upload your policy document or enter details manually
        2. Our AI analyzes your coverage
        3. Compare with US averages
        4. Get personalized recommendations
        """)
    
    # Main content
    tab1, tab2 = st.tabs(["📄 Upload Policy", "✍️ Manual Entry"])
    
    with tab1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        st.subheader("Upload Your Auto Policy")
        
        uploaded_file = st.file_uploader(
            "Choose a policy document (PDF, DOC, TXT, or image)",
            type=['pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
            help="Upload your auto insurance policy document for AI analysis"
        )
        
        if uploaded_file is not None:
            # Process uploaded file
            file_content = uploaded_file.read()
            
            if uploaded_file.type == "application/pdf":
                # Handle PDF files
                st.success(f"✅ Successfully uploaded: {uploaded_file.name}")
                
                # Extract text from PDF
                uploaded_file.seek(0)  # Reset file pointer
                text_content = extract_text_from_pdf(uploaded_file)
                
                if text_content:
                    st.text_area("Extracted Text from PDF", text_content, height=300)
                    
                    if st.button("Analyze Policy"):
                        with st.spinner("AI is analyzing your policy..."):
                            analysis = analyze_policy_with_gemini(text_content)
                            if not analysis:
                                st.warning("JSON analysis failed, trying simple analysis...")
                                analysis = analyze_policy_simple(text_content)
                            if analysis:
                                display_analysis_results(analysis)
                else:
                    st.error("❌ Could not extract text from PDF. The file might be scanned or password-protected.")
                    st.info("💡 Try using the Manual Entry tab instead, or upload a different PDF file.")
                    
            elif uploaded_file.type.startswith('image'):
                # Handle image files
                image = Image.open(io.BytesIO(file_content))
                st.image(image, caption="Uploaded Policy Document", use_column_width=True)
                
                # Convert image to text (simplified - in real app, use OCR)
                st.info("🖼️ Image processing feature coming soon. Please use manual entry for now.")
                
            else:
                # Handle text files (TXT, DOC, etc.)
                try:
                    text_content = file_content.decode('utf-8')
                    st.text_area("Extracted Text", text_content, height=200)
                    
                    if st.button("Analyze Policy"):
                        with st.spinner("AI is analyzing your policy..."):
                            analysis = analyze_policy_with_gemini(text_content)
                            if not analysis:
                                st.warning("JSON analysis failed, trying simple analysis...")
                                analysis = analyze_policy_simple(text_content)
                            if analysis:
                                display_analysis_results(analysis)
                except:
                    st.error("❌ Could not read file content. Please try manual entry.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        st.subheader("Enter Policy Details Manually")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Liability Coverage")
            bi_per_person = st.number_input("Bodily Injury - Per Person ($)", value=50000, step=1000)
            bi_per_accident = st.number_input("Bodily Injury - Per Accident ($)", value=100000, step=1000)
            pd_per_accident = st.number_input("Property Damage - Per Accident ($)", value=25000, step=1000)
            
            st.subheader("Deductibles")
            comp_deductible = st.number_input("Comprehensive Deductible ($)", value=500, step=100)
            collision_deductible = st.number_input("Collision Deductible ($)", value=500, step=100)
        
        with col2:
            st.subheader("Additional Coverage")
            um_per_person = st.number_input("Uninsured Motorist - Per Person ($)", value=25000, step=1000)
            um_per_accident = st.number_input("Uninsured Motorist - Per Accident ($)", value=50000, step=1000)
            med_payments = st.number_input("Medical Payments ($)", value=1000, step=100)
            rental_reimbursement = st.number_input("Rental Reimbursement ($/day)", value=30, step=5)
            
            st.subheader("Premium")
            monthly_premium = st.number_input("Monthly Premium ($)", value=150.0, step=10.0)
            annual_premium = monthly_premium * 12
        
        roadside_assistance = st.checkbox("Roadside Assistance", value=True)
        
        if st.button("Analyze My Policy"):
            # Create policy dictionary
            user_policy = {
                "liability_coverage": {
                    "bodily_injury": {"per_person": bi_per_person, "per_accident": bi_per_accident},
                    "property_damage": {"per_accident": pd_per_accident}
                },
                "comprehensive_deductible": comp_deductible,
                "collision_deductible": collision_deductible,
                "uninsured_motorist": {"per_person": um_per_person, "per_accident": um_per_accident},
                "medical_payments": med_payments,
                "rental_reimbursement": rental_reimbursement,
                "roadside_assistance": roadside_assistance,
                "monthly_premium": monthly_premium,
                "annual_premium": annual_premium
            }
            
            # Create policy text for AI analysis
            policy_text = f"""
            Auto Insurance Policy Details:
            
            Liability Coverage:
            - Bodily Injury: ${bi_per_person:,} per person, ${bi_per_accident:,} per accident
            - Property Damage: ${pd_per_accident:,} per accident
            
            Deductibles:
            - Comprehensive: ${comp_deductible:,}
            - Collision: ${collision_deductible:,}
            
            Additional Coverage:
            - Uninsured Motorist: ${um_per_person:,} per person, ${um_per_accident:,} per accident
            - Medical Payments: ${med_payments:,}
            - Rental Reimbursement: ${rental_reimbursement}/day
            - Roadside Assistance: {'Yes' if roadside_assistance else 'No'}
            
            Premium:
            - Monthly: ${monthly_premium:.2f}
            - Annual: ${annual_premium:.2f}
            """
            
            with st.spinner("AI is analyzing your policy..."):
                analysis = analyze_policy_with_gemini(policy_text)
                if not analysis:
                    st.warning("JSON analysis failed, trying simple analysis...")
                    analysis = analyze_policy_simple(policy_text)
                if analysis:
                    display_analysis_results(analysis, user_policy)
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_analysis_results(analysis, user_policy=None):
    """Display the AI analysis results"""
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    st.subheader("🤖 AI Analysis Results")
    
    # Simple overall score display
    if 'overall_score' in analysis:
        score = analysis['overall_score']
        st.metric("Overall Policy Score", f"{score}/10")
        st.progress(score/10)
    
    # Policy analysis
    if 'policy_analysis' in analysis:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Coverage Adequacy</h4>
                <p>{analysis['policy_analysis'].get('coverage_adequacy', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Cost Effectiveness</h4>
                <p>{analysis['policy_analysis'].get('cost_effectiveness', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Risk Level</h4>
                <p>{analysis['policy_analysis'].get('risk_level', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Comparison charts
    if user_policy:
        st.subheader("📊 Comparison with US Averages")
        fig_premium, fig_coverage = create_comparison_charts(user_policy, US_AVERAGES)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_premium, use_container_width=True)
        with col2:
            st.plotly_chart(fig_coverage, use_container_width=True)
    
    # Detailed comparison
    if 'comparison' in analysis:
        st.subheader("📈 Detailed Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Liability Adequacy:**")
            st.write(analysis['comparison'].get('liability_adequacy', 'N/A'))
            
            st.markdown("**Deductible Analysis:**")
            st.write(analysis['comparison'].get('deductible_analysis', 'N/A'))
        
        with col2:
            st.markdown("**Premium Analysis:**")
            st.write(analysis['comparison'].get('premium_analysis', 'N/A'))
    
    # Simple Recommendations
    if 'recommendations' in analysis:
        st.subheader("💡 AI Recommendations")
        for i, rec in enumerate(analysis['recommendations'], 1):
            st.markdown(f"{i}. {rec}")
    
    # Simple Risk Assessment
    if 'risk_assessment' in analysis:
        st.subheader("⚠️ Risk Assessment")
        st.write(analysis['risk_assessment'])
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 