# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!flask/bin/python
# coding=utf-8
from api import app
import logging as log
import traceback

from uuid import uuid4
import time,json
import sys,os
from flask import request
from ..libv2.apiv2_exc import *
from ..libv2.quotas_exc import *

#from ..libv2.telegram import tsend
def tsend(txt):
    None
from ..libv2.carbon import Carbon
carbon = Carbon()

from ..libv2.quotas import Quotas
quotas = Quotas()

from ..libv2.api_desktops_nonpersistent import ApiDesktopsNonPersistent
desktops = ApiDesktopsNonPersistent()

@app.route('/api/v2/desktop', methods=['POST'])
def api_v2_desktop_new():
    try:
        user_id = request.form.get('id', type = str)
        template_id = request.form.get('template', type = str)
    except Exception as e:
        return json.dumps({"code":8,"msg":"Incorrect access. exception: " + error }), 401, {'Content-Type': 'application/json'}
    if user_id == None or template_id == None:
        log.error("Incorrect access parameters. Check your query.")
        return json.dumps({"code":8,"msg":"Incorrect access parameters. Check your query." }), 401, {'Content-Type': 'application/json'}

    # Leave only one nonpersistent desktop from this template
    try:
        desktops.DeleteOthers(user_id,template_id)

    except DesktopNotFound:
        try:
            quotas.DesktopCreateAndStart(user_id)
        except QuotaUserNewDesktopExceeded:
            log.error("Quota for user "+user_id+" to create a desktop exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user desktop quota CREATE exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaGroupNewDesktopExceeded:
            log.error("Quota for user "+user_id+" to create a desktop in his group limits is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew group desktop limits CREATE exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaCategoryNewDesktopExceeded:
            log.error("Quota for user "+user_id+" to create a desktop in his category limits is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew category desktop limits CREATE exceeded"}), 507, {'Content-Type': 'application/json'}

        except QuotaUserConcurrentExceeded:
            log.error("Quota for user "+user_id+" to start a desktop is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user quota CONCURRENT exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaGroupConcurrentExceeded:
            log.error("Quota for user "+user_id+" to start a desktop in his group is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user limits CONCURRENT exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaCategoryConcurrentExceeded:
            log.error("Quota for user "+user_id+" to start a desktop is his category exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user category limits CONCURRENT exceeded"}), 507, {'Content-Type': 'application/json'}
        
        except QuotaUserVcpuExceeded:
            log.error("Quota for user "+user_id+" to allocate vCPU is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user quota vCPU allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaGroupVcpuExceeded:
            log.error("Quota for user "+user_id+" to allocate vCPU in his group is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user group limits vCPU allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaCategoryVcpuExceeded:
            log.error("Quota for user "+user_id+" to allocate vCPU in his category is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user category limits vCPU allocation exceeded"}), 507, {'Content-Type': 'application/json'}

        except QuotaUserMemoryExceeded:
            log.error("Quota for user "+user_id+" to allocate MEMORY is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user quota MEMORY allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaGroupMemoryExceeded:
            log.error("Quota for user "+user_id+" for creating another desktop is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user group limits MEMORY allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaCategoryMemoryExceeded:
            log.error("Quota for user "+user_id+" category for desktop MEMORY allocation is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user category limits MEMORY allocation exceeded"}), 507, {'Content-Type': 'application/json'}

        except Exception as e:
            error = traceback.format_exc()
            return json.dumps({"code":9,"msg":"DesktopNew quota check general exception: " + error }), 401, {'Content-Type': 'application/json'}
    
    except DesktopNotStarted:
        try:
            quotas.DesktopStart(user_id)        
        except QuotaUserConcurrentExceeded:
            log.error("Quota for user "+user_id+" to start a desktop is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user quota CONCURRENT exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaGroupConcurrentExceeded:
            log.error("Quota for user "+user_id+" to start a desktop in his group is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user limits CONCURRENT exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaCategoryConcurrentExceeded:
            log.error("Quota for user "+user_id+" to start a desktop is his category exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user category limits CONCURRENT exceeded"}), 507, {'Content-Type': 'application/json'}
        
        except QuotaUserVcpuExceeded:
            log.error("Quota for user "+user_id+" to allocate vCPU is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user quota vCPU allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaGroupVcpuExceeded:
            log.error("Quota for user "+user_id+" to allocate vCPU in his group is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user group limits vCPU allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaCategoryVcpuExceeded:
            log.error("Quota for user "+user_id+" to allocate vCPU in his category is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user category limits vCPU allocation exceeded"}), 507, {'Content-Type': 'application/json'}

        except QuotaUserMemoryExceeded:
            log.error("Quota for user "+user_id+" to allocate MEMORY is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user quota MEMORY allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaGroupMemoryExceeded:
            log.error("Quota for user "+user_id+" for creating another desktop is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user group limits MEMORY allocation exceeded"}), 507, {'Content-Type': 'application/json'}
        except QuotaCategoryMemoryExceeded:
            log.error("Quota for user "+user_id+" category for desktop MEMORY allocation is exceeded")
            return json.dumps({"code":11,"msg":"DesktopNew user category limits MEMORY allocation exceeded"}), 507, {'Content-Type': 'application/json'}

        except Exception as e:
            error = traceback.format_exc()
            return json.dumps({"code":9,"msg":"DesktopNew quota check general exception: " + error }), 401, {'Content-Type': 'application/json'}

    except Exception as e:
        error = traceback.format_exc()
        return json.dumps({"code":9,"msg":"DesktopNew previous checks general exception: " + error }), 401, {'Content-Type': 'application/json'}


    # So now we have checked if desktop exists and if we can create and/or start it

    try:
        now=time.time()
        desktop_id = desktops.New(user_id,template_id)
        carbon.send({'create_and_start_time':str(round(time.time()-now,2))})
        return json.dumps({'id': desktop_id}), 200, {'Content-Type': 'application/json'}
    except UserNotFound:
        log.error("Desktop for user "+user_id+" from template "+template_id+", user not found")
        return json.dumps({"code":1,"msg":"DesktopNew user not found"}), 404, {'Content-Type': 'application/json'}
    except TemplateNotFound:
        log.error("Desktop for user "+user_id+" from template "+template_id+" template not found.")
        return json.dumps({"code":2,"msg":"DesktopNew template not found"}), 404, {'Content-Type': 'application/json'}
    except DesktopNotCreated:
        log.error("Desktop for user "+user_id+" from template "+template_id+" creation failed.")
        carbon.send({'create_and_start_time':'100'})
        return json.dumps({"code":1,"msg":"DesktopNew not created"}), 404, {'Content-Type': 'application/json'}
    except DesktopActionTimeout:
        log.error("Desktop for user "+user_id+" from template "+template_id+" start timeout.")
        carbon.send({'create_and_start_time':'100'})
        return (
            json.dumps({"code": 2, "msg": "DesktopNew start timeout"}),
            408,
            {"Content-Type": "application/json"},
        )
    except DesktopActionFailed:
        log.error("Desktop for user "+user_id+" from template "+template_id+" start failed.")
        carbon.send({'create_and_start_time':'100'})
        return json.dumps({"code":3,"msg":"DesktopNew start failed"}), 404, {'Content-Type': 'application/json'}
    except Exception as e:
        error = traceback.format_exc()
        return json.dumps({"code":9,"msg":"DesktopNew general exception: " + error }), 401, {'Content-Type': 'application/json'}

@app.route('/api/v2/desktop/<desktop_id>', methods=['DELETE'])
def api_v2_desktop_delete(desktop_id=False):
    if desktop_id == False:
        log.error("Incorrect access parameters. Check your query.")
        return json.dumps({"code":8,"msg":"Incorrect access parameters. Check your query." }), 401, {'Content-Type': 'application/json'}

    try:
        now=time.time()
        desktops.Delete(desktop_id)
        carbon.send({'delete_time':str(round(time.time()-now,2))})
        return json.dumps({}), 200, {'Content-Type': 'application/json'}
    except DesktopNotFound:
        log.error("Desktop delete "+desktop_id+", desktop not found")
        return json.dumps({"code":1,"msg":"Desktop delete id not found"}), 404, {'Content-Type': 'application/json'}
    except DesktopDeleteFailed:
        log.error("Desktop delete "+desktop_id+", desktop delete failed")
        return json.dumps({"code":5,"msg":"Desktop delete deleting failed"}), 404, {'Content-Type': 'application/json'}
    except Exception as e:
        error = traceback.format_exc()
        return json.dumps({"code":9,"msg":"DesktopDelete general exception: " + error }), 401, {'Content-Type': 'application/json'}
