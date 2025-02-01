import pytest
from api.models import Language, FAQ, Translation
from django.core.cache import cache
from unittest.mock import patch
from googletrans import Translator

@pytest.mark.django_db
def test_faq_auto_translates_with_google_trans():

    language = Language.objects.create(code="hi")

    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")

    assert FAQ.objects.filter(id=faq.id).exists(), "FAQ was not created successfully"


    translation = Translation.objects.filter(faq=faq, language=language).first()

    assert translation is not None, "Translation was not created successfully"


    translator = Translator()
    expected_question = translator.translate("What is Django?", src='en', dest='hi').text
    expected_answer = translator.translate("Django is a web framework.", src='en', dest='hi').text

    assert translation.question == expected_question, f"Expected: {expected_question}, Got: {translation.question}"
    assert translation.answer == expected_answer, f"Expected: {expected_answer}, Got: {translation.answer}"



@pytest.mark.django_db
def test_faq_translation_after_adding_language():
    faq = FAQ.objects.create(question="How does Python work?", answer="Python is an interpreted language.")

    assert FAQ.objects.filter(id=faq.id).exists(), "FAQ was not created successfully"

    language = Language.objects.create(code="bn")

    translation = Translation.objects.filter(faq=faq, language=language).first()
    
    assert translation is not None, "Translation was not created successfully"

    translator = Translator()
    expected_question = translator.translate("How does Python work?", src='en', dest='bn').text
    expected_answer = translator.translate("Python is an interpreted language.", src='en', dest='bn').text

    assert translation.question == expected_question, f"Expected: {expected_question}, Got: {translation.question}"
    assert translation.answer == expected_answer, f"Expected: {expected_answer}, Got: {translation.answer}"
