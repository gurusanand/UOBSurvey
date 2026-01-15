# Quick Start Guide - 5 Minutes

## TL;DR - Get Running in 5 Minutes

### Windows Users

```cmd
# 1. Extract zip file
# 2. Open Command Prompt in the extracted folder
# 3. Run these commands:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

# 4. Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here

# 5. Run:
streamlit run app/app.py

# 6. Open browser: http://localhost:8501
```

### macOS/Linux Users

```bash
# 1. Extract zip file
# 2. Open Terminal in the extracted folder
# 3. Run these commands:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 4. Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here

# 5. Run:
streamlit run app/app.py

# 6. Open browser: http://localhost:8501
```

## What You Need

1. **Python 3.11+** - Download from python.org
2. **OpenAI API Key** - Get from platform.openai.com
3. **Internet Connection** - For OpenAI API calls

## File Structure

```
UOB_QA_Complete/
├── app/                    # Application code
├── config/                 # Configuration
├── data/                   # Questions data
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── INSTALLATION_GUIDE.md  # Detailed setup
└── README.md              # Project info
```

## First Run

1. **Start Survey**
   - Select "User" role
   - Click "Start Survey"

2. **Step 1: Baseline** (2 minutes)
   - Answer 15 fixed questions
   - Click "Complete Step 1"

3. **Step 2: Deep Dive** (10-15 minutes)
   - Answer dynamic questions
   - Read tooltips for guidance
   - System generates next question based on your answer

4. **Step 3: Submit** (1 minute)
   - Review all answers
   - Click "Submit Survey"

## Common Issues

### "Python not found"
- Reinstall Python from python.org
- Check "Add Python to PATH" during installation

### "OPENAI_API_KEY not set"
- Edit `.env` file
- Add your API key: `OPENAI_API_KEY=sk-...`
- Restart the app

### "Cannot connect to MongoDB"
- MongoDB is optional for local testing
- Skip if you don't have it installed
- Data will be stored in session memory

### "Port 8501 already in use"
```cmd
streamlit run app/app.py --server.port 8502
```

## Features

✅ **Dynamic Questions** - AI generates questions based on your answers  
✅ **Smart Tooltips** - Specific guidance for each question  
✅ **Progress Tracking** - See your completion percentage  
✅ **Admin Dashboard** - View all responses (if logged in as Admin)  
✅ **Report Generation** - Generate assessment reports  

## Next Steps

1. ✅ Get OpenAI API key
2. ✅ Install Python 3.11+
3. ✅ Follow installation steps above
4. ✅ Run the application
5. ✅ Complete a survey
6. ✅ Generate a report

## Documentation

- **Full Setup**: See `INSTALLATION_GUIDE.md`
- **Dynamic Questions**: See `docs/STEP2_ENHANCED_GUIDE.md`
- **Reports**: See `docs/REPORT_GENERATION_GUIDE.md`
- **Technical Details**: See `docs/STEP2_DYNAMIC_INTEGRATION.md`

## Support

For detailed help:
1. Check `INSTALLATION_GUIDE.md`
2. Review the docs folder
3. Check Streamlit logs: `streamlit run app/app.py --logger.level=debug`

---

**That's it! You're ready to go! 🚀**
