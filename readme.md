# Welcome To the Dobot Voice Control Application! 
## This Tutorial will guide you through the process of setting up and running the application.

## Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

## Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

## Running LiveKit

1. Set up environment variables by creating a livekit account, heading to setting and generating a new token, Copy the API key, API secret and url then set them as environment variables. Then head to google ai studio and create your free google_api_key and set it as an environment variable:
```bash
export LIVEKIT_API_KEY=<your-api-key>
export LIVEKIT_API_SECRET=<your-api-secret>
export LIVEKIT_URL=<your-url>
export GOOGLE_API_KEY=<your-google-api-key>
```

2. Start the LiveKit server. In the Voice Control Application directory, run:
```bash
python main.py start
```

## Common Issues and Troubleshooting

- If you encounter permission issues, try running the commands with sudo
- Check if all environment variables are properly set

## Additional Resources

- [LiveKit Documentation](https://docs.livekit.io)
- [API Reference](https://docs.livekit.io/api-reference)
- [GitHub Repository](https://github.com/livekit/livekit)

## Support

For additional help or issues:
- Create an issue in the GitHub repository

