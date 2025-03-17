from django.db import models
from django.contrib.auth.models import User
CHOICES_TOPIC = [
    ("Question", "Question"),
    ("Job Listing", "Job Listing"),
    ("Tip", "Tip"),
    ("Shitpost", "Shitpost"),
    ("Discussion", "Discussion"),
    ("News", "News"),
    ("Event", "Event"),
]

CHOICES_INDUSTRY = [
    ("Technology-IT", "Technology & IT"),
    ("Business-Finance", "Business & Finance"),
    ("Engineering", "Engineering"),
    ("Healthcare-Life Sciences", "Healthcare & Life Sciences"),
    ("Education-Research", "Education & Research"),
    ("Design", "Design"),
    ("Legal-Compliance", "Legal & Compliance"),
    ("Sciences", "Sciences"),
    ("Government-Public Services", "Government & Public Services"),
]
INDUSTRY_DICT = dict(CHOICES_INDUSTRY)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=10000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    topic_tag = models.CharField(max_length=50, choices=CHOICES_TOPIC, default=("None", "None"))
    industry_tag = models.CharField(max_length=50, choices=CHOICES_INDUSTRY, default=("None", "None"))



    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    depth = models.PositiveIntegerField(default=0)

    def is_reply(self):
        return self.parent is not None