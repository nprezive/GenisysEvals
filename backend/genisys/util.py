from __future__ import with_statement
from django.core.signals import request_finished
from django.dispatch import receiver
from django_cas_ng.backends import CASBackend
from django_cas_ng import signals as cas_signals
from db.models import User
from django.conf import settings as config
import ldap
import socket
import logging


class WeberCASBackend(CASBackend):
    def configure_user(self, user):
        return user

@receiver(cas_signals.cas_user_authenticated)
def CASLoginCallack(sender, **kwargs):
    print("Request finished!")


@receiver(cas_signals.cas_user_logout)
def CASLoginCallack(sender, **kwargs):
    print("Request finished!")



class LDAPService:
    def __init__(self):
        self.logger = None

    def __enter__(self):
        self.logger = logging.getLogger("django.ldap")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def login(self, username, password, ip):
        self.logger.info("LDAP request for [" + username + "] using [" + socket.getfqdn() + "]")

        user = dict()
        user["iserror"] = False
        user["errorRetry"] = False
        user["success"] = False
        user["username"] = username
        user["password"] = password
        user["ip"] = ip

        for key in config.AUTH_LDAP_CONNECTION_OPTIONS:
            ldap.set_option(key, config.AUTH_LDAP_CONNECTION_OPTIONS[key])

        try:
            conn = ldap.initialize(config.AUTH_LDAP_SERVER_URI)
            conn.bind_s(config.AUTH_LDAP_BIND_DN, config.AUTH_LDAP_BIND_PASSWORD, ldap.AUTH_SIMPLE)
            result = conn.search_s("dc=ad,dc=weber,dc=edu", ldap.SCOPE_SUBTREE,
                                   "(&(objectclass=user)(sAMAccountName=" + user["username"] + "))")
            if len(result) is 0:
                user["iserror"] = True
                user["errorType"] = "user"
                user["errorText"] = "User not found"
            elif len(result[0]) is 0:
                user["iserror"] = True
                user["errorType"] = "user"
                user["errorText"] = "User not found"
            elif result[0][0] is None:
                user["iserror"] = True
                user["errorType"] = "user"
                user["errorText"] = "User not found"
            else:
                user["userdn"] = result[0][0]
                conn.unbind_s()
                conn = ldap.initialize(config.AUTH_LDAP_SERVER_URI)
                conn.bind_s(user["userdn"], user["password"], ldap.AUTH_SIMPLE)
                user["attrs"] = result[0][1]
                user["success"] = True

        except ldap.NO_RESULTS_RETURNED as err:
            user["iserror"] = True
            user["errorType"] = "notfound"
            user["errorObj"] = err.args[0]
        except ldap.NO_SUCH_ATTRIBUTE as err:
            user["iserror"] = True
            user["errorType"] = "notfound"
            user["errorObj"] = err.args[0]
        except ldap.NO_SUCH_OBJECT as err:
            user["iserror"] = True
            user["errorType"] = "notfound"
            user["errorObj"] = err.args[0]
        except ldap.SERVER_DOWN as err:
            user["iserror"] = True
            user["errorType"] = "server"
            user["errorObj"] = err.args[0]
            user["errorRetry"] = True
            self.logger.error(err.args[0])
        except ldap.TIMEOUT as err:
            user["iserror"] = True
            user["errorType"] = "timeout"
            user["errorObj"] = err.args[0]
            user["errorRetry"] = True
            self.logger.error(err.args[0])
        except ldap.ADMINLIMIT_EXCEEDED as err:
            user["iserror"] = True
            user["errorType"] = "admin"
            user["errorObj"] = err.args[0]
            self.logger.error(err.args[0])
        except ldap.CONNECT_ERROR as err:
            user["iserror"] = True
            user["errorType"] = "connection"
            user["errorObj"] = err.args[0]
            user["errorRetry"] = True
            self.logger.error(err.args[0])
        except ldap.INVALID_CREDENTIALS as err:
            user["iserror"] = True
            user["errorType"] = "credentials"
            user["errorText"] = "bad credentials"
            user["errorObj"] = err.args[0]
        except ldap.LDAPError as err:
            user["iserror"] = True
            user["errorType"] = "unknown"
            user["errorObj"] = err.args[0]
            user["errorRetry"] = True
            self.logger.error(err.args[0])
        finally:
            if user["errorRetry"]:
                user = self.login(username, password, ip)

            if user["iserror"]:
                if "userdn" in user:
                    self.logger.info(
                        "LDAP login failed for [" + str(user["userdn"]) + "] using [" + socket.getfqdn() + "]")
                else:
                    self.logger.info("LDAP login failed for [" + username + "] using [" + socket.getfqdn() + "]")

            return user

class LDAPBackend(object):
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return None

        ldapuser = None

        with LDAPService() as ldap:
            ldapuser = ldap.login(username, password, request.get_host())

        if ldapuser is None:
            return None

        if ldapuser['iserror']:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User()

        user.username = username
        user.last_name = ldapuser['attrs']['sn'][0].decode('utf-8')
        user.first_name = ldapuser['attrs']['givenName'][0].decode('utf-8')
        # user.phone = ldapuser['attrs']['telephoneNumber'][0].decode('utf-8')
        user.email = ldapuser['attrs']['mail'][0].decode('utf-8')

        if any(b'Chitester Admins' in bstr for bstr in ldapuser['attrs']['memberOf']):
            user.is_superuser = True
            user.is_active = True

        if any(b'trevororgill' in bstr for bstr in ldapuser['attrs']['sAMAccountName']):
            user.is_superuser = True
            user.is_active = True

        if any(b'collinwelker' in bstr for bstr in ldapuser['attrs']['sAMAccountName']):
            user.is_superuser = True
            user.is_active = True

        if any(b'All Students' in bstr for bstr in ldapuser['attrs']['memberOf']):
            user.is_active = True

        if any(b'WSU Employees' in bstr for bstr in ldapuser['attrs']['memberOf']):
            user.is_staff = True
            user.is_active = True

        user.save()


        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
