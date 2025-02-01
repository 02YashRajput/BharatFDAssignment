from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.response import Response
from googletrans import Translator
from .models import FAQ, Translation, Language
from .serializers import FAQSerializer, TranslatedFAQSerializer

class FAQListView(APIView):
    def get(self, request, *args, **kwargs):
        lang_code = request.query_params.get('lang', 'en')
        
        if lang_code == 'en' or not lang_code:
            cache_key = "faq_translations_en"
            cached_faqs = cache.get(cache_key)
            if cached_faqs:
                return Response(cached_faqs)
            faqs = FAQ.objects.all()
            serializer = FAQSerializer(faqs, many=True)
            cache.set(cache_key, serializer.data, timeout=None)  
            return Response(serializer.data)
        
        try:
            language = Language.objects.get(code=lang_code)
        except Language.DoesNotExist:
            translator = Translator()
            try:
                translator.translate('Test', src='en', dest=lang_code)
                language = Language.objects.create(code=lang_code)
            except Exception as e:
                language = None  
        cache_key = f"faq_translations_{lang_code}"
        cached_translations = cache.get(cache_key)

        if cached_translations:
            return Response(cached_translations)

        faqs = FAQ.objects.all()
        translated_faqs = []

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

        cache.set(cache_key, translated_faqs, timeout=None)

        serializer = TranslatedFAQSerializer(translated_faqs, many=True)
        return Response(serializer.data)