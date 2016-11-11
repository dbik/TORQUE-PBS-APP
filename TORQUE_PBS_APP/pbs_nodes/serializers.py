from rest_framework import serializers

class NodeSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=100)
    jobs = serializers.CharField(required=False, max_length=100)
    gres = serializers.CharField(required=False, max_length=100)
    nusers = serializers.IntegerField()
    idletime = serializers.IntegerField()
    rectime = serializers.IntegerField()
    sessions = serializers.CharField(required=False, max_length=100)
    physmem = serializers.CharField(required=False, max_length=100)
    totmem = serializers.CharField(required=False, max_length=100)
    netload = serializers.IntegerField()
    loadave = serializers.CharField(required=False, max_length=100)
    uname = serializers.CharField(required=False, max_length=100)
    opsys = serializers.CharField(required=False, max_length=100)
    nsessions = serializers.IntegerField()
    ncpus = serializers.IntegerField()
    availmem = serializers.CharField(required=False, max_length=100)
    varattr = serializers.CharField(required=False, max_length=100)
    #mom_manager_port = serializers.IntegerField()
    ntype = serializers.CharField(required=False, max_length=100)
    state = serializers.CharField(required=False, max_length=100)
    mom_service_port = serializers.IntegerField()
    np = serializers.IntegerField()
    #gpus = serializers.IntegerField()