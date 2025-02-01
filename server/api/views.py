from rest_framework.views import APIView
from rest_framework.response import Response
from googletrans import Translator
from .models import FAQ, Translation, Language
from .serializers import FAQSerializer, TranslatedFAQSerializer

class FAQListView(APIView):
    def get(self, request, *args, **kwargs):
        lang_code = request.query_params.get('lang', 'en')
        
        # If language is 'en' or not provided, use the original FAQ data
        if lang_code == 'en' or not lang_code:
            faqs = FAQ.objects.all()
            serializer = FAQSerializer(faqs, many=True)
            return Response(serializer.data)
        
        # Handle translations
        try:
            language = Language.objects.get(code=lang_code)
        except Language.DoesNotExist:
            translator = Translator()
            try:
                translator.translate('Test', src='en', dest=lang_code)
                language = Language.objects.create(code=lang_code)
            except Exception as e:
                language = None  

        faqs = FAQ.objects.all()
        translated_faqs = []

        # Check for translations
        for faq in faqs:
            translation = None
            if language:
                translation = Translation.objects.filter(faq=faq, language=language).first()

            if translation:
                translated_faqs.append({
                    'question': translation.question,
                    'answer': translation.answer,
                })
            else:
                translated_faqs.append({
                    'question': faq.question,
                    'answer': faq.answer,
                })

        # Use the TranslatedFAQSerializer for the translated FAQ response
        serializer = TranslatedFAQSerializer(translated_faqs, many=True)
        return Response(serializer.data)
