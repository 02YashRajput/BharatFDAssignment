from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  
    def save(self, *args, **kwargs):
      """Override save to automatically create translations for all FAQs when a new language is added."""
      is_new_language = self._state.adding 

      super().save(*args, **kwargs)  

      if is_new_language:
          translator = Translator()

          all_faqs = FAQ.objects.all()  
          for faq in all_faqs:
              translated_question = translator.translate(faq.question, src='en', dest=self.code).text
              translated_answer = translator.translate(faq.answer, src='en', dest=self.code).text

              
              Translation.objects.create(
                  faq=faq,
                  language=self,
                  question=translated_question,
                  answer=translated_answer
              )
    
    
class FAQ(models.Model):
  question = models.TextField()
  answer = RichTextField()  
  created_at = models.DateTimeField(auto_now_add=True)
  
  
  def save(self, *args, **kwargs):
    """Override save to automatically translate question and answer fields."""
    super().save(*args, **kwargs)  
    
    translator = Translator()
    existing_languages = set([t.language.code for t in Translation.objects.filter(faq=self)])

    all_languages = Language.objects.all()

    for lang in all_languages:
        if lang.code not in existing_languages:
            translated_question = translator.translate(self.question,src='en', dest=lang.code).text
            translated_answer = translator.translate(self.answer,src='en', dest=lang.code).text
            
            Translation.objects.create(
                faq=self,
                language=lang,
                question=translated_question,
                answer=translated_answer
            )
    
    
class Translation(models.Model):
  faq = models.ForeignKey(FAQ, on_delete=models.CASCADE,related_name='translations')
  language = models.ForeignKey(Language, on_delete=models.CASCADE)
  question = models.TextField()
  answer = RichTextField()
  created_at = models.DateTimeField(auto_now_add=True)

  