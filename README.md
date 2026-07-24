# Hemel Study AI

A production-ready Android AI Chat Application with premium UI, advanced settings, and multi-provider AI support.

**Made by Hemel**

## Features

- 🤖 Multi-provider AI support (Gemini, OpenAI, Custom APIs)
- 💬 Real-time streaming chat responses
- 🎨 Three beautiful themes (Light, Dark, WhatsApp)
- 🔒 Secure API key storage with encryption
- 🔐 Lock scheduler for settings protection
- 📝 System prompt customization
- 💾 Complete chat history with SQLite
- 🎯 Material Design 3 UI
- ⚡ Smooth animations and transitions
- 📱 Fully responsive design

## Architecture

```
Hemel-study-apk/
├── main.py
├── buildozer.spec
├── requirements.txt
├── README.md
├── .gitignore
├── .github/
│   └── workflows/
│       └── android.yml
├── core/
│   ├── app_manager.py
│   ├── theme_manager.py
│   ├── settings_manager.py
│   ├── storage_manager.py
│   └── security_manager.py
├── ai/
│   ├── provider.py
│   ├── gemini.py
│   ├── openai.py
│   └── custom_api.py
├── screens/
│   ├── home.py
│   ├── chat.py
│   ├── settings.py
│   └── history.py
├── widgets/
│   ├── message_bubble.py
│   ├── input_bar.py
│   ├── sidebar.py
│   └── animations.py
├── database/
│   └── database.py
└── assets/
    ├── icons/
    ├── images/
    └── fonts/
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Git
- Java Development Kit (JDK)
- Android SDK

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/sarlokhemel-tech/Hemel-study-apk.git
cd Hemel-study-apk
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## GitHub Actions - Automatic APK Build

The repository includes GitHub Actions workflow that automatically builds the Android APK.

### How it works:

1. Push code to the repository
2. GitHub Actions workflow starts automatically
3. Buildozer compiles the application
4. APK is generated and uploaded as artifact

### To download APK:

1. Go to **Actions** tab on GitHub
2. Click on the latest workflow run
3. Download **Hemel-Study-AI-APK** artifact
4. Install on your Android device

## API Configuration

### Gemini API

1. Get your API key from [Google AI Studio](https://aistudio.google.com)
2. In app Settings → Special Feature & Settings → Input API
3. Select Gemini API
4. Paste your API key
5. Save

### OpenAI API

1. Get your API key from [OpenAI](https://platform.openai.com)
2. In app Settings → Special Feature & Settings → Input API
3. Select OpenAI API
4. Paste your API key
5. Save

## Theme Customization

### Available Themes:

1. **Light Theme** - Clean, bright interface
2. **Dark Theme** - Night-friendly, OLED optimized
3. **WhatsApp Theme** - Green-inspired chat interface

Switch themes in: **Settings → Theme**

## Special Features & Settings

### 1. Input API
- Securely store and switch AI providers
- Encrypted API key storage
- Support for Gemini, OpenAI, and custom APIs

### 2. System Prompt
- Customize AI behavior
- Create custom instructions
- Apply system-wide to all conversations

### 3. Lock All Settings
- Schedule time periods when settings are locked
- Prevent accidental API key changes
- Great for study sessions

## Development

### Project Structure

**Core Module** (`core/`)
- Application state management
- Theme handling
- Settings persistence
- Secure storage
- Security operations

**AI Module** (`ai/`)
- Abstract provider interface
- Gemini implementation
- OpenAI implementation
- Custom API support
- Streaming response handling

**UI Module** (`screens/`)
- Home screen with welcome animation
- Chat interface with message bubbles
- Settings management
- Chat history browser

**Widgets** (`widgets/`)
- Message bubble components
- Input bar with actions
- Navigation sidebar
- Animation utilities

**Database** (`database/`)
- SQLite chat storage
- Message persistence
- History management

## Troubleshooting

### Build Issues

**APK build fails in GitHub Actions**
- Check that all files are committed to Git
- Verify Python dependencies are correct
- Check buildozer.spec configuration

**API connection errors**
- Verify internet connection
- Check API key validity
- Ensure API has correct permissions

**UI rendering issues**
- Clear app cache
- Reinstall APK
- Check device screen resolution

## Contributing

This is a production application. For improvements:
1. Create a feature branch
2. Implement changes
3. Test thoroughly
4. Submit pull request

## License

This project is proprietary. All rights reserved.

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation

---

**Hemel Study AI** - Premium AI Chat Application

Made with ❤️ by Hemel
