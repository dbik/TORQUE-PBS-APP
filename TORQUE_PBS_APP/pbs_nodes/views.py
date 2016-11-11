from utils import NodeInstance
from serializers import NodeSerializer

from permissions import IsOwner

from pbs_servers.utils import ServerInstance

from rest_framework import generics, permissions

import json
from django.http import HttpResponse
from rest_framework.response import Response


class NodeList(generics.ListAPIView):

    queryset = NodeInstance
    serializer_class = NodeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def list(self, request, format=None):
        # if 'username' not in request.session:
        #     return Response("User not found")
        # else:
        #Job_Owner = request.session['username']
        list = []
        node_list = ServerInstance().node_list()
        for node in node_list:
            serializer = NodeSerializer(node)
            list.append(serializer.data)
        return Response(list)
        # if format == 'json':
        #     return HttpResponse(json.dumps(json_data), content_type="application/json")
        # else:
        #     return HttpResponse(json.dumps(json_data), content_type="application/json")
        #     #return Response(data=list)

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
    #         list = []
    #         node_list = ServerInstance().node_list()
    #         for node in node_list:
    #             serializer = NodeSerializer(node)
    #             list.append(serializer.data)
    #         json_data['data'] = list
    #     if format == 'json':
    #         return HttpResponse(json.dumps(json_data), content_type="application/json")
    #     else:
    #         return HttpResponse(json.dumps(json_data), content_type="application/json")
    #         #return Response(data=list)


class NodeDetail(generics.RetrieveAPIView):
    def get(self, request, pk, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            cpu_per_job_per_node_list = []
            Job_Owner = request.session['username']
            node_name = ''
            node_names_list = []
            all_node_list = ServerInstance().node_list()  # Get a list with all nodes
            for node in all_node_list:  # Fill a list with node names and node names without '-'
                node_names_list.append({'node_name': node.name, 'clear_node_name': node.name.replace('-', '')})
            for item in node_names_list:  # Search the list with node names and node names without '-'
                if str(pk) == item[
                    'clear_node_name']:  # If url node name equals list's clear_node_name, set the proper node name
                    node_name = item['node_name']

            node_list = ServerInstance().node_list(node_name)  # Get specific node
            node = node_list[0]
            serializer = NodeSerializer(node)
            cpu_per_job_per_node_list.append(serializer.data)

            json_data['data'] = cpu_per_job_per_node_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=cpu_per_job_per_node_list)


class UserCPUPerJobsPerNode(generics.RetrieveAPIView):
    def get(self, request, pk, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            cpu_per_job_per_node_list = []
            Job_Owner = request.session['username']
            node_name = ''
            node_names_list = []
            all_node_list = ServerInstance().node_list()  # Get a list with all nodes
            for node in all_node_list:  # Fill a list with node names and node names without '-'
                node_names_list.append({'node_name': node.name, 'clear_node_name': node.name.replace('-', '')})
            for item in node_names_list:  # Search the list with node names and node names without '-'
                if str(pk) == item[
                    'clear_node_name']:  # If url node name equals list's clear_node_name, set the proper node name
                    node_name = item['node_name']

            node_list = ServerInstance().node_list(node_name)  # Get specific node
            node = node_list[0]
            node_job_list = node.jobs
            # torque_version = "old"
            for node_job in node_job_list:
                check = 0
                print node_job
                cpu_id, job = node_job.split('/')
                job_id, host = job.split('.')

                print cpu_id
                if '-' in cpu_id:
                    cpu_id_1, cpu_id_2 = cpu_id.split('-')
                    cpu_id_1 = int(cpu_id_1)
                    cpu_id_2 = int(cpu_id_2)
                    cpu_id = cpu_id_2 - cpu_id_1 + 1
                else:
                    cpu_id = 1
                print "CPUs: %d" % cpu_id
                job_id = int(job_id)

                cpu_per_job_per_node_list.append({'job': job_id, 'cpu': cpu_id})

                # support Torque 6

                # print cpu_id
                # if '-' in cpu_id:
                #     torque_version = "new"
                #     cpu_id_1, cpu_id_2 = cpu_id.split('-')
                #     cpu_id_1 = int(cpu_id_1)
                #     cpu_id_2 = int(cpu_id_2)
                #     cpu_id = cpu_id_2 - cpu_id_1 + 1
                #     print "torque 6: %d" % cpu_id
                # else:
                #     torque_version = "old"
                #     cpu_id = int(cpu_id)
                #     print "torque 4: %d" % cpu_id
                # job_id = int(job_id)
                # for job in cpu_per_job_per_node_list:
                #     if torque_version == "old":
                #         if job['job'] == job_id:
                #             job['cpu'] += 1
                #             check = 1
                #         cpu_per_job_per_node_list.append({'job' : job_id, 'cpu' : job['cpu']})
                #     else:
                #         job['cpu'] = cpu_id
                #         cpu_per_job_per_node_list.append({'job' : job_id, 'cpu' : cpu_id})
                #         check = 1
                # if check == 0:
                #     if torque_version == "old":
                #         cpu_per_job_per_node_list.append({'job' : job_id, 'cpu' : 1})
                #     else:
                #         cpu_per_job_per_node_list.append({'job' : job_id, 'cpu' : cpu_id})
            print cpu_per_job_per_node_list
            json_data['data'] = cpu_per_job_per_node_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=cpu_per_job_per_node_list)


class NpPerNCPUPerNode(generics.RetrieveAPIView):
    def get(self, request, pk, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            cpu_per_job_per_node_list = []
            Job_Owner = request.session['username']
            node_name = ''
            node_names_list = []
            all_node_list = ServerInstance().node_list()  # Get a list with all nodes
            for node in all_node_list:  # Fill a list with node names and node names without '-'
                node_names_list.append({'node_name': node.name, 'clear_node_name': node.name.replace('-', '')})
            for item in node_names_list:  # Search the list with node names and node names without '-'
                if str(pk) == item[
                    'clear_node_name']:  # If url node name equals list's clear_node_name, set the proper node name
                    node_name = item['node_name']

            node_list = ServerInstance().node_list(node_name)  # Get specific node
            node = node_list[0]
            node_np = int(node.np)
            node_ncpus = int(node.ncpus)
            cpu_per_job_per_node_list.append({'cpu_type': 'virtual cpu', 'cpu_num': node_np})
            cpu_per_job_per_node_list.append({'cpu_type': 'real cpu', 'cpu_num': node_ncpus})

            json_data['data'] = cpu_per_job_per_node_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=cpu_per_job_per_node_list)


class NodePerState(generics.RetrieveAPIView):
    def get(self, request, format=None):
        json_data = {
            'success': True,
            'data': {},
            'msg': 'User queue list'
        }
        if 'username' not in request.session:
            json_data['data'] = "User not found"
        else:
            cpu_per_job_per_node_list = []
            node_list = ServerInstance().node_list()
            for node in node_list:
                check = 0
                for item in cpu_per_job_per_node_list:
                    if node.state == item['state']:
                        item['value'] += 1
                        check = 1
                if check == 0:
                    cpu_per_job_per_node_list.append({'state': node.state, 'value': 1})

            json_data['data'] = cpu_per_job_per_node_list
        if format == 'json':
            return HttpResponse(json.dumps(json_data), content_type="application/json")
        else:
            return Response(data=cpu_per_job_per_node_list)