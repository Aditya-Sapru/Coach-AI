# Coach AI - Fitness Consultant App

A Python-based fitness consultant application featuring dual AI agents that serve as your personal coach and nutritionist, built with Kivy and powered by Google's Gemini 1.5 Flash AI model.

## Features

- **Dual AI Agents**: Two specialized AI assistants
  - **Coach Agent**: Provides workout plans, exercise guidance, and fitness motivation
  - **Nutritionist Agent**: Offers meal planning, dietary advice, and nutrition tracking
- **Modern UI**: Built with Python's Kivy framework for cross-platform compatibility
- **AI-Powered**: Utilizes Google's Gemini 1.5 Flash for intelligent responses
- **User History**: Tracks user interactions and progress over time
- **Mobile Ready**: Configured with Buildozer for Android deployment

## Project Structure

```
Coach-AI/
├── main.py                          # Main application entry point
├── coach_agent.py                   # Fitness coach AI agent
├── nutritionist_agent.py            # Nutrition specialist AI agent
├── screens_coach_screen.py          # Coach interface screen
├── screens_nutritionist_screen.py   # Nutritionist interface screen
├── user_history.py                  # User data and history management
├── buildozer.spec                   # Android build configuration               
└── README.md                        # Project documentation
```

## Prerequisites

- Python 3.8+
- Google Gemini API key
- Kivy framework
- Android SDK (for mobile deployment)

## Usage

### Desktop Application
```bash
python main.py
```

### Features Overview

**Coach Agent:**
- Personalized workout routines
- Exercise form guidance
- Progress tracking
- Motivational support

**Nutritionist Agent:**
- Custom meal plans
- Calorie tracking
- Nutritional analysis
- Dietary recommendations

## Mobile Deployment

Build for Android using Buildozer:

```bash
# Install buildozer
pip install buildozer

# Initialize and build
buildozer init
buildozer android debug
```

## Configuration

The app uses the following key configurations:
- **AI Model**: Gemini 1.5 Flash for fast, accurate responses
- **UI Framework**: Kivy for cross-platform compatibility
- **Data Storage**: Local user history tracking
- **Build System**: Buildozer for Android deployment

## Dependencies

Key libraries used:
- `kivy` - Cross-platform UI framework
- `google-generativeai` - Gemini AI integration
- `python-dotenv` - Environment variable management

## API Usage

The app integrates with Google's Gemini 1.5 Flash model for:
- Natural language processing
- Contextual fitness and nutrition advice
- Personalized recommendations based on user history

## Security

- API keys are stored in environment variables
- User data is handled locally
- No sensitive information is transmitted without encryption

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Developer**: Aditya Sapru  
**Repository**: [https://github.com/Aditya-Sapru/Coach-AI](https://github.com/Aditya-Sapru/Coach-AI)

## Acknowledgments

- Google Gemini AI for powering the intelligent agents
- Kivy community for the excellent cross-platform framework
- Contributors and testers who helped improve the application

---

*Built with ❤️ using Python, Kivy, and Google Gemini AI*
