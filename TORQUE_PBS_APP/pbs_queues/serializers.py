from rest_framework import serializers


class QueueSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=100)
    state_count = serializers.CharField(required=False, max_length=100)
    Transit = serializers.IntegerField()
    Queued = serializers.IntegerField()
    Held = serializers.IntegerField()
    Waiting = serializers.IntegerField()
    Running = serializers.IntegerField()
    Exiting = serializers.IntegerField()
    Complete = serializers.IntegerField()
    started = serializers.BooleanField()
    enabled = serializers.BooleanField()
    resources_default_nodes = serializers.IntegerField()
    resources_default_walltime = serializers.CharField(required=False, max_length=100)
    queue_type = serializers.CharField(required=False, max_length=100)
    mtime = serializers.IntegerField()
    total_jobs = serializers.IntegerField()
    # absolute_url = serializers.CharField(required=False, max_length=100)
    # acl_users = serializers.CharField(required=False, max_length=100)
    # acl_user_enable = serializers.CharField(required=False, max_length=100)
