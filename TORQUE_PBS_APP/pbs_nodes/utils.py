class NodeInstance(object):
    def __init__(self, server, name, data=None):
        self.server = server
        self.server_name = str(server.name)
        self.name = str(name)
        self.data = data

        # Some variables need initialization
        # because they are not present in every node
        self.jobs = ''
        self.gres = ''
        self.nusers = 0
        self.idletime = 0
        self.rectime = 0
        self.sessions = ''
        self.physmem = ''
        self.totmem = ''
        self.netload = 0
        self.loadave = ''
        self.uname = ''
        self.opsys = ''
        self.nsessions = 0
        self.ncpus = 0
        self.availmem = ''
        self.varattr = ''
        # self.mom_manager_port = self.get_mom_manager_port()#int
        self.ntype = self.get_ntype()
        self.state = self.get_state()
        self.mom_service_port = self.get_mom_service_port()  # int
        self.np = self.get_np()  # int
        # self.gpus = self.get_gpus()#int

        if not data:
            data = self.server.p.getnodes(self.name)

        for k, v in data.items():
            if k.startswith('status'):
                for i, j in v.items():
                    j.append('')
                    setattr(self, i, str(j[0]))
            if k.startswith('jobs'):
                setattr(self, k, v)
            if k.startswith('gres'):
                setattr(self, k, v[0])
            if k.startswith('nusers'):
                setattr(self, k, v[0])
            if k.startswith('idletime'):
                setattr(self, k, v[0])
            if k.startswith('rectime'):
                setattr(self, k, v[0])
            if k.startswith('sessions'):
                setattr(self, k, v[0])
            if k.startswith('physmem'):
                setattr(self, k, v[0])
            if k.startswith('totmem'):
                setattr(self, k, v[0])
            if k.startswith('netload'):
                setattr(self, k, v[0])
            if k.startswith('loadave'):
                setattr(self, k, v[0])
                # if k.startswith('state'):
                #   setattr(self, k, v[0])
            if k.startswith('uname'):
                setattr(self, k, v[0])
            if k.startswith('opsys'):
                setattr(self, k, v[0])
            if k.startswith('nsessions'):
                setattr(self, k, v[0])
            if k.startswith('ncpus'):
                setattr(self, k, v[0])
            if k.startswith('availmem'):
                setattr(self, k, v[0])
            if k.startswith('varattr'):
                setattr(self, k, v[0])

    def __str__(self):
        return self.name

    def _get_pk_val(self):
        return self.name

    def get_jobs(self):
        return self.data['jobs']

    # def get_mom_manager_port(self):
    #    return self.data['mom_manager_port'][0]
    def get_mom_service_port(self):
        return self.data['mom_service_port'][0]

    def get_ntype(self):
        return self.data['ntype'][0]

    def get_state(self):
        return self.data['state'][0]

    def get_np(self):
        return self.data['np'][0]
        # def get_gpus(self):
        #    return self.data['gpus'][0]