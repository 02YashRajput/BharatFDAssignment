from rest_framework import serializers
from .models import FAQ, Translation

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['question', 'answer']

class FAQSerializer(serializers.ModelSerializer):
    translations = TranslationSerializer(many=True, read_only=True)
    
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'translations']

