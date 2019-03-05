from django.db import models
from django_cryptography.fields import encrypt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

def get_key_pair(length = 2048):
    pri_key = RSA.generate(length, Random.new().read)
    pub_key = pri_key.publickey()
    return pri_key.exportKey().decode(),pub_key.exportKey().decode()

def rsa_decrypt(pri_key, text):
    pri_key = RSA.importKey(pri_key)
    plaintext = PKCS1_OAEP.new(pri_key).decrypt(text.encode('utf-8'))
    plaintext = plaintext.decode('utf-8')
    return plaintext


# Create your models here.
class UserWithEmail(models.Model):
    id = models.AutoField(primary_key = True)
    email_password = encrypt(models.CharField(max_length = 64))
    smtp_server_address = models.CharField(max_length = 64)
    smtp_port = models.IntegerField(default = 587)

    #The client will encrypt all communication using this 
    public_key = models.CharField(max_length = 2048)
    private_key = models.CharField(max_length = 2048)

    def __str__(self):
        return '%s : %s' % (self.id, self.email)
    class Meta:
        ordering = ['email']

class MessageRecipient(models.Model):
    id = models.AutoField(primary_key = True)
    email = models.EmailField(unique = True, blank = False)
    password = encrypt(models.CharField(max_length = 64, null = False))

    #This will be a part of the link sent to this recipient, after
    #the user clicks the link, we will ask the user for his email,
    #we will check if user has clicked the link that was meant for 
    #him/her only, this check can be turned off/on(allow_only_uuid_verified_recpt) when building the
    #message
    uuid = models.UUIDField()

    def __str__(self):
        return '%s : %s' % (id, self.email)

    class Meta:
        ordering = ['email']

class Message(models.Model):
    id = models.AutoField(primary_key = True)
    content_sha = models.CharField(max_length = 50, null = False, blank = False)
    encrypted_content_sha = models.CharField(max_length = 50 , blank = False) 
    is_permanent = models.BooleanField()
    message_timeout = models.DateTimeField()
    created = models.DateTimeField()
    allow_only_uuid_verified_recpt = models.BooleanField(default = False)
    encryption_key = encrypt(models.CharField(max_length = 64, blank = False))

    #Foreign key
    message_recpts = models.ManyToManyField(MessageRecipient)

    def __str__(self):
        return '%s : %s : %s' % (id, self.content_sha, self.encrypted_content_sha)

    class Meta:
        ordering = ['id']

