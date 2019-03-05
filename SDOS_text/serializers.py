from rest_framework import serializers
from SDOS_text.models import Message, MessageRecipient, UserWithEmail, MessageRecipient, get_key_pair, rsa_decrypt
from django_cryptography.fields import encrypt


class UserWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    email_password = serializers.CharField(max_length = 64,)
    smtp_server_address = serializers.CharField(max_length = 64)
    smtp_port = serializers.IntegerField()
    public_key = serializers.CharField(max_length = 64, required = True)

    def create(self, validated_data):
        #validated data has smtp info and email
        private_key, public_key = get_key_pair()
        user_with_email = UserWithEmail.objects.create(public_key = public_key, private_key = private_key, **validated_data)
        return user_with_email

    def update(self, instance, validated_data):
        encrypted_passwd = validated_data.get('email_password',instance.email_password)
        
        #encrypt to store in the database
        instance.email_password = encrypt(rsa_decrypt(instance.private_key, encrypted_passwd))
        
        instance.smtp_server_address = validated_data.get('smtp_server_address', instance.smtp_server_address)
        instance.smtp_port = validated_data.get('smtp_port', instance.smtp_port)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

""" class MessageRecipientSerializer(serializers.Serializer):


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    allow_only_uuid_verified_recpt = serializers.BooleanField(required = False, default = True)
    content_sha = serializers.CharField(read_only = True)
    created = serializers.DateTimeField(read_only = True)
    encrypted_content_sha = serializers.CharField(read_only = True) 
    is_permanent = serializers.BooleanField(required = True)
    message_timeout = serializers.DateTimeField()

    message_recpts =  """


