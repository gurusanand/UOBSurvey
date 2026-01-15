# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub repository with the application code
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- OpenAI API key
- MongoDB Atlas connection string (optional, for data persistence)

## Deployment Steps

### 1. Prepare Your Repository
```bash
# Ensure requirements.txt is in the root directory
# Ensure app.py is in the app/ directory
git push origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to [Streamlit Cloud Dashboard](https://share.streamlit.io/)
2. Click "New app"
3. Select your GitHub repository
4. Choose the branch (usually `main`)
5. Set the main file path to: `app/app.py`
6. Click "Deploy"

### 3. Configure Secrets
After deployment:

1. Go to your app settings (click the "..." menu in the top right)
2. Click "Manage secrets"
3. Add the following secrets:

```toml
# Required for AI-powered questions
OPENAI_API_KEY = "sk-your-actual-api-key-here"

# Optional: For MongoDB data persistence
MONGODB_URI = "mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DB = "uob_survey"
MONGODB_COLLECTION = "responses"
```

**Important:** 
- Never share your secrets
- Each secret should be on its own line
- Do NOT use quotes around secret values in Streamlit Cloud

### 4. Troubleshooting

#### Issue: "ModuleNotFoundError: No module named 'dotenv'"
- This is expected in Streamlit Cloud - it's handled gracefully
- Ensure `python-dotenv` is in `requirements.txt`
- The app will work without the `.env` file using Streamlit Secrets instead

#### Issue: "OPENAI_API_KEY not set"
- Go to app settings → "Manage secrets"
- Add your OpenAI API key as `OPENAI_API_KEY`
- The app will automatically use `st.secrets` in cloud environments

#### Issue: MongoDB connection fails
- Optional - survey works without MongoDB (data stored in session)
- To enable MongoDB:
  1. Set up MongoDB Atlas (free tier available)
  2. Add connection string to secrets as `MONGODB_URI`
  3. Create database and collection before running

### 5. Environment Variables
In Streamlit Cloud, use `st.secrets` instead of `os.environ`:

```python
# Local (uses .env file)
api_key = os.getenv("OPENAI_API_KEY")

# Cloud (uses Streamlit Secrets)
api_key = st.secrets.get("OPENAI_API_KEY")

# Code in the app already handles both automatically
```

## Local Testing

### Test locally before deploying:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/app.py

# Login with:
# User ID: user
# Password: user123$
# or
# User ID: admin
# Password: admin123%%
```

## Production Considerations

1. **Change default credentials** - Update hardcoded credentials in `render_login_page()`
2. **Enable MongoDB** - For persistent data storage across sessions
3. **Use custom domain** - Streamlit Cloud supports custom domains
4. **Enable authentication** - Add enterprise authentication layer
5. **Monitor usage** - Track API calls to OpenAI to manage costs

## Support

For issues:
1. Check Streamlit Cloud logs (app settings → "Logs")
2. Review the troubleshooting section above
3. Check requirements.txt is up to date
4. Verify all secrets are configured
5. Restart the app from settings

