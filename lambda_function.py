import boto3
import json
import telegram

TOKEN_KEY = 'HAALBAI_BOT_TELEGRAM_TOKEN'
CHANNEL_KEY = 'HAALBAI_BOT_TELEGRAM_CHANNEL_TO'

def get_parameter(param_name):
    """
    This function reads a secure parameter from AWS' SSM service.
    The request must be passed a valid parameter name, as well as
    temporary credentials which can be used to access the parameter.
    The parameter's value is returned.
    """
    # Create the SSM Client
    ssm = boto3.client('ssm', region_name='us-east-2')
    # Get the requested parameter
    response = ssm.get_parameters(
        Names=[param_name],
        WithDecryption=True
    )
    # Store the credentials in a variable
    credentials = response['Parameters'][0]['Value']
    return credentials

def lambda_handler(event, context):
    telegram_token = get_parameter(TOKEN_KEY)
    telegram_channel = '@' + get_parameter(CHANNEL_KEY)
    bot = telegram.Bot(telegram_token)
    return_code = 200
    try:
        bot.sendMessage(telegram_channel, 'Hello World')
    except Exception as e:
        return_code = 500

    return {
        'statusCode': return_code
    }

