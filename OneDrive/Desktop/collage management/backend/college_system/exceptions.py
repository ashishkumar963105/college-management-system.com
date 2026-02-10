from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses"""
    
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the error
    logger.error(f"Exception: {exc}, Context: {context}")
    
    if response is not None:
        # Customize the response format
        custom_response = {
            'error': True,
            'message': str(exc),
            'details': response.data if isinstance(response.data, dict) else {'detail': response.data}
        }
        response.data = custom_response
    else:
        # Handle unexpected errors
        custom_response = {
            'error': True,
            'message': 'An unexpected error occurred',
            'details': {'detail': str(exc)}
        }
        response = Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
