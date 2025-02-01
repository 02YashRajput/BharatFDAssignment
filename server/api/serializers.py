from rest_framework import serializers
from .models import FAQ, Translation
class TranslatedFAQSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.CharField()




class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
