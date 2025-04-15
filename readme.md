
# LiveKit Setup Guide

## Prerequisites
- Python 3.7 or higher
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

1. Set up environment variables:
```bash
export LIVEKIT_API_KEY=<your-api-key>
export LIVEKIT_API_SECRET=<your-api-secret>
```

2. Start the LiveKit server:
```bash
livekit-server --config config.yaml
```

3. Run the application:
```bash
python main.py
```

## Common Issues and Troubleshooting

- If you encounter permission issues, try running the commands with sudo
- Make sure all ports specified in config.yaml are available
- Check if all environment variables are properly set

## Additional Resources

- [LiveKit Documentation](https://docs.livekit.io)
- [API Reference](https://docs.livekit.io/api-reference)
- [GitHub Repository](https://github.com/livekit/livekit)

## Support

For additional help or issues:
- Create an issue in the GitHub repository
- Join the LiveKit Discord community
- Check the official documentation
