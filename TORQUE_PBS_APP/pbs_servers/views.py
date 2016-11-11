from utils import ServerInstance
from serializers import ServerSerializer
#from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.response import Response

from rest_framework.decorators import api_view
#from django.contrib.auth import authenticate, login, logout
import json
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404

import os
import pwd
import grp
import pam
import subprocess


def report_ids(msg):
    print 'uid, gid = %d, %d; %s' % (os.getuid(), os.getgid(), msg)


def demote_and_create_dir(user_uid, user_gid, username):
    def result():
        report_ids('starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
        report_ids('finished demotion')
        path = 'jobs/' + username + '/'
        print "Path: ", path
        if not os.path.exists(path):
            print "Path: ", path, " doesn\'t exists!"
            os.makedirs(path)
            print "Path created!!"

    return result


@api_view(['POST'])
def user_login(request):
    json_data = {
        'success': False,
        'data': {},
        'msg': {},
    }
    req_username = request.POST['username']  # for check boxes: username = request.POST.get('username', False)
    req_password = request.POST['password']
    print 'Username: ', req_username
    print 'Password: ', req_password

    p = pam.pam()

    linux_account_exist = p.authenticate(req_username, req_password)
    print 'linux_account_exist: ', linux_account_exist
    if linux_account_exist:
        print 'User authentication...'
        user = authenticate(username=req_username, password=req_password)
        if user is not None:
            print 'User authentication succesfull!'
            if user.is_active:
                print 'User is active!'
                print 'Logging in...'
                login(request, user)
                request.session['username'] = user.username
                request.session['user_id'] = user.id
                print 'Logged in!'
                json_data['success'] = True
                json_data['data'] = (user.username, user.is_superuser)
                json_data['msg'] = 'Succesfull log in: %s!' % (user.username,)
            else:
                # Return a 'disabled account' error message
                print 'User account is not active!'
                json_data['data'] = (user.username)
                json_data['msg'] = 'Unsuccesfull log in! %s account disabled!' % (user.username,)
        else:
            print 'User account doesn\'t exist in application database'
            print 'User account creation...'
            user = User.objects.create_user(req_username, 'testemail@gmail.com', req_password)
            if user is not None:
                print 'User account created!!!'
                print 'User authentication...'
                user = authenticate(username=req_username, password=req_password)
                if user is not None:
                    print 'User authentication succesfull!'
                    if user.is_active:
                        print 'User is active!'
                        print 'Logging In...'
                        login(request, user)
                        request.session['username'] = user.username
                        request.session['user_id'] = user.id
                        print 'Creating user directory...'
                        uid = pwd.getpwnam(request.session['username']).pw_uid
                        gid = grp.getgrnam(request.session['username']).gr_gid
                        print uid
                        # process = subprocess.Popen(
                        #    args=['echo', 'Start subprocess: demote_and_create_dir'], preexec_fn=demote_and_create_dir(uid, uid, request.session['username'])
                        # )
                        path = 'jobs/' + request.session['username'] + '/'
                        print "Path: ", path
                        if not os.path.exists(path):
                            print "Path: ", path, " doesn\'t exists!"
                            os.makedirs(path)
                            print "Path created!!"
                            print "Giving user permissions to path..."
                            os.chown(path, uid, gid)
                            print "User permissions ok!"
                        print 'User directory created!'
                        json_data['success'] = True
                        json_data['data'] = (user.username)
                        json_data['msg'] = 'Succesfull log in: %s!' % (user.username,)
                else:
                    print 'Error in 2nd level authentication!'
                    json_data['data'] = ''
                    json_data['msg'] = 'Internal system error!!!'
            else:
                print 'Error in user account creation!'
                json_data['data'] = ''
                json_data['msg'] = 'Could not register user in application\'s database!\nSystem error!!!'
    else:
        json_data['data'] = 'Cannot log in'
        json_data[
            'msg'] = 'Invalid username/password or\n user account doesn\'t exist in system. Contact with sys-admin!'
    return HttpResponse(json.dumps(json_data), content_type="application/json")


@api_view(['POST'])
def user_logout(request):
    '''
    #Session vars
    print request.session.keys()
    if(request.session['_auth_user_id']):
        print request.session['_auth_user_id']
    if(request.session['_auth_user_backend']):
        print request.session['_auth_user_backend']
    '''
    json_data = {
        'success': False,
        'data': {},
        'msg': {},
    }
    logout(request)
    json_data['success'] = True
    json_data['msg'] = 'Logged out!!!'
    return HttpResponse(json.dumps(json_data), content_type="application/json")


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ServerList(generics.ListAPIView):
    serializer_class = ServerSerializer

    def list(self, request, format=None):
        print format
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Server info'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            server_list = []
            server_instance = ServerInstance()
            serializer = ServerSerializer(server_instance)
            server_list.append(serializer.data)
            json_data['data'] = server_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=server_list)


class ServerDetail(generics.RetrieveAPIView):
    serializer_class = ServerSerializer


class RQALLJobsPerUser(generics.ListAPIView):
    def list(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Jobs per user list'
        }
        all_job_instances_list = ServerInstance().job_list()
        if len(all_job_instances_list) > 0:
            # print len(all_job_instances_list)
            check = 0
            jobs_per_user_list = []
            jobs_per_user_list.append(
                {'Job_Owner': all_job_instances_list[0].Job_Owner, 'r_jobs': 0, 'q_jobs': 0, 'all_jobs': 0})
            for job in all_job_instances_list:
                for listed_job in jobs_per_user_list:
                    if job.Job_Owner == listed_job['Job_Owner']:
                        listed_job['all_jobs'] += 1
                        if job.job_state == 'R':
                            listed_job['r_jobs'] += 1
                        elif job.job_state == 'Q':
                            listed_job['q_jobs'] += 1
                        check = 1
                        continue
                if check == 0:
                    if job.job_state == 'R':
                        jobs_per_user_list.append({'Job_Owner': job.Job_Owner, 'r_jobs': 1, 'q_jobs': 0, 'all_jobs': 1})
                    elif job.job_state == 'Q':
                        jobs_per_user_list.append({'Job_Owner': job.Job_Owner, 'r_jobs': 0, 'q_jobs': 1, 'all_jobs': 1})

                check = 0
            json_data['data'] = jobs_per_user_list

            if format == 'json':
                return HttpResponse(json.dumps(json_data), content_type="application/json")
            else:
                return Response(data=jobs_per_user_list)
        else:
            return Response(data="No jobs in server")


class AllQueues(generics.ListAPIView):
    def list(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            queues_list = []
            queue_instances_list = ServerInstance().queue_list()
            for queue in queue_instances_list:
                queues_list.append({'queue': queue.name, 'r_jobs': queue.Running, 'q_jobs': queue.Queued})
            json_data['data'] = queues_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=queues_list)


class GetNodeNamesState(generics.RetrieveAPIView):
    def get(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Nof nodes'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            list = []
            node_instances_list = ServerInstance().node_list()
            for node in node_instances_list:
                list.append({'node_name': node.name, 'node_state': node.state})
            json_data['data'] = list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=list)


class GetnofNodes(generics.RetrieveAPIView):
    def get(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Nof nodes'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            list = []
            node_instances_list = ServerInstance().node_list()
            nof_nodes = len(node_instances_list)
            list.append({'nof_nodes': nof_nodes})
            json_data['data'] = list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=list)


class GetMaxCPUs(generics.RetrieveAPIView):
    def get(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Nof nodes'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            list = []
            node_instances_list = ServerInstance().node_list()
            max_cpus = 0
            for node in node_instances_list:
                if node.np > max_cpus:
                    max_cpus = node.np
            list.append({'max_cpus': max_cpus})
            json_data['data'] = list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=list)


class UsageTotals(generics.RetrieveAPIView):
    def get(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'UsageTotals'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            usage_totals_list = []
            node_instances_list = ServerInstance().node_list()
            all_nodes = 0
            free_nodes = 0
            for node in node_instances_list:
                all_nodes += 1
                if node.state == 'free':
                    free_nodes += 1

            node_instances_list = ServerInstance().node_list()
            all_cpus = 0
            free_cpus = 0
            used_cpus = 0
            down_cpus = 0
            for node in node_instances_list:
                all_cpus += int(node.np)
                used_cpus += len(node.jobs)
                if node.state == 'down':
                    down_cpus += int(node.np)
            free_cpus = all_cpus - used_cpus - down_cpus

            job_instances_list = ServerInstance().job_list()
            running_jobs = 0
            queued_jobs = 0
            for job in job_instances_list:
                if job.job_state == 'R':
                    running_jobs += 1
                elif job.job_state == 'Q':
                    queued_jobs += 1

            usage_totals_list.append(
                {'id': 1, 'free_nodes': free_nodes, 'all_nodes': all_nodes, 'free_cpu': free_cpus, 'all_cpu': all_cpus,
                 'running_jobs': running_jobs, 'queued_jobs': queued_jobs})
            json_data['data'] = usage_totals_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=usage_totals_list)


class CPUSummary(generics.RetrieveAPIView):
    def get(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Nof nodes'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            cpu_sum_list = []
            node_instances_list = ServerInstance().node_list()
            all_cpus = 0
            free_cpus = 0
            used_cpus = 0
            for node in node_instances_list:
                all_cpus += int(node.np)
                used_cpus += len(node.jobs)
            free_cpus = all_cpus - used_cpus
            cpu_sum_list.append({'free_cpu': free_cpus, 'all_cpu': all_cpus})
            json_data['data'] = cpu_sum_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=cpu_sum_list)


class JobSummary(generics.RetrieveAPIView):
    def get(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Nof nodes'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            cpu_sum_list = []
            job_instances_list = ServerInstance().job_list()
            running_jobs = 0
            queued_jobs = 0
            for job in job_instances_list:
                if job.job_state == 'R':
                    running_jobs += 1
                elif job.job_state == 'Q':
                    queued_jobs += 1
            cpu_sum_list.append({'running_jobs': running_jobs, 'queued_jobs': queued_jobs})
            json_data['data'] = cpu_sum_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=cpu_sum_list)


class QtopNodes(generics.ListAPIView):
    def list(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'Node list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            nodes_list = []
            node_instances_list = ServerInstance().node_list()
            max_np = 0
            for node in node_instances_list:
                node_list = []  # init job id table for node
                temp_node_list = []  # init original job table for node
                np = int(node.np)
                if np > max_np:
                    max_np = np
                if node.state == 'free':
                    if node.jobs:
                        jobs_count = len(node.jobs)
                        temp_node_list = node.jobs
                        for item in temp_node_list:  # item = 0/230.jim-desktop
                            # 0-1/23.jim-SATELLITE-L50-B
                            # 2-3/24.jim-SATELLITE-L50-B
                            cpu, job = item.split("/")
                            if "-" in cpu:
                                initial_cpu, last_cpu = cpu.split("-")
                                initial_cpu = int(initial_cpu)
                                last_cpu = int(last_cpu)
                                diff = last_cpu - initial_cpu
                                i = 0
                                while i <= diff:
                                    job_id, host = job.split(".")
                                    node_list.append(job_id)
                                    i += 1
                            else:
                                job_id, host = job.split(".")
                                node_list.append(job_id)  # node_list now has only job ids: 230
                        free_cpu = int(node.np) - jobs_count
                        i = 0
                        while (i < free_cpu):
                            node_list.append('-')
                            i = i + 1
                    else:
                        cpus = int(node.np)
                        i = 0
                        while (i < cpus):
                            node_list.append('-')
                            i = i + 1
                else:
                    cpus = int(node.np)
                    i = 0
                    while (i < cpus):
                        node_list.append(node.state[0])
                        i = i + 1
                nodes_list.append(node_list)
            final_node_list = []
            ctr_1 = 0
            while (ctr_1 < max_np):
                res = '{"cpu":"' + str(ctr_1) + '"'
                ctr_2 = 0
                for node in nodes_list:
                    ctr_2 += 1
                    try:
                        if node:
                            if node[ctr_1]:
                                res += ', "jid_' + str(ctr_2 - 1) + '":"' + node[ctr_1] + '"'
                        else:
                            res += ', "jid_' + str(ctr_2 - 1) + '":""'
                    except:
                        res += ', "jid_' + str(ctr_2 - 1) + '":""'
                res += '}'
                res = json.loads(res)
                final_node_list.append(res)
                ctr_1 += 1
            json_data['data'] = final_node_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=final_node_list)