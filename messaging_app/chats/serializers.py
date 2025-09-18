from rest_framework import serializers
from .models import User, Message, Conversation
from django.contrib.auth.password_validation import validate_password
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=validate_password)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'email', 'phone_number', 'role', 'created_at',
            'password', 'confirm_password'
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return username

    def validate_email(self, email):
        """Validate email format and uniqueness"""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email
    
    def validate_phone_number(self, phone_number):
        """Validate phone number format if provided"""
        if phone_number:
            # Basic phone number validation (adjust regex as needed)
            phone_template = re.compile(r'^\+254\d{9}')
            if not phone_template.match(phone_number):
                raise serializers.ValidationError("Enter a valid phone number. +254*********")
            if User.objects.filter(phone_number=phone_number).exists():
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
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

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

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'participant_name', 'created_at', 'messages']

    def get_participant_name(self, obj):
        """Return participant's full name"""
        return f"{obj.participants_id.first_name} {obj.participants_id.last_name}"

    def validate_participants_id(self, participants_id):
        """Validate participant exists and is active"""
        if not participants_id.is_active:
            raise serializers.ValidationError("Participant account is not active.")
        return participants_id