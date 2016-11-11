from django.db import models

import os


def get_upload_path(instance, filename):
    # return os.path.join("user_%d" % instance.owner.id, "car_%s" % instance.slug, filename)
    return os.path.join('media/storage/%s/%s' % (instance.owner.username, filename))


class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=1024)
    file = models.FileField(upload_to=get_upload_path, null=True)
    owner = models.ForeignKey('users.CustomUser', related_name='files')

    def __str__(self):
        #return self.filename
        return self.id

    def getOwner(self):
        return self.owner