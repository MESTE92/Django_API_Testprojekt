import re                                                    # für Regex Validierung
import bleach                                                # für XSS Schutz
from rest_framework import serializers                       # für Serialisierung
from django.contrib.auth import get_user_model               # gibt CustomUser zurück

User = get_user_model()                                      # == CustomUser zur Laufzeit



class RegisterSerializer(serializers.ModelSerializer):    # -> für Registrierung

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'password', 'profile_picture']

        extra_kwargs = {
            'id':       {'read_only': True},
            'username': {'min_length': 5, 'required': True},
            'email':    {'required': True},
            'password': {'min_length': 8, 'write_only': True},
        }

    def validate(self, attrs):
        # XSS Schutz für Textfelder
        fields_to_validate = ['username', 'email']
        for field in fields_to_validate:
            if attrs.get(field):
                attrs[field] = bleach.clean(attrs[field])

        # Passwort Validierung – kein bleach, Sonderzeichen müssen erlaubt bleiben !
        password = attrs.get('password', '')
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Mindestens ein Großbuchstabe erforderlich.")
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Mindestens ein Kleinbuchstabe erforderlich.")
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError("Mindestens eine Zahl erforderlich.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Mindestens ein Sonderzeichen erforderlich.")

        return attrs


    def create(self, validated_data):
        # create_user() hasht das Passwort – niemals User.objects.create() direkt nutzen
        # sonst landet es im Klartext in der Datenbank
        # Token wird automatisch via post_save-Signal in models.py erstellt
        user = User.objects.create_user(**validated_data)
        return user








class UserPublicSerializer(serializers.ModelSerializer):        # -> für öffentliche Profilansicht (nur-lesen)

    class Meta:
        model  = User
        fields = ['username', 'profile_picture']

        extra_kwargs = {
            'username':        {'read_only': True},
            'profile_picture': {'read_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):      # -> für User Profil

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture', 'password']

        extra_kwargs = {
            'id':         {'read_only': True},
            'first_name': {'required': False},
            'last_name':  {'required': False},
            'password':   {'min_length': 8, 'write_only': True, 'required': False},
        }

    def validate(self, attrs):
        # XSS Schutz für Textfelder
        fields_to_validate = ['username', 'email', 'first_name', 'last_name']
        for field in fields_to_validate:
            if attrs.get(field):
                attrs[field] = bleach.clean(attrs[field])

        # Passwort nur validieren wenn es mitgeschickt wird
        password = attrs.get('password')
        if password:
            if not re.search(r'[A-Z]', password):
                raise serializers.ValidationError("Mindestens ein Großbuchstabe erforderlich.")
            if not re.search(r'[a-z]', password):
                raise serializers.ValidationError("Mindestens ein Kleinbuchstabe erforderlich.")
            if not re.search(r'[0-9]', password):
                raise serializers.ValidationError("Mindestens eine Zahl erforderlich.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise serializers.ValidationError("Mindestens ein Sonderzeichen erforderlich.")

        return attrs

    def update(self, instance, validated_data):
        # Passwort separat behandeln – set_password() hasht es korrekt
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        # alle anderen Felder normal updaten
        return super().update(instance, validated_data)