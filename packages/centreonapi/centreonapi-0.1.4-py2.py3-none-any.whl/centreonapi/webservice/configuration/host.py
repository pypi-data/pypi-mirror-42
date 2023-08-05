# -*- coding: utf-8 -*-

import centreonapi.webservice.configuration.common as common
from centreonapi.webservice.configuration.poller import Poller
from centreonapi.webservice.configuration.hostgroups import HostGroup
from centreonapi.webservice.configuration.contact import ContactGroup, Contact
from centreonapi.webservice import Webservice


class Host(common.CentreonObject):

    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.__clapi_action = 'HOST'
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.activate = properties.get('activate')
        self.address = properties.get('address')
        self.alias = properties.get('alias')
        self.macros = dict()
        self.templates = dict()
        self.parents = dict()
        self.hostgroups = dict()
        self.contactgroups = dict()
        self.contacts = dict()
        self.state = properties.get('state')

    def getmacro(self):
        self.macros.clear()
        state, macro = self.webservice.call_clapi(
                            'getmacro',
                            self.__clapi_action,
                            self.name)
        if state:
            if len(macro['result']) > 0:
                for m in macro['result']:
                    macro_obj = HostMacro(m)
                    self.macros[macro_obj.engine_name] = macro_obj
                return state, self.macros
            else:
                return state, None
        else:
            return state, macro

    def setmacro(self, name, value, is_password=None, description=None):
        if description is None:
            description = ''
        if is_password is None:
            is_password = 0
        macro = name.replace("_HOST", "").replace("$", "").upper()
        values = [self.name, macro, value, is_password, description]
        return self.webservice.call_clapi(
            'setmacro',
            self.__clapi_action,
            values)

    def deletemacro(self, macro):
        values = [self.name,
                  "|".join(common.build_param(macro, HostMacro))]
        return self.webservice.call_clapi(
            'delmacro',
            self.__clapi_action,
            values)

    def gettemplate(self):
        state, template = self.webservice.call_clapi(
                            'gettemplate',
                            self.__clapi_action,
                            self.name)
        if state:
            if len(template['result']) > 0:
                for t in template['result']:
                    template_obj = HostTemplate(t)
                    self.templates[template_obj.name] = template_obj
                return state, self.templates
            else:
                return state, None
        else:
            return state, template

    def settemplate(self, template=None):
        values = [self.name,
                  "|".join(common.build_param(template, HostTemplate))]
        return self.webservice.call_clapi(
            'settemplate',
            self.__clapi_action,
            values)

    def addtemplate(self, template=None):
        values = [self.name,
                  "|".join(common.build_param(template, HostTemplate))]
        return self.webservice.call_clapi(
            'addtemplate',
            self.__clapi_action,
            values)

    def deletetemplate(self, template=None):
        values = [self.name,
                  str("|".join(common.build_param(template, HostTemplate)))]
        return self.webservice.call_clapi(
            'deltemplate',
            self.__clapi_action,
            values)

    def applytemplate(self):
        return self.webservice.call_clapi(
            'applytpl',
            self.__clapi_action,
            self.name)

    def enable(self):
        s, e = self.webservice.call_clapi(
                'enable',
                self.__clapi_action,
                self.name)
        if s:
            self.activate = "1"
        return s, e

    def disable(self):
        s, e = self.webservice.call_clapi(
                'disable',
                self.__clapi_action,
                self.name)
        if s:
            self.activate = "0"
        return s, e

    def setinstance(self, instance):
        values = [self.name,
                  str(common.build_param(instance, Poller)[0])]
        return self.webservice.call_clapi(
            'setinstance',
            self.__clapi_action,
            values)

    def status(self):
        values = {'search': self.name}
        self.state = self.webservice.centreon_realtime(
            'list',
             'hosts',
            values)[0]['state']
        return self.state

    def getparent(self):
        state, parent = self.webservice.call_clapi(
                        'getparent',
                        self.__clapi_action,
                        self.name)
        if state:
            if len(parent['result']) > 0:
                for p in parent['result']:
                    parent_obj = Host(p)
                    self.parents[parent_obj.name] = parent_obj
                return state, self.parents
            return state, None
        else:
            return state, parent

    def addparent(self, parents):
        values = [self.name,
                  "|".join(common.build_param(parents, Host))]
        return self.webservice.call_clapi(
            'addparent',
            self.__clapi_action,
            values)

    def setparent(self, parents):
        values = [self.name,
                  "|".join(common.build_param(parents, Host))]
        return self.webservice.call_clapi(
            'setparent',
            self.__clapi_action,
            values)

    def deleteparent(self, parents):
        values = [self.name,
                  "|".join(common.build_param(parents, Host))]
        return self.webservice.call_clapi(
            'delparent',
            self.__clapi_action,
            values)

    def gethostgroup(self):
        state, hgs =  self.webservice.call_clapi(
                        'gethostgroup',
                        self.__clapi_action,
                        self.name)
        if state:
            if len(hgs['result']) > 0:
                for h in hgs['result']:
                    hg_obj = HostGroup(h)
                    self.hostgroups[hg_obj.name] = hg_obj
                return state, self.hostgroups
            else:
                return state, None
        else:
            return state, hgs

    def addhostgroup(self, hostgroup=None):
        values = [self.name,
                  "|".join(common.build_param(hostgroup, HostGroup))]
        return self.webservice.call_clapi(
            'addhostgroup',
            self.__clapi_action,
            values)

    def sethostgroup(self, hostgroup=None):
        values = [self.name,
                  "|".join(common.build_param(hostgroup, HostGroup))]
        return self.webservice.call_clapi(
            'sethostgroup',
            self.__clapi_action,
            values)

    def deletehostgroup(self, hostgroup=None):
        values = [self.name,
                  "|".join(common.build_param(hostgroup, HostGroup))]
        return self.webservice.call_clapi(
            'delhostgroup',
            self.__clapi_action,
            values)

    def getcontactgroup(self):
        state, cgs = self.webservice.call_clapi(
                        'getcontactgroup',
                        self.__clapi_action,
                        self.name)
        if state:
            if len(cgs['result']) > 0:
                for c in cgs['result']:
                    cg_obj = ContactGroup(c)
                    self.contactgroups[cg_obj.name] = cg_obj
                return state, self.contactgroups
            else:
                return state, None
        else:
            return state, cgs

    def addcontactgroup(self, contactgroups):
        values = [self.name,
                  "|".join(common.build_param(contactgroups, ContactGroup))]
        return self.webservice.call_clapi(
            'addcontactgroup',
            self.__clapi_action,
            values)

    def setcontactgroup(self, contactgroups):
        values = [self.name,
                  "|".join(common.build_param(contactgroups, ContactGroup))]
        return self.webservice.call_clapi(
            'setcontactgroup',
            self.__clapi_action,
            values)

    def deletecontactgroup(self, contactgroups):
        values = [self.name,
                  "|".join(common.build_param(contactgroups, ContactGroup))]
        return self.webservice.call_clapi(
            'delcontactgroup',
            self.__clapi_action,
            values)

    def getcontact(self):
        """
        :return: state (True/False), contacts or error message
        """
        state, cs =  self.webservice.call_clapi(
                        'getcontact',
                        self.__clapi_action,
                        self.name)
        if state:
            if len(cs['result']) > 0:
                for c in cs['result']:
                    c_obj = Contact(c)
                    self.contacts[c_obj.name] = c_obj
                return state, self.contacts
            else:
                return state, None
        else:
            return state, cs

    def addcontact(self, contacts):
        values = [self.name,
                  "|".join(common.build_param(contacts, Contact))]
        return self.webservice.call_clapi(
            'addcontact',
             self.__clapi_action,
            values)

    def setcontact(self, contacts):
        values = [self.name,
                  "|".join(common.build_param(contacts, Contact))]
        return self.webservice.call_clapi(
            'setcontact',
             self.__clapi_action,
             values)

    def deletecontact(self, contacts):
        values = [self.name,
                  "|".join(common.build_param(contacts, Contact))]
        return self.webservice.call_clapi(
            'delcontact',
            self.__clapi_action,
            values)

    def setseverity(self, name):
        pass
        #return self.webservice.call_clapi(
        #    'setseverity',
        #    self.__clapi_action,
        #    [self.name, name])

    def unsetseverity(self):
        pass
        #return self.webservice.call_clapi(
        #    'unsetseverity',
        #    self.__clapi_action,
        #    self.name)

    def setparam(self, name, value):
        values = [self.name, name, value]
        return self.webservice.call_clapi(
            'setparam',
            self.__clapi_action,
            values)

    def getparam(self, name):
        pass


class HostMacro(common.CentreonObject):

    def __init__(self, properties):
        self.name = properties.get('macro name')
        self.value = properties.get('macro value')
        self.description = properties.get('description', '')
        self.is_password = properties.get('is_password')
        self.source = properties.get('source')
        if self.is_password == '':
            self.is_password = 0
        self.engine_name = '$_HOST' + self.name + '$'

    def __repr__(self):
        return self.engine_name

    def __str__(self):
        return self.engine_name


class Hosts(common.CentreonDecorator, common.CentreonClass):
    """
    Centreon Web host object
    """

    def __init__(self):
        super(Hosts, self).__init__()
        self.hosts = dict()
        self.__clapi_action = 'HOST'

    def __contains__(self, name):
        return name in self.hosts.keys() or None

    def __getitem__(self, name):
        if not self.hosts:
            self.list()
        if name in self.hosts.keys():
            return True, self.hosts[name]
        else:
            return False, None

    def _refresh_list(self):
        self.hosts.clear()
        state, host = self.webservice.call_clapi(
                            'show',
                            self.__clapi_action)
        if state and len(host['result']) > 0:
            for h in host['result']:
                host_obj = Host(h)
                self.hosts[host_obj.name] = host_obj

    @common.CentreonDecorator.pre_refresh
    def list(self):
        return self.hosts

    @common.CentreonDecorator.post_refresh
    def add(self,
            name,
            alias,
            ip,
            instance=None,
            template=None,
            hg=None,
            post_refresh=True):
        """
        Add new Host on Centreon platform
        :param name: name for host
        :param alias:  alias (short name for example)
        :param ip: Ip address or DNS
        :param instance: Poller() or str()
        :param template: HostTemplate(), list() of HostTemplate(),
         list() of str() or str()
        :param hg: HostGroup(), list() of HostGroup(),
         list() of str() or str()
        :return:
        """
        values = [
            name,
            alias,
            ip,
            str("|".join(common.build_param(template, HostTemplate))) if template else template,
            str(common.build_param(instance, Poller)[0]) if instance else "Central",
            str("|".join(common.build_param(hg, HostGroup))) if hg else hg
        ]
        return self.webservice.call_clapi(
                    'add',
                    self.__clapi_action,
                    values)

    @common.CentreonDecorator.post_refresh
    def delete(self, host, post_refresh=True):
        value = str(common.build_param(host, Host)[0])
        return self.webservice.call_clapi(
                    'del',
                    self.__clapi_action,
                    value)


class HostTemplates(Hosts):
    def __init__(self):
        super(HostTemplates, self).__init__()
        self.__clapi_action = 'HTPL'


class HostTemplate(Host):

    def __init__(self, properties):
        super(HostTemplate, self).__init__(properties)
        self.__clapi_action = 'HTPL'
