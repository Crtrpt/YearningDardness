import logging
import json
import traceback
import ast
from libs import baseview
from libs.cryptoAES import cryptoAES
from libs import con_database
from core.task import grained_permissions
from libs import util
from rest_framework.response import Response
from django.http import HttpResponse
from django.db import transaction
from libs.serializers import Sqllist
from libs.serializers import Envlist
from libs.serializers import Servicelist
from settingConf import settings
from core.models import (
    DatabaseList,
    Env,
    Service,
    SqlRecord,
    SqlOrder,
    grained,
    query_order
)

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

AES = cryptoAES(settings.SECRET_KEY)


class Meta(baseview.AnyLogin):
    '''

    :argument 服务管理页面api 接口

    '''

    def get(self, request, args=None):

        '''

        :argument 管理页面数据展示

        :return

                {
                        'page': page_number,
                        'data': serializers.data,
                        'ding_switch': switch_dingding,
                        'mail_switch': switch_email
                }

        '''
        info = Env.objects.all().order_by('id')
        env_serializers = Envlist(info, many=True)

        info = Service.objects.all().order_by('id')
        service_serializers = Servicelist(info, many=True)

        return Response(
            {
                'env_list': env_serializers.data,
                'service_list': service_serializers.data,
                'version_list': [],
            }
        )

    def post(self, request, args=None):

        '''

        :argument 添加数据库连接信息,并保存至DatabaseList表

        :return: ok

        '''

        try:
            data = json.loads(request.data['data'])
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                Service.objects.get_or_create(
                    service_name=data['service_name'],
                    env_name=data['env_name'],
                    env_id=int(data['env_id']),
                )
                return Response('ok')
            except Exception as e:
                traceback.print_stack()
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    def put(self, request, args=None):

        '''

        :argument 测试数据库连接,并返回测试结果数据

        :return: success or fail

        '''

        if args == 'test':

            try:
                ip = request.data['ip']
                user = request.data['user']
                password = request.data['password']
                port = request.data['port']
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    with con_database.SQLgo(ip=ip, user=user, password=password, port=port):
                        return Response('连接成功!')
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return Response('连接失败!')

        elif args == 'update':

            try:
                update_data = json.loads(request.data['data'])
                password = AES.encrypt(update_data['password'])
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    DatabaseList.objects.filter(
                        connection_name=update_data['connection_name'],
                        computer_room=update_data['computer_room']).update(
                        ip=update_data['ip'],
                        username=update_data['username'],
                        password=password,
                        port=update_data['port']
                    )
                    return Response('数据信息更新成功！')
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)

    def delete(self, request, args=None):

        '''

        :argument 删除数据库连接,并删除改数据库连接相关的工单记录,执行记录，以及权限表等相关所有数据

        :return: success or fail

        '''

        try:
            with transaction.atomic():
                con_id = DatabaseList.objects.filter(connection_name=args).first()
                work_id = SqlOrder.objects.filter(bundle_id=con_id.id).first()
                with transaction.atomic():
                    SqlRecord.objects.filter(workid=work_id).delete()
                    SqlOrder.objects.filter(bundle_id=con_id.id).delete()
                    DatabaseList.objects.filter(connection_name=args).delete()
                    query_order.objects.filter(connection_name=args).update(query_per=3)
                per = grained.objects.all().values('username', 'permissions')
                for i in per:
                    for c in i['permissions']:
                        if isinstance(i['permissions'][c], list):
                            i['permissions'][c] = list(filter(lambda x: x != args, i['permissions'][c]))
                    grained.objects.filter(username=i['username']).update(permissions=i['permissions'])
            return Response('数据库信息已删除!')
        except Exception as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
