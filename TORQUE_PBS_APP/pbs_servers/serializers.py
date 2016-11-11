from rest_framework import serializers
#from django.contrib.auth.models import User
#
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     files = serializers.HyperlinkedRelatedField(many=True, view_name='file-detail', read_only=True)
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'email', 'files')


class ServerSerializer(serializers.Serializer):

    id = serializers.CharField(required=False, max_length=100)
    name = serializers.CharField(required=False, max_length=100)
    tcp_timeout = serializers.IntegerField(required=False, default=0)
    managers = serializers.CharField(required=False, max_length=100)
    keep_completed = serializers.IntegerField(required=False, default=0)
    poll_jobs = serializers.BooleanField()
    node_check_rate = serializers.IntegerField(required=False, default=0)
    job_stat_rate = serializers.IntegerField(required=False, default=0)
    scheduling = serializers.BooleanField()
    total_jobs = serializers.IntegerField(required=False, default=0)
    acl_hosts = serializers.CharField(required=False, max_length=100)
    moab_array_compatible = serializers.CharField(required=False, max_length=100)
    mom_job_sync = serializers.BooleanField()
    state_count = serializers.CharField(required=False, max_length=100)
    default_queue = serializers.CharField(required=False, max_length=100)
    server_state = serializers.CharField(required=False, max_length=100)
    operators = serializers.CharField(required=False, max_length=100)
    net_counter = serializers.CharField(required=False, max_length=100)
    next_job_number = serializers.IntegerField(required=False, default=0)
    submit_hosts = serializers.CharField(required=False, max_length=100)
    #scheduler_iteration = serializers.IntegerField(required=False, default=0)
    mail_from = serializers.CharField(required=False, max_length=100)
    log_events = serializers.CharField(required=False, max_length=100)
    pbs_version = serializers.CharField(required=False, max_length=100)
    allow_node_submit = serializers.BooleanField()
    Transit = serializers.IntegerField()
    Queued = serializers.IntegerField()
    Held = serializers.IntegerField()
    Waiting = serializers.IntegerField()
    Running = serializers.IntegerField()
    Exiting = serializers.IntegerField()
    Complete = serializers.IntegerField()