# UOB Risk & Regulatory IT Survey - Installation Guide

## System Requirements

- **OS**: Windows 10/11, macOS, or Linux
- **Python**: 3.11 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB
- **Internet**: Required for OpenAI API and MongoDB

## Pre-Installation Setup

### 1. Install Python 3.11+

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt-get install python3.11 python3.11-venv
```

### 2. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (you'll need it later)
5. Set up billing at https://platform.openai.com/account/billing/overview

### 3. MongoDB Setup (Optional)

**Option A: Local MongoDB**
- Download from https://www.mongodb.com/try/download/community
- Install and run MongoDB server
- Default connection: `mongodb://localhost:27017`

**Option B: MongoDB Atlas (Cloud)**
- Go to https://www.mongodb.com/cloud/atlas
- Create a free account
- Create a cluster
- Get connection string
- Update in `.env` file

## Installation Steps

### Step 1: Extract Files

Extract the `UOB_QA_Complete.zip` file to your desired location:
```
C:\Users\YourUsername\Documents\UOB_QA_Complete\
```

### Step 2: Open Command Prompt

**Windows:**
1. Press `Win + R`
2. Type `cmd`
3. Press Enter

**Navigate to project directory:**
```cmd
cd C:\Users\YourUsername\Documents\UOB_QA_Complete
```

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

**Activate virtual environment:**

**Windows:**
```cmd
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 4: Install Dependencies

```cmd
pip install -r requirements.txt
```

This will install:
- Streamlit (UI framework)
- OpenAI (LLM integration)
- PyMongo (database driver)
- And other required packages

Wait for installation to complete (2-5 minutes).

### Step 5: Configure Environment

1. Copy `.env.example` to `.env`:
   ```cmd
   copy .env.example .env
   ```

2. Open `.env` file in a text editor (Notepad, VS Code, etc.)

3. Update with your values:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   MONGODB_URI=mongodb://localhost:27017
   ```

4. Save the file

### Step 6: Copy Configuration

```cmd
copy config\config.ini .
```

This copies the configuration file to the root directory.

### Step 7: Run the Application

```cmd
streamlit run app/app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 8: Access the Application

1. Open your web browser
2. Go to `http://localhost:8501`
3. The UOB Survey application should load

## Troubleshooting

### Issue: "Python not found"

**Solution:**
1. Verify Python is installed: `python --version`
2. If not found, reinstall Python and check "Add Python to PATH"
3. Restart Command Prompt after installation

### Issue: "No module named 'streamlit'"

**Solution:**
```cmd
pip install streamlit
```

### Issue: "OPENAI_API_KEY not set"

**Solution:**
1. Verify `.env` file exists in project root
2. Check that `OPENAI_API_KEY` is set correctly
3. Restart the application: Press Ctrl+C and run `streamlit run app/app.py` again

### Issue: "Cannot connect to MongoDB"

**Solution:**
1. Verify MongoDB is running:
   - Windows: Check Services or MongoDB Compass
   - macOS/Linux: `brew services list` or `sudo systemctl status mongod`
2. If using MongoDB Atlas, verify connection string in `.env`
3. Check internet connection

### Issue: "Port 8501 already in use"

**Solution:**
```cmd
streamlit run app/app.py --server.port 8502
```

### Issue: "Module not found" errors

**Solution:**
```cmd
pip install -r requirements.txt
```

## First Run

1. **Start Survey**
   - Select your role (User or Admin)
   - Click "Start Survey"

2. **Step 1: Baseline Assessment**
   - Answer fixed questions
   - Click "Complete Step 1"

3. **Step 2: Deep Dive**
   - Answer dynamic questions
   - Read tooltips for guidance
   - System generates next question based on your answer

4. **Step 3: Review & Submit**
   - Review all answers
   - Click "Submit Survey"

## Features

### User Features
- ✅ Step 1: Fixed questions for baseline assessment
- ✅ Step 2: Dynamic questions with AI-generated tooltips
- ✅ Step 3: Review and submit survey
- ✅ Progress tracking
- ✅ Conversation history

### Admin Features
- ✅ View all survey responses
- ✅ Generate assessment reports
- ✅ Analytics dashboard
- ✅ Admin settings

## Configuration

### Edit config.ini

Located in `config/config.ini`:

```ini
[APP]
num_open_ended = 15              # Number of open-ended questions
enable_dynamic_questions = true  # Enable/disable dynamic questions
enable_tooltips = true           # Enable/disable tooltips

[OPENAI]
model = gpt-4o-mini              # LLM model
temperature = 0.7                # Creativity (0.0-1.0)
max_tokens = 250                 # Max response length
```

### Edit .env

Located in project root:

```env
OPENAI_API_KEY=sk-...            # Your OpenAI API key
MONGODB_URI=mongodb://...        # MongoDB connection string
```

## Performance Tips

1. **Faster Responses**: Use `gpt-3.5-turbo` instead of `gpt-4o-mini`
2. **Lower Costs**: Reduce `max_tokens` in config.ini
3. **Better Tooltips**: Increase `temperature` to 0.7-0.9
4. **Caching**: Enable tooltip caching (default: enabled)

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Keep API keys private** - don't share with others
3. **Use strong MongoDB passwords** for production
4. **Enable MongoDB authentication** for production
5. **Use HTTPS** for production deployments

## Updating the Application

To update to the latest version:

```cmd
# Deactivate virtual environment
deactivate

# Delete old venv
rmdir /s venv

# Extract new version
# Repeat installation steps
```

## Stopping the Application

Press `Ctrl + C` in the command prompt to stop the Streamlit server.

## Production Deployment

For production deployment:

1. Use a production MongoDB instance
2. Set `APP_ENV=production` in `.env`
3. Use a production-grade web server (Nginx, Apache)
4. Enable HTTPS/SSL
5. Set up monitoring and logging
6. Use environment-specific configurations

## Support & Documentation

- **Quick Start**: See `STEP2_ENHANCED_GUIDE.md`
- **Dynamic Questions**: See `STEP2_DYNAMIC_INTEGRATION.md`
- **Report Generation**: See `REPORT_GENERATION_GUIDE.md`
- **Troubleshooting**: See relevant guide files

## File Structure

```
UOB_QA_Complete/
├── app/
│   ├── app.py                           # Main application
│   ├── dynamic_questions_enhanced.py    # Question generation
│   ├── step2_dynamic_ui_enhanced.py     # Step 2 UI
│   ├── report_generator.py              # Report generation
│   └── admin_report_ui.py               # Admin UI
├── config/
│   └── config.ini                       # Configuration file
├── data/
│   └── questions_fixed.json             # Questions data
├── docs/
│   ├── STEP2_ENHANCED_GUIDE.md
│   ├── STEP2_DYNAMIC_INTEGRATION.md
│   └── REPORT_GENERATION_GUIDE.md
├── .env.example                         # Environment template
├── requirements.txt                     # Python dependencies
├── INSTALLATION_GUIDE.md                # This file
└── README.md                            # Project overview
```

## Next Steps

1. ✅ Complete installation
2. ✅ Run the application
3. ✅ Complete a survey
4. ✅ Generate a report
5. ✅ Explore admin dashboard

## Version Information

- **Version**: 2.0
- **Release Date**: January 14, 2026
- **Author**: Optimum AI Lab
- **Python**: 3.11+
- **Streamlit**: 1.28+
- **OpenAI**: 1.0+

## Contact & Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the documentation files
3. Check Streamlit logs: `streamlit run app/app.py --logger.level=debug`
4. Verify OpenAI API status
5. Check MongoDB connection

---

**Happy surveying! 🚀**
