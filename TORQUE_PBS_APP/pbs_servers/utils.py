from PBSQuery import PBSQuery
import pbs

from pbs_queues.utils import QueueInstance
from pbs_nodes.utils import NodeInstance
#from jobs_api.instance import JobInstance


class ServerInstance(object):
    try:
        c = pbs.pbs_connect(str(pbs.pbs_default()))
    except BaseException:
        pass
    try:
        p = PBSQuery(str(pbs.pbs_default()))
    except BaseException:
        pass

    def __init__(self):
        info = self.p.get_serverinfo().items()[0]
        self.name = info[0]
        self.tcp_timeout = int(info[1]['tcp_timeout'][0])
        self.managers = info[1]['managers']
        self.keep_completed = int(info[1]['keep_completed'][0])
        self.poll_jobs = info[1]['poll_jobs'][0]
        self.node_check_rate = int(info[1]['node_check_rate'][0])
        self.job_stat_rate = int(info[1]['job_stat_rate'][0])
        self.scheduling = info[1]['scheduling'][0]
        self.total_jobs = int(info[1]['total_jobs'][0])
        self.acl_hosts = info[1]['acl_hosts']
        self.moab_array_compatible = info[1]['moab_array_compatible'][0]
        self.mom_job_sync = info[1]['mom_job_sync'][0]

        self.state_count = info[1]['state_count'][0]
        self.state_count = self.state_count[:-1]

        list = self.state_count.split(" ")
        for item in list:
            state, num = item.split(":")
            if state == 'Transit':
                self.Transit = num
            elif state == 'Queued':
                self.Queued = num
            elif state == 'Held':
                self.Held = num
            elif state == 'Waiting':
                self.Waiting = num
            elif state == 'Running':
                self.Running = num
            elif state == 'Exiting':
                self.Exiting = num
            elif state == 'Complete':
                self.Complete = num

        self.default_queue = info[1]['default_queue'][0]
        self.server_state = info[1]['server_state'][0]
        self.operators = info[1]['operators']
        self.net_counter = info[1]['net_counter'][0]
        self.next_job_number = int(info[1]['next_job_number'][0])
        #self.submit_hosts = info[1]['submit_hosts']
        # self.scheduler_iteration = int(info[1]['scheduler_iteration'][0])
        self.mail_from = info[1]['mail_from'][0]
        self.log_events = info[1]['log_events'][0]
        self.pbs_version = info[1]['pbs_version'][0]
        #self.allow_node_submit = info[1]['allow_node_submit'][0]

    def getnodes(self):
        return self.p.getnodes()

    def getnode(self, id):
        return self.p.getnode(id)

    def getqueues(self):
        return self.p.getqueues()

    def getqueue(self, id):
        return self.p.getqueue(id)

    def getjobs(self):
        return self.p.getjobs()

    def getjob(self, id):
        return self.p.getjob(id)

    def cpu_stats(self):
        node_data = self.getnodes()
        total = 0
        used = 0
        for k, n in node_data.items():
            if 'cluster' not in n['ntype']:
                continue
            if 'offline' in n['state'] or 'down' in n['state']:
                continue
            total += int(n['np'][0])
            try:
                used += len(n['jobs'])
            except:
                pass
        return used, total

    def acl_host_list(self):
        acl_hosts = self.acl_hosts
        acl_host_list = []
        for acl_host in acl_hosts:
            acl_host_list.append(acl_host)
        return acl_host_list

    # def submit_host_list(self):
    #     submit_hosts = self.submit_hosts
    #     submit_host_list = []
    #     for submit_host in submit_hosts:
    #         submit_host_list.append(submit_host)
    #     return submit_host_list

    def manager_list(self):
        managers = self.managers
        manager_list = []
        for manager in managers:
            manager_list.append(manager)
        return manager_list

    def operator_list(self):
        operators = self.operators
        operator_list = []
        for operator in operators:
            operator_list.append(operator)
        return operator_list

    # def job_list(self, usernames=None, job_id=None):
    #     job_list = []
    #     if job_id is None:
    #         data_list = self.getjobs()
    #         for d in data_list:
    #             id, host = d.split('.', 1)
    #             if usernames:
    #                 owner, host = data_list[d]['Job_Owner'][0].split('@')
    #                 if owner in usernames:
    #                     job_list.append(JobInstance(server=self, id=id, host=host, data=data_list[d]))
    #             else:
    #                 job_list.append(JobInstance(server=self, id=id, host=host, data=data_list[d]))
    #     else:
    #         data = self.getjob(job_id)
    #         if usernames:
    #             owner, host = data['Job_Owner'][0].split('@')
    #             if owner in usernames:
    #                 job_list.append(JobInstance(server=self, id=job_id, host=host, data=data))
    #         else:
    #             job_list.append(JobInstance(server=self, id=job_id, host=host, data=data))
    #     return job_list

    def create_job(self, username, Job_Name, queue, nodes, walltime, file):
        c = pbs.pbs_connect(str(pbs.pbs_default()))

        attrl = pbs.new_attropl(3)

        attrl[0].name = pbs.ATTR_N
        attrl[0].value = str(Job_Name)

        attrl[1].name = pbs.ATTR_l
        attrl[1].resource = 'nodes'
        attrl[1].value = str(nodes)

        attrl[2].name = pbs.ATTR_l
        attrl[2].resource = 'walltime'
        attrl[2].value = str(walltime)

        queue = str(queue)
        task_id = pbs.pbs_submit(c, attrl, str("media/" + username + "/" + file), queue, 'NULL')
        return pbs.pbs_geterrmsg(c)
        # print "Task id: " + str(task_id)

    def hold_rls_job(self, job_id, server, mode, permission):
        '''
        Example:
        job_id: 183
        server: jim-desktop
        mode: hold | rls
        permission: u | o | s
        '''
        c = pbs.pbs_connect(str(pbs.pbs_default()))  # Create new connection for the child process
        if server is None:
            server = pbs.pbs_default()
        job_full_id = job_id + '.' + server
        if mode == 'hold':
            result = pbs.pbs_holdjob(c, job_full_id, permission, 'NULL')
        elif mode == 'rls':
            result = pbs.pbs_rlsjob(c, job_full_id, permission, 'NULL')
        return result  # If operation is successfull, result == 0

    def del_job(self, job_id, server):
        c = pbs.pbs_connect(str(pbs.pbs_default()))  # Create new connection for the child process
        if server is None:
            server = pbs.pbs_default()
        job_full_id = job_id + '.' + server
        result = pbs.pbs_deljob(c, job_full_id, 'NULL')
        return result  # If operation is successfull, result == 0

    def node_list(self, node_name=None, username=None):
        nodes = []
        if node_name is None:
            data = self.getnodes()
            for k, v in data.items():
                nodes.append(NodeInstance(self, k, dict(v)))
        else:
            data = self.getnode(node_name)
            nodes.append(NodeInstance(self, node_name, data))
        return nodes

    def queue_list(self, queue_name=None):
        queues = []
        if queue_name is None:
            data = self.getqueues()
            for k, v in data.items():
                queues.append(QueueInstance(self, k, dict(v)))
        else:
            data = self.getqueue(queue_name)
            queues.append(QueueInstance(self, queue_name, data))
        return queues