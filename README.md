# Conversational AI Assistant

## Overview
A web-based conversational AI assistant built using AWS Lambda, API Gateway, and AWS Bedrock. This assistant leverages foundation models to respond to user queries in natural language through a simple web interface.

## Technical Architecture

### Components
- **Frontend**: HTML/JavaScript web interface
- **Backend**: AWS Lambda function (Python)
- **API Gateway**: Routes HTTP requests to Lambda
- **AWS Bedrock**: Provides foundation models for AI responses
- **IAM Roles**: Manages permissions for Lambda execution and Bedrock access

### File Structure
- `index.html`: Frontend web interface
- `index.py`: Lambda function code
- `function.zip`: Deployment package for Lambda
- `trust-policy.json`: IAM role trust policy
- `.env`: Environment variables (not committed to repository)
- `.gitignore`: Specifies intentionally untracked files to ignore
- `test_index.py`: Unit tests for Lambda function
- `requirements.txt`: Project dependencies

## Setup Instructions

### Prerequisites
- AWS Account with Bedrock access enabled
- AWS CLI configured with appropriate credentials
- Python 3.8+
- Bedrock model access (Claude, Llama, etc.)

### Local Development
1. Clone the repository
2. Create a `.env` file with your AWS credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `python test_index.py` 
5. Test locally: `python index.py`

### Deployment
1. Package the Lambda function: `zip -r function.zip index.py`
2. Create IAM role using `trust-policy.json`
3. Create Lambda function and upload the package
4. Set up API Gateway to trigger the Lambda function
5. Deploy the API

## Configuration
All sensitive information (API keys, AWS credentials) should be stored in environment variables, either in the `.env` file locally or configured directly in the Lambda function.

### Bedrock Configuration
- Set up AWS Bedrock access in your AWS account
- Configure model ID and parameters in Lambda environment variables
- Ensure proper IAM permissions for Bedrock API access

## Testing
- Comprehensive test suite with >80% code coverage
- Unit tests for success and error scenarios
- Mock testing of AWS Bedrock integration
- Run tests with coverage reports: `python test_index.py`


