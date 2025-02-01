import pytest
from rest_framework.test import APIClient
from django.core.cache import cache
from googletrans import Translator
from api.models import FAQ, Language, Translation

@pytest.mark.django_db
def test_get_faqs_in_english():
    """
    Test retrieving FAQs in English without translation.
    """
    client = APIClient()

    # Create an FAQ
    FAQ.objects.create(question="What is Django?", answer="Django is a Python web framework.")

    # Clear cache to ensure fresh retrieval
    cache.clear()

    # Make GET request without language parameter (default 'en')
    response = client.get("/api/faqs/")

    # Check response status
    assert response.status_code == 200

    # Ensure FAQ is returned in English
    assert response.data[0]["question"] == "What is Django?"
    assert response.data[0]["answer"] == "Django is a Python web framework."

    # Check if data is cached
    cached_faqs = cache.get("faq_translations_en")
    assert cached_faqs is not None


@pytest.mark.django_db
def test_get_faqs_with_translation():
    """
    Test retrieving FAQs in a non-English language (e.g., French 'fr').
    """
    client = APIClient()

    # Create an FAQ
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a Python web framework.")

    # Add a language (French)
    language = Language.objects.create(code="fr")

    # Use Google Translate to get expected translation
    translator = Translator()
    translated_question = translator.translate(faq.question, src="en", dest="fr").text
    translated_answer = translator.translate(faq.answer, src="en", dest="fr").text

    # Store the translation in the database
    Translation.objects.create(faq=faq, language=language, question=translated_question, answer=translated_answer)

    # Clear cache
    cache.clear()

    # Make GET request for French FAQs
    response = client.get("/api/faqs/?lang=fr")

    # Check response status
    assert response.status_code == 200

    # Ensure response contains the translated FAQ
    assert response.data[0]["question"] == translated_question
    assert response.data[0]["answer"] == translated_answer

    # Check if data is cached
    cached_faqs = cache.get("faq_translations_fr")
    assert cached_faqs is not None


@pytest.mark.django_db
def test_get_faqs_with_nonexistent_language():
    """
    Test behavior when requesting FAQs in a language that doesn't exist.
    """
    client = APIClient()

    # Create an FAQ
    FAQ.objects.create(question="What is Django?", answer="Django is a Python web framework.")

    # Clear cache
    cache.clear()

    # Make GET request with an invalid language code
    response = client.get("/api/faqs/?lang=xyz")

    # Check response status
    assert response.status_code == 200  # Should still return data

    # Ensure response returns the original English FAQ (since translation doesn't exist)
    assert response.data[0]["question"] == "What is Django?"
    assert response.data[0]["answer"] == "Django is a Python web framework."
