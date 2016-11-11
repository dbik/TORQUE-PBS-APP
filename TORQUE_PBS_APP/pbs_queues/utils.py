class QueueInstance:
    def __init__(self, server, name, data=None):
        self.server = server
        self.server_name = str(server.name)
        self.name = str(name)
        self.data = data

        # Some variables need initialization
        # because they are not present in every queue
        self.state_count = self.get_state_count()
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

        self.started = 'False'
        self.enabled = 'False'
        self.resources_default_nodes = 0
        self.resources_default_walltime = '00:00:00'
        self.queue_type = self.get_queue_type()
        self.mtime = self.get_mtime()  # int
        self.total_jobs = self.get_total_jobs()  # int
        self.acl_users = ''
        self.acl_user_enable = 'False'

        if not data:
            data = self.server.p.getqueue(self.name)

        for k, v in data.items():
            if k.startswith('resources'):
                for i, j in v.items():
                    setattr(self, k + '_' + i, j[0])
            if k.startswith('acl_users'):
                setattr(self, k, v[0])
            if k.startswith('acl_user_enable'):
                setattr(self, k, v[0])
            if k.startswith('started'):
                setattr(self, k, v[0])
            if k.startswith('enabled'):
                setattr(self, k, v[0])

    def __str__(self):
        return self.name

    def get_data(self):
        return self.data

    def get_state_count(self):
        return self.data['state_count'][0]

    def get_queue_type(self):
        return self.data['queue_type'][0]

    def get_total_jobs(self):
        return self.data['total_jobs'][0]

    def get_mtime(self):
        return self.data['mtime'][0]