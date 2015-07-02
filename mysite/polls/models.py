import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question)

    choice_text = models.CharField(max_length=200)  #jennifer
    votes = models.IntegerField(default=0)  ## TODO refactor = votes and other misnomers


    #jennifer TODO populate the same answers about ASSOCIATION IF it is
    #a broad relationship type
    """
    "Are definitely associated"/>
  <cml:radio value="speculative" label="Are speculatively associated"/>
  <cml:radio value="negative" label="Are not associated"/>
  <cml:radio value="false" label="No claim of association made"/>
    """
    def __unicode__(self):
        return self.choice_text
