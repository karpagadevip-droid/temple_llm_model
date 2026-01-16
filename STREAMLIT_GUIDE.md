# Temple Expert AI - Streamlit Guide

## 🚀 Quick Start

### Local Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables**

Create a `.env` file:
```bash
TAVILY_API_KEY=your_tavily_key_here
HUGGINGFACE_MODEL_PATH=Karpagadevi/llama-3-temple-expert-600
```

3. **Run the App**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Using the App

### Chat Interface

1. **Load Model**: Click "Load Model" in the sidebar
2. **Ask Questions**: Type in the chat input at the bottom
3. **View Responses**: See agent's answers with optional Chain of Thought

### Features

#### Model Selection
- **60-step (baseline)**: Faster, basic responses
- **600-step (improved)**: Better quality, less hallucination

#### Chain of Thought Display
- Toggle "Show Chain of Thought" to see:
  - Agent's reasoning process
  - Strategy used (search/model/hybrid)
  - Confidence score
  - Quality rating

#### Statistics
- Total queries processed
- Tavily API usage
- Strategy distribution
- Temples discussed

---

## 🎨 UI Components

### Sidebar
- **Model Selection**: Choose between models
- **Display Options**: Toggle Chain of Thought
- **Statistics**: Real-time usage metrics
- **Actions**: Clear conversation

### Main Chat
- **Chat History**: All previous messages
- **Chain of Thought**: Expandable reasoning display
- **Input Box**: Ask new questions

---

## 🚀 Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

2. **Deploy on Streamlit Cloud**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Select your GitHub repo
- Set main file: `app.py`
- Add secrets (API keys)
- Deploy!

**Secrets to add**:
```toml
TAVILY_API_KEY = "your_key_here"
```

### Option 2: Heroku

1. **Create Procfile**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Deploy**
```bash
heroku create temple-expert-ai
heroku config:set TAVILY_API_KEY=your_key_here
git push heroku main
```

### Option 3: Local Network

Run on your local network:
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Access from other devices: `http://your-ip:8501`

---

## ⚙️ Configuration

### Environment Variables

```bash
# Required
TAVILY_API_KEY=your_tavily_api_key

# Optional
HUGGINGFACE_MODEL_PATH=Karpagadevi/llama-3-temple-expert-600
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### Streamlit Config

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
```

---

## 🐛 Troubleshooting

### Model Not Loading

**Issue**: "Error loading model"

**Solutions**:
1. Check GPU availability (model needs GPU or good CPU)
2. Try running without model (search only)
3. Use smaller model or CPU-compatible version

### API Key Error

**Issue**: "Tavily API key not found"

**Solutions**:
1. Check `.env` file exists
2. Verify `TAVILY_API_KEY` is set
3. Restart Streamlit app

### Port Already in Use

**Issue**: "Port 8501 is already in use"

**Solutions**:
```bash
# Use different port
streamlit run app.py --server.port=8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8501 | xargs kill
```

### Slow Performance

**Solutions**:
1. Use caching for model loading
2. Reduce model size (use 60-step)
3. Deploy on server with better resources

---

## 📊 Performance Tips

### Caching

Streamlit automatically caches:
- Model loading (via session state)
- Agent initialization
- Conversation history

### Optimization

1. **Model Loading**: Only reload when model changes
2. **Session State**: Persist agent across interactions
3. **Lazy Loading**: Load model on first use

---

## 🔒 Security

### API Keys

**Never commit API keys to GitHub!**

Use:
- `.env` file (add to `.gitignore`)
- Streamlit secrets (for deployment)
- Environment variables

### Best Practices

1. Add `.env` to `.gitignore`
2. Use `.env.example` for templates
3. Rotate keys regularly
4. Use read-only keys when possible

---

## 📱 Mobile Support

The app is responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

**Note**: Model loading may be slow on mobile networks.

---

## 🎯 Features Roadmap

### Current (v1.0)
- ✅ Chat interface
- ✅ Chain of Thought display
- ✅ Model selection
- ✅ Statistics dashboard

### Future (v2.0)
- [ ] Export conversation
- [ ] Dark mode toggle
- [ ] Voice input
- [ ] Multi-language support
- [ ] Image upload (temple photos)

---

## 💡 Tips

1. **First Time**: Load model before chatting
2. **Switching Models**: Click "Load Model" after selection
3. **Clear Chat**: Use "Clear Conversation" to start fresh
4. **CoT Display**: Toggle on/off as needed
5. **Statistics**: Monitor API usage to stay within limits

---

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud](https://share.streamlit.io)
- [Tavily AI](https://tavily.com)
- [Hugging Face](https://huggingface.co)

---

## 🆘 Support

**Issues?**
1. Check this guide
2. Review error messages
3. Check API keys and environment
4. Restart the app

**Still stuck?**
- Check GitHub issues
- Review Streamlit documentation
- Verify all dependencies installed

---

**Enjoy chatting with Temple Expert AI!** 🏛️
