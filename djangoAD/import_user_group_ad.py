# -*- coding: UTF-8 -*-
__author__ = 'lenin'
from django.contrib.auth.models import User,Group
import ldap

class DjangoAD:

    def __init__(self,basedn,lcon_emg):
        self._basedn=basedn
        self._lcon_emg=lcon_emg
        
    def get_user_display_name(self):
        scope = ldap.SCOPE_SUBTREE
        filters = "(&(objectClass=user)(name=*))"
        attributess = ['sAMAccountName','displayName']
        result= self._lcon_emg.search_s(self._basedn, scope, filters,attributess )
        d=[]
        for x in result[:-3]:
            a=len(x[1:][0])
            if a==2:
                d.append(x[1:][0])
        data={}
        for x in d:
            data[x['displayName'][0].decode('utf-8')]=x['sAMAccountName'][0]
        return data

    def get_User_by_group(self,ldap,lcon_emg):
        scope = ldap.SCOPE_SUBTREE
        filter = "(&(objectClass=group)(cn=wis*))"
        attributes = ['member']

        result= lcon_emg.search_s(self._basedn, scope, filter,attributes )
        displayName=getUserDisplayName(ldap,lcon_emg)
        user_group={}
        for k,v in result[:-3]:
            group=k.split(',')[0][3:]
            for item in v.items():
                usuario=[]
                for usuarios in item[1]:
                    a=usuarios.split(',OU')[0][3:]
                    displayNameUser=a.replace('\\','').decode('utf-8')
                    if len(displayNameUser.split(','))>1:
                        usuario.append(displayName[displayNameUser])
                    else:
                        usuario.append(displayNameUser)
                user_group[group]=usuario
        f=open('groupname','w')
        f.writelines(str(user_group))
        f.close()
        return user_group

    def get_users(user_group):
        users=[]
        for k,v in user_group.items():
            users+=v
        return set(users)

    def get_groups(user_group):
        groups=[]
        for k,v in user_group.items():
            groups.append(k)
        return groups

    def register_groups(groups):
        for grupo in groups:
            try:
                group=Group.objects.get(name=grupo)
            except Group.DoesNotExist:
                group=Group(name=grupo)
                group.save()

    def register_users(users):
        for username in users:
            try:
                user=User.objects.get(username=username)
            except User.DoesNotExist:
                user=User(username=username,is_active=True,is_superuser=False,is_staff=True)
                user.last_name=''
                user.set_password('')
                user.first_name=''
                user.save()

    def add_users_to_group(user_group):
        for k,v in user_group.items():
            grupo=Group.objects.get(name=k)
            print(grupo.id,grupo.name)
            for x in v:
                user=User.objects.get(username=x)
                user.groups.add(grupo)
                print(usuario.id,usuario.username)
