from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import secrets

from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer,
    StudentSetupSerializer, FacultySetupSerializer
)
from users.models import User, PasswordResetToken, StudentProfile, FacultyProfile
from contact.models import NotificationLog
from .services import send_email_notification

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Send welcome email
        try:
            send_email_notification(
                to_email=user.email,
                subject='Welcome to Adwaita Mission Institute of Technology',
                message=f'Hello {user.name},\n\nYour account has been created successfully.\n\nRole: {user.role}\nEmail: {user.email}\n\nPlease login to complete your profile setup.'
            )
        except Exception as e:
            # Log but don't fail registration
            NotificationLog.objects.create(
                type='email',
                recipient=user.email,
                content='Welcome email',
                status='failed',
                error_message=str(e)
            )
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """User logout endpoint"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Forgot password endpoint - sends reset token via email"""
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = secrets.token_urlsafe(32)
            expires_at = timezone.now() + timedelta(hours=1)
            
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            
            # Send reset email
            reset_link = f"{request.build_absolute_uri('/')[:-1]}/reset-password?token={token}"
            try:
                send_email_notification(
                    to_email=user.email,
                    subject='Password Reset Request',
                    message=f'Hello {user.name},\n\nYou requested a password reset.\n\nClick here to reset: {reset_link}\n\nThis link expires in 1 hour.\n\nIf you did not request this, please ignore this email.'
                )
                
                return Response({
                    'message': 'Password reset email sent successfully'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                NotificationLog.objects.create(
                    type='email',
                    recipient=user.email,
                    content='Password reset email',
                    status='failed',
                    error_message=str(e)
                )
                return Response({
                    'error': 'Failed to send email. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except User.DoesNotExist:
            # Don't reveal if email exists
            return Response({
                'message': 'If the email exists, a reset link has been sent'
            }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """Reset password with token"""
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                used=False,
                expires_at__gt=timezone.now()
            )
            
            # Update password
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            # Mark token as used
            reset_token.used = True
            reset_token.save()
            
            return Response({
                'message': 'Password reset successful'
            }, status=status.HTTP_200_OK)
            
        except PasswordResetToken.DoesNotExist:
            return Response({
                'error': 'Invalid or expired reset token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """Verify JWT token"""
    return Response({
        'message': 'Token is valid',
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_setup(request):
    """Complete first-time user setup"""
    user = request.user
    
    if user.is_setup_complete:
        return Response({
            'error': 'Setup already completed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if user.role == 'student':
        serializer = StudentSetupSerializer(data=request.data)
        if serializer.is_valid():
            StudentProfile.objects.create(user=user, **serializer.validated_data)
            user.is_setup_complete = True
            user.save()
            return Response({
                'message': 'Student profile setup completed'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif user.role == 'faculty':
        serializer = FacultySetupSerializer(data=request.data)
        if serializer.is_valid():
            FacultyProfile.objects.create(user=user, **serializer.validated_data)
            user.is_setup_complete = True
            user.save()
            return Response({
                'message': 'Faculty profile setup completed'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:  # admin
        user.is_setup_complete = True
        user.save()
        return Response({
            'message': 'Admin setup completed'
        }, status=status.HTTP_200_OK)
