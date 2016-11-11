from storage.models import File
from rest_framework import serializers

class FileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = File
        fields = ('id', 'file', 'filename', 'created', 'owner')