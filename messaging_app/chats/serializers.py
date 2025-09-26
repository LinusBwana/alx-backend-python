from rest_framework import serializers
from .models import CustomUser, Message, Conversation
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import re

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(format="%d %b %Y %H:%M:%S")

    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'username', 'first_name', 'last_name', 
            'email', 'phone_number', 'role', 'created_at',
            'password', 'confirm_password'
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
        }

    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return username

    def validate_email(self, email):
        """Validate email format and uniqueness"""
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email
    
    def validate_phone_number(self, phone_number):
        """Validate phone number format if provided"""
        if phone_number:
            # Basic phone number validation (adjust regex as needed)
            phone_template = re.compile(r'^\+254\d{9}')
            if not phone_template.match(phone_number):
                raise serializers.ValidationError("Enter a valid phone number. +254*********")
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("A user with this phone_number already exists.")
        return phone_number
    
    def validate(self, validated_data):
        """Validate password confirmation matches password"""
        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError("Password confirmation does not match.")
        return validated_data
    
    def create(self, validated_data):
        """Create user with encrypted password"""
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
            username = data.get('username')
            password = data.get('password')

            if username and password:
                user = authenticate(username=username, password=password)

                if user is None:
                    raise serializers.ValidationError("Invalid Credentials")
                
                if not user.is_active:
                     raise serializers.ValidationError("User account is disabled")
                
                refresh = RefreshToken.for_user(user)
                
                data['user'] = user
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)

                return data
            
            raise serializers.ValidationError("Both username and password are required")


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sent_at = serializers.DateTimeField(format="%d %b %Y %H:%M:%S", read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'sender_name', 'message_body', 'sent_at']

        extra_kwargs = {
            'message_id': {'read_only': True},
            'sent_at': {'read_only': True},
        }

    def get_sender_name(self, obj):
        """Return sender's full name"""
        return f"{obj.sender_id.first_name} {obj.sender_id.last_name}"

    def validate_message_body(self, message_body):
        """Validate message body is not empty or just whitespace"""
        if not message_body or not message_body.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(message_body) > 5000:  # Reasonable limit
            raise serializers.ValidationError("Message body cannot exceed 5000 characters.")
        return message_body.strip()

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participant_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d %b %Y %H:%M:%S", read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'participant_name', 'created_at', 'messages']

    def get_participant_name(self, obj):
        """Return participant's full name"""
        return ', '.join([f"{participant.first_name} {participant.last_name}" for participant in obj.participants_id.all()])

    def validate_participants_id(self, participants_id):
        """Validate participant exists and is active"""
        if not participants_id:
            raise serializers.ValidationError("Participants list cannot be empty.")

        for participant in participants_id:
            if not participant.is_active:
                raise serializers.ValidationError(
                    f"Participant {participant.username} account is not active."
                )

        return participants_id