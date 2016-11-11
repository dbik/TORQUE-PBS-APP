from django.shortcuts import get_object_or_404

from storage.models import File
from storage.serializers import FileSerializer
from rest_framework import generics
import json, os
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
import pwd
import grp

from storage.permissions import IsOwner


class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def create(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'File uploaded successfully',
            'filename': request.data['filename']
        }
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        json_data['data'] = serializer.data

        path = 'media/storage/' + self.request.user['username'] + '/'
        uid = pwd.getpwnam(self.request.user['username']).pw_uid
        gid = grp.getgrnam(self.request.user['username']).gr_gid

        for root, dirs, files in os.walk(path):
            for momo in dirs:
                os.chown(os.path.join(root, momo), uid, gid)
            for momo in files:
                os.chown(os.path.join(root, momo), uid, gid)
        os.chown(path, uid, gid)
        print "User permissions ok!"

        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return HttpResponse(json.dumps(json_data), content_type="application/json")

    def list(self, request, format=None):
        json_data = {
            'success': True,
            'data': {""},
            'msg': 'File info'
        }
        queryset = File.objects.all().filter(owner=request.user)#(owner=request.session['user_id'])
        serializer = FileSerializer(queryset, many=True)
        json_data['data'] = serializer.data
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=serializer.data)


class FileDetail(generics.RetrieveDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_object(self):
        file = get_object_or_404(File, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, file)
        return file

    def get(self, request, pk, format=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        #serializer = FileSerializer(file)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        try:
            file = File.objects.get(pk=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(file)
        filename = serializer.data.get('filename')
        os.remove(serializer.data.get('file'))
        file.delete()