from flask import url_for
from server import db

class Post(db.Document):
    title = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
    }