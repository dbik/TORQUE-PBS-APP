from utils import QueueInstance
from serializers import QueueSerializer

from pbs_servers.utils import ServerInstance

from rest_framework import generics, permissions
from rest_framework.response import Response

from permissions import IsOwner
from django.http import HttpResponse

import json


class QueueList(generics.ListAPIView):
    queryset = QueueInstance
    serializer_class = QueueSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def list(self, request, format=None):
        # if 'username' not in request.session:
        #     return Response("User not found")
        # else:
        # Job_Owner = request.session['username']
        queue_list = []
        user_queue_list = ServerInstance().queue_list()
        for queue in user_queue_list:
            serializer = QueueSerializer(queue)
            queue_list.append(serializer.data)
        return Response(queue_list)

    # def list(self, request, format=None):
    #     json_data = {
    #         'success': True,
    #         'data': {},
    #         'msg': 'User queue list'
    #     }
    #     if 'username' not in request.session:
    #         json_data['data'] = "User not found"
    #     else:
    #         Job_Owner = request.session['username']
    #         user_queues_list = []
    #         user_queue_list = ServerInstance().queue_list()
    #         for user_queue_instance in user_queue_list:
    #             serializer = QueueSerializer(user_queue_instance)
    #             user_queues_list.append(serializer.data)
    #         json_data['data'] = user_queues_list
    #     if format == 'json':
    #         return HttpResponse(json.dumps(json_data), content_type="application/json")
    #     else:
    #         return Response(data=user_queues_list)


class UserQueues(generics.ListAPIView):
    def list(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            check = 0
            user_queues_list = []
            Job_Owner = request.session['username']
            user_job_instances_list = ServerInstance().job_list(Job_Owner)
            for user_job_instance in user_job_instances_list:
                for user_queue in user_queues_list:
                    if user_queue['queue'] == user_job_instance.queue:
                        user_queue['jobs'] += 1
                        check = 1
                        continue
                if check == 0:
                    user_queues_list.append({'queue': user_job_instance.queue, 'jobs': 1})
                check = 0
            json_data['data'] = user_queues_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=user_queues_list)


class UserPerAllJobsPerQueue(generics.RetrieveAPIView):
    def get(self, request, pk, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            user_jobs = 0
            rest_jobs = 0
            user_all_job_queue_list = []
            Job_Owner = request.session['username']
            all_job_list = ServerInstance().job_list()
            for job in all_job_list:
                if job.queue == str(pk):
                    temp_Job_Owner, temp_host = job.Job_Owner.split('@')
                    if temp_Job_Owner == Job_Owner:
                        user_jobs += 1
                    else:
                        rest_jobs += 1
            user_all_job_queue_list.append({'user': Job_Owner, 'jobs': user_jobs})
            user_all_job_queue_list.append({'user': 'rest', 'jobs': rest_jobs})

            json_data['data'] = user_all_job_queue_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=user_all_job_queue_list)


class UserJobsPerQueuePerJobState(generics.RetrieveAPIView):
    def get(self, request, pk, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            Job_Owner = request.session['username']
            user_job_list = ServerInstance().job_list(Job_Owner)
            completed_user_jobs = 0
            running_user_jobs = 0
            holded_user_jobs = 0
            queued_user_jobs = 0
            for job in user_job_list:
                if job.queue == str(pk):
                    if job.job_state == 'C':
                        completed_user_jobs += 1
                    elif job.job_state == 'R':
                        running_user_jobs += 1
                    elif job.job_state == 'H':
                        holded_user_jobs += 1
                    elif job.job_state == 'Q':
                        queued_user_jobs += 1

            user_jobs_list = []
            user_jobs_list.append({'state': 'C', 'value': completed_user_jobs})
            user_jobs_list.append({'state': 'R', 'value': running_user_jobs})
            user_jobs_list.append({'state': 'H', 'value': holded_user_jobs})
            user_jobs_list.append({'state': 'Q', 'value': queued_user_jobs})

            json_data['data'] = user_jobs_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=user_jobs_list)


class AllJobsPerQueuePerJobState(generics.RetrieveAPIView):
    def get(self, request, pk, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            Job_Owner = request.session['username']
            job_list = ServerInstance().job_list()
            completed_user_jobs = 0
            running_user_jobs = 0
            holded_user_jobs = 0
            queued_user_jobs = 0
            for job in job_list:
                if job.queue == str(pk):
                    if job.job_state == 'C':
                        completed_user_jobs += 1
                    elif job.job_state == 'R':
                        running_user_jobs += 1
                    elif job.job_state == 'H':
                        holded_user_jobs += 1
                    elif job.job_state == 'Q':
                        queued_user_jobs += 1

            jobs_list = []
            jobs_list.append({'state': 'C', 'value': completed_user_jobs})
            jobs_list.append({'state': 'R', 'value': running_user_jobs})
            jobs_list.append({'state': 'H', 'value': holded_user_jobs})
            jobs_list.append({'state': 'Q', 'value': queued_user_jobs})

            json_data['data'] = jobs_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=jobs_list)


class QueueDetail(generics.RetrieveAPIView):
    def get(self, request, pk, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User detail'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            Job_Owner = request.session['username']
            user_queues_list = []
            queue_instances_list = ServerInstance().queue_list(str(pk))
            for queue in queue_instances_list:
                serializer = QueueSerializer(queue)
                user_queues_list.append(serializer.data)
            json_data['data'] = user_queues_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=user_queues_list)