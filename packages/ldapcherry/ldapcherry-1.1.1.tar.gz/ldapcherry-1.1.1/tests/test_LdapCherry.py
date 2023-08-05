#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import pytest
import sys
import subprocess
from tempfile import NamedTemporaryFile as tempfile
import re

from ldapcherry import LdapCherry
from ldapcherry.exceptions import *
from ldapcherry.pyyamlwrapper import DumplicatedKey, RelationError
import ldapcherry.backend.backendAD
import cherrypy
from cherrypy.process import plugins, servers
from cherrypy import Application
import logging
from ldapcherry.lclogging import *
from disable import *
import json
from tidylib import tidy_document
if sys.version < '3':
    from sets import Set as set

cherrypy.session = {}

adcfg = {
    'display_name': u'test☭',
    'domain': 'DC.LDAPCHERRY.ORG',
    'login': 'Administrator',
    'password': 'qwertyP455',
    'uri': 'ldaps://ad.ldapcherry.org',
    'checkcert': 'off',
}
adattr = ['shell', 'cn', 'sAMAccountName', 'uidNumber', 'gidNumber', 'home', 'unicodePwd', 'givenName', 'email', 'sn']


addefault_user = {
'sAMAccountName': u'☭default_user',
'sn':  u'test☭1',
'cn':  u'test☭2',
'unicodePwd': u'test☭P666',
'uidNumber': '42',
'gidNumber': '42',
'homeDirectory': '/home/test/'
}

# monkey patching cherrypy to disable config interpolation
def new_as_dict(self, raw=True, vars=None):
    """Convert an INI file to a dictionary"""
    # Load INI file into a dict
    result = {}
    for section in self.sections():
        if section not in result:
            result[section] = {}
        for option in self.options(section):
            value = self.get(section, option, raw=raw, vars=vars)
            try:
                value = cherrypy.lib.reprconf.unrepr(value)
            except Exception:
                x = sys.exc_info()[1]
                msg = ("Config error in section: %r, option: %r, "
                       "value: %r. Config values must be valid Python." %
                       (section, option, value))
                raise ValueError(msg, x.__class__.__name__, x.args)
            result[section][option] = value
    return result
cherrypy.lib.reprconf.Parser.as_dict = new_as_dict

conf = {'/static': {'tools.staticdir.dir': './resources/static/', 'tools.staticdir.on': True}, 'roles': {'roles.file': './tests/cfg/roles.yml'}, 'global': {'tools.sessions.on': True, 'log.access_handler': 'syslog', 'log.level': 'debug', 'server.thread_pool': 8, 'log.error_handler': 'syslog', 'server.socket_port': 8080, 'server.socket_host': '127.0.0.1', 'tools.sessions.timeout': 10, 'request.show_tracebacks': False}, 'auth': {'auth.mode': 'or'}, 'backends': {'ldap.checkcert': 'off', 'ldap.module': 'ldapcherry.backends.ldap', 'ldap.uri': 'ldaps://ldap.ldapcherry.org', 'ldap.starttls': 'on', 'ldap.groupdn': 'ou=group,dc=example,dc=com', 'ldap.people': 'ou=group,dc=example,dc=com', 'ldap.authdn': 'cn=ldapcherry,dc=example,dc=com', 'ldap.password': 'password', 'ldap.ca': '/etc/dnscherry/TEST-cacert.pem', 'ad.module': 'ldapcherry.backends.ad', 'ad.auth': 'Administrator', 'ad.password': 'password'}, 'attributes': {'attributes.file': './tests/cfg/attributes.yml'}, 'resources': {'templates.dir': './resources/templates/'}}

def loadconf(configfile, instance):
    app = cherrypy.tree.mount(instance, '/', configfile)
    cherrypy.config.update(configfile)
    instance.reload(app.config)

class HtmlValidationFailed(Exception):
    def __init__(self, out):
        self.errors = out

def _is_html_error(line):
    for p in [
                r'.*Warning: trimming empty <span>.*',
                r'.*Error: <nav> is not recognized!.*',
                r'.*Warning: discarding unexpected <nav>.*',
                r'.*Warning: discarding unexpected </nav>.*',
                r'.*Warning: <meta> proprietary attribute "charset".*',
                r'.*Warning: <meta> lacks "content" attribute.*',
                r'.*Warning: <link> inserting "type" attribute.*',
                r'.*Warning: <link> proprietary attribute.*',
                r'.*Warning: <input> proprietary attribute.*',
                r'.*Warning: <button> proprietary attribute.*',
                r'.*Warning: <form> proprietary attribute.*',
                r'.*Warning: <table> lacks "summary" attribute.*',
                r'.*Warning: <script> inserting "type" attribute.*',
                r'.*Warning: <input> attribute "id" has invalid value.*',
                r'.*Warning: <a> proprietary attribute.*',
                r'.*Warning: <input> attribute "type" has invalid value.*',
                r'.*Warning: <span> proprietary attribute.*',
             ]:
        if re.match(p, line):
            return False
    return True

def htmlvalidator(page):
    document, errors = tidy_document(page,
        options={'numeric-entities':1})
    f = tempfile()
    for line in errors.splitlines():
        if _is_html_error(line):
            print("################")
            print("Blocking error: '%s'" % line)
            print("all tidy_document errors:")
            print(errors)
            print("################")
            raise HtmlValidationFailed(line)

class BadModule():
    pass

class TestError(object):

    def testNominal(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry.ini', app)
        return True

    def testMissingBackendModule(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry.ini', app)
        cfg = {'backends': {'ldap.module': 'dontexists'}}
        try:
            app._init_backends(cfg)
        except BackendModuleLoadingFail:
            return
        else:
            raise AssertionError("expected an exception")

    def testInitgBackendModuleFail(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry.ini', app)
        cfg = {'backends': {'ldap.module': 'ldapcherry.backend'}}
        try:
            app._init_backends(cfg)
        except BackendModuleInitFail:
            return
        else:
            raise AssertionError("expected an exception")

    def testLog(self):
        app = LdapCherry()
        cfg = { 'global' : {}}
        for t in ['none', 'file', 'syslog', 'stdout']:
            cfg['global']['log.access_handler']=t
            cfg['global']['log.error_handler']=t
            app._set_access_log(cfg, logging.DEBUG)
            app._set_error_log(cfg, logging.DEBUG)

    def testAuth(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        app.auth_mode = 'and'
        ret1 = app._auth('jsmith', 'passwordsmith')
        app.auth_mode = 'or'
        ret2 = app._auth('jsmith', 'passwordsmith')
        assert ret2 == {'connected': True, 'isadmin': False} and \
            ret1 == {'connected': True, 'isadmin': False}

    def testPPolicy(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry.ini', app)
        wrong = app._checkppolicy('password')['match']
        good = app._checkppolicy('Passw0rd.')['match']
        assert wrong == False and good == True

    def testMissingBackend(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry.ini', app)
        del app.backends_params['ad']
        try:
            app._check_backends()
        except MissingBackend:
            return
        else:
            raise AssertionError("expected an exception")

    def testMissingParameters(self):
        app = LdapCherry()
        try:
            app.reload({})
        except SystemExit:
            return
        else:
            raise AssertionError("expected an exception")

    def testRandomException(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry.ini', app)
        e = Exception()
        app._handle_exception(e)

    def testLogin(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        app.auth_mode = 'or'
        try:
            app.login(u'jwatsoné', u'passwordwatsoné')
        except cherrypy.HTTPRedirect as e:
            expected = 'http://127.0.0.1:8080/'
            assert e.urls[0] == expected
        else:
            raise AssertionError("expected an exception")

    def testLoginFailure(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        app.auth_mode = 'or'
        try:
            app.login(u'jwatsoné', u'wrongPasswordé')
        except cherrypy.HTTPRedirect as e:
            expected = 'http://127.0.0.1:8080/signin'
            assert e.urls[0] == expected
        else:
            raise AssertionError("expected an exception")

    def testSearch(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        expected = {
            u'ssmith': {
                'password': u'passwordsmith',
                'cn': u'Sheri Smith',
                'name': u'smith',
                'uid': u'ssmith',
                'email': [u's.smith@example.com',
                          u'ssmith@example.com',
                          u'sheri.smith@example.com'
                     ],
                },
            u'jsmith': {
                'password': u'passwordsmith',
                'cn': u'John Smith',
                'name': u'Smith',
                'uid': u'jsmith',
                'email': [
                    'j.smith@example.com',
                    'jsmith@example.com',
                    'jsmith.smith@example.com'
                    ],
                }
            }
        ret = app._search('smith')
        assert expected == ret

    def testGetUser(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        expected = {
            'password': u'passwordsmith',
            'cn': u'Sheri Smith',
            'uid': u'ssmith',
            'name': u'smith',
            'email': [u's.smith@example.com',
                     u'ssmith@example.com',
                     u'sheri.smith@example.com'
                ],
            }
        ret = app._get_user('ssmith')
        assert expected == ret

    def testAddUser(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        form = {'groups': {}, 'attrs': {'password1': u'password☭', 'password2': u'password☭', 'cn': u'Test ☭ Test', 'name': u'Test ☭', 'uidNumber': u'1000', 'gidNumber': u'1000', 'home': u'/home/test', 'first-name': u'Test ☭', 'email': u'test@test.fr', 'uid': u'test'}, 'roles': {'admin-lv3': u'on', 'admin-lv2': u'on', 'users': u'on'}}
        app._adduser(form)
        app._deleteuser('test')

    def testParse(self):
        app = LdapCherry()
        form = {'attr.val': 'val', 'role.id': 'id', 'group.ldap.id': 'id'}
        ret = app._parse_params(form)
        expected = {'attrs': {'val': 'val'}, 'roles': {'id': 'id'}, 'groups': {'ldap': ['id']}}
        assert expected == ret

    def testModifUser(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        form = {'groups': {}, 'attrs': {'password1': u'password☭', 'password2': u'password☭', 'cn': u'Test ☭ Test', 'name': u'Test ☭', 'uidNumber': u'1000', 'gidNumber': u'1000', 'home': u'/home/test', 'first-name': u'Test ☭', 'email': u'test@test.fr', 'uid': u'test'}, 'roles': {'admin-lv3': u'on', 'admin-lv2': u'on', 'users': u'on'}}
        app._adduser(form)
        modify_form = { 'attrs': {'first-name': u'Test42 ☭', 'uid': u'test'}, 'roles': { 'admin-lv3': u'on'}}
        app._modify(modify_form)
        app._deleteuser('test')

    @slow_disabled
    def testHtml(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        pages = {
                'signin': app.signin(),
                'index': app.index(),
                'searchuser': app.searchuser('smit'),
                'searchadmin':app.searchadmin('smit'),
                'adduser': app.adduser(),
                'modify':app.modify('jsmith'),
                'selfmodify':app.selfmodify(),
                }
        for page in pages:
            print(page)
            htmlvalidator(pages[page])

    def testNoneType(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        app.modify('ssmith')
 
    def testNoneModify(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        app.modify(user=None)

    @slow_disabled
    def testNaughtyStrings(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_test.ini', app)
        with open('./tests/cfg/blns.json') as data_file:
            data = json.load(data_file)
        for attr in data:
            print('testing: ' + attr)
            # delete whatever is happening...
            try:
                app._deleteuser('test')
            except:
                pass
            form = {'groups': {}, 'attrs': {'password1': u'password☭', 'password2': u'password☭', 'cn': 'Test', 'name': attr, 'uidNumber': u'1000', 'gidNumber': u'1000', 'home': u'/home/test', 'first-name': u'Test ☭', 'email': u'test@test.fr', 'uid': 'test'}, 'roles': {'admin-lv3': u'on', 'admin-lv2': u'on', 'users': u'on'}}
            app._adduser(form)
            page = app.searchuser('test'),
            app._deleteuser('test')
            htmlvalidator(page[0])

    @travis_disabled
    def testDeleteUserOneBackend(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_adldap.cfg', app)
        inv = ldapcherry.backend.backendAD.Backend(adcfg, cherrypy.log, u'test☭', adattr, 'sAMAccountName')
        inv.add_user(addefault_user.copy())
        app._deleteuser(u'☭default_user')

    @travis_disabled
    def testAddUserOneBackend(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_adldap.cfg', app)
        inv = ldapcherry.backend.backendAD.Backend(adcfg, cherrypy.log, u'test☭', adattr, 'sAMAccountName')
        inv.add_user(addefault_user.copy())
        form = {'groups': {}, 'attrs': {'password1': u'password☭P455', 'password2': u'password☭P455', 'cn': u'Test ☭ Test', 'name': u'Test ☭', 'uidNumber': u'1000', 'gidNumber': u'1000', 'home': u'/home/test', 'first-name': u'Test ☭', 'email': u'test@test.fr', 'uid': u'☭default_user'}, 'roles': {'admin-lv3': u'on', 'admin-lv2': u'on', 'users': u'on'}}
        app._adduser(form)
        app._deleteuser(u'☭default_user')

    @travis_disabled
    def testModifyUserOneBackend(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry_adldap.cfg', app)
        inv = ldapcherry.backend.backendAD.Backend(adcfg, cherrypy.log, u'test☭', adattr, 'sAMAccountName')
        try:
            app._deleteuser(u'☭default_user')
        except:
            pass
        inv.add_user(addefault_user.copy())
        modify_form = { 'attrs': {'first-name': u'Test42 ☭', 'uid': u'☭default_user'}, 'roles': { 'admin-lv3': u'on'}}
        app._modify(modify_form)
        app._deleteuser(u'☭default_user')



    def testLogger(self):
        app = LdapCherry()
        loadconf('./tests/cfg/ldapcherry.ini', app)
        assert get_loglevel('debug') is logging.DEBUG and \
        get_loglevel('notice') is logging.INFO and \
        get_loglevel('info') is logging.INFO and \
        get_loglevel('warning') is logging.WARNING and \
        get_loglevel('err') is logging.ERROR and \
        get_loglevel('critical') is logging.CRITICAL and \
        get_loglevel('alert') is logging.CRITICAL and \
        get_loglevel('emergency') is logging.CRITICAL and \
        get_loglevel('notalevel') is logging.INFO
