# 🚗 Auto Policy AI Analyzer

An intelligent web application that analyzes American auto insurance policies using AI and compares them with US averages. Built with Streamlit and Google's Gemini AI.

## ✨ Features

- **AI-Powered Analysis**: Uses Google Gemini to analyze policy details and provide insights
- **US Average Comparison**: Compares your policy with nationwide averages
- **Interactive Charts**: Visual comparison of premiums and coverage
- **File Upload Support**: Upload policy documents (PDF, DOC, TXT, images)
- **Manual Entry**: Enter policy details manually for analysis
- **Personalized Recommendations**: Get AI-generated recommendations for policy improvements
- **Risk Assessment**: Understand your policy's risk level
- **Modern UI**: Beautiful, responsive interface with custom styling

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PolicyAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Gemini API**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

4. **Create environment file**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env and add your API key
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## 🚀 Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - Navigate to `http://localhost:8501`
   - The app will open automatically

3. **Analyze your policy**
   - **Option 1**: Upload your policy document
   - **Option 2**: Enter policy details manually
   - Click "Analyze Policy" to get AI insights

## 📊 What the AI Analyzes

### Policy Coverage Analysis
- Liability coverage adequacy
- Deductible analysis
- Additional coverage assessment
- Premium cost-effectiveness

### US Average Comparison
- Monthly and annual premiums
- Bodily injury coverage limits
- Property damage coverage
- Uninsured motorist protection
- Medical payments coverage

### AI Recommendations
- Coverage improvement suggestions
- Cost optimization tips
- Risk mitigation strategies
- Policy enhancement opportunities

## 🏗️ Project Structure

```
PolicyAI/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── env_example.txt     # Environment variables template
├── README.md          # Project documentation
└── .env               # Your API keys (create this)
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key

### Customizing US Averages
Edit the `US_AVERAGES` dictionary in `app.py` to update the comparison benchmarks:

```python
US_AVERAGES = {
    "liability_coverage": {
        "bodily_injury": {"per_person": 50000, "per_accident": 100000},
        "property_damage": {"per_accident": 25000}
    },
    "monthly_premium": 150,
    "annual_premium": 1800,
    # ... other averages
}
```

## 🎨 Features in Detail

### File Upload Support
- **Supported formats**: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG
- **Text extraction**: Automatically extracts text from uploaded documents
- **Image processing**: Preview uploaded images (OCR coming soon)

### Manual Entry Interface
- **Liability Coverage**: Bodily injury and property damage limits
- **Deductibles**: Comprehensive and collision deductibles
- **Additional Coverage**: Uninsured motorist, medical payments, rental reimbursement
- **Premium Information**: Monthly and annual premium amounts

### AI Analysis Output
- **Overall Policy Score**: 1-10 rating of your policy
- **Coverage Adequacy**: Assessment of protection levels
- **Cost Effectiveness**: Value analysis of premiums
- **Risk Level**: Current risk assessment
- **Detailed Comparisons**: Side-by-side analysis with US averages
- **Personalized Recommendations**: Actionable improvement suggestions

## 🔒 Privacy & Security

- **Local Processing**: All analysis runs locally on your machine
- **No Data Storage**: Policy information is not stored or transmitted
- **Secure API**: Uses Google's secure Gemini API for analysis
- **Environment Variables**: API keys stored securely in .env file

## 🚧 Future Enhancements

- [ ] OCR support for image uploads
- [ ] PDF text extraction improvements
- [ ] State-specific average comparisons
- [ ] Historical policy tracking
- [ ] Multiple policy comparison
- [ ] Export analysis reports
- [ ] Mobile-responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check that your Google API key is correctly set in the `.env` file
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Verify you have an active internet connection for API calls
4. Check the Streamlit console for error messages

## 📊 Data Sources

The US average data used for comparisons is based on:
- National Association of Insurance Commissioners (NAIC) data
- Industry reports and surveys
- Consumer insurance studies

*Note: These are approximate averages and may vary by state, age, driving record, and other factors.*

---

**Built with ❤️ using Streamlit and Google Gemini AI** 