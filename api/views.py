# coding:utf-8
# from django.shortcuts import redirect,render,HttpResponse
# from django.views.decorators.csrf import csrf_exempt,csrf_protect
import hashlib
import time
import json
# Create your views here.
# ck = "8kasoimnasodn8687asdfkmasdf"

#
# @csrf_exempt
# def asset(request):
    #
    #
    #     # print(request.method)
    #     # print(request.POST)
    #     # print(request.GET)
    #     # print(request.body)
    #     auth_key_time = request.META['HTTP_AUTHKEY']
    #     auth_key_client,client_ctime = auth_key_time.split('|')
    #     server_current_time = time.time()
    #     if server_current_time-5 > float(client_ctime):
    #         # 太久远
    #         return HttpResponse('时间太久远了')
    #     if auth_key_time in auth_list:
    #         # 已经访问过
    #         return HttpResponse('你来晚了')
    #
    #     # auth_key:9ff77e3f67f4baf3e44d7c957d80bc9a
    #     # client_ctime:1492395317.8952246
    #     # 9ff77e3f67f4baf3e44d7c957d80bc9a|
    #
    #     # 173b81be05cd997eeac31e2fa99eff1c|1492395689.3360105
    #     key_time = "%s|%s" %(ck,client_ctime,)
    #     m = hashlib.md5()
    #     m.update(bytes(key_time, encoding='utf-8'))
    #     authkey = m.hexdigest()
    #
    #     if authkey != auth_key_client:
    #         return HttpResponse('授权失败')
    #     auth_list.append(auth_key_time)
    #
    #
    # auth_key = request.META["HTTP_AUTHKEY"]
    # if auth_key != ck:
    #     return HttpResponse("授权失败！")
    # else:
    #     if request.method == 'POST':
    #         import json
    #         host_info = json.loads(str(request.body, encoding='utf-8'))  # 把json的编码转换成python的数据类型列表(字典)
    #         print(host_info)
    #         print(type(host_info))
    #         return HttpResponse('数据发送成功！')

# def test(request):
#     # print(request.POST,type(request.POST))
#     # from django.http.request import QueryDict
#     response = render(request,'index.html')
#     response.set_signed_cookie('kkkk','vvvv',salt='asdf')
#     return response

# def test(request):
#     import requests
#     host_data = {
#         "status": True,
#         "data": {
#             "hostname": "slave1",
#             "disk": {"status": True, "data": ""},
#             "mem": {"status": True, "data": ""},
#             "nic": {"status": True, "data": ""},
#             "cpu": {"status": True, "data": ""},
#             "main_board": {"status": True, "data": ""},
#         },
#     }
#     # ds = json.dumps(host_data, cls=Json)
#     ds=json.dumps(host_data) #将python数据类型列表进行json格式的编码
#     response = requests.post(
#         url="http://127.0.0.1:8000/api/test/",
#         data=host_data,
#         headers={"authkey": "8kasoimnasodn8687asdfkmasdf"},
#     )
#
#     return render(request,"test.html",{"res":response})
# class AssetView(View):
#     @method_decorator(csrf_exempt)
#     def dispath(self,request,*args,**kwargs):
#         pass
#
#     @method_decorator(auth.api_auth)
#     def get(self,request,*args,**kwargs):
#         pass
#
#     @method_decorator(auth.api_auth)
#     def post(self,request,*args,**kwargs):
#         pass

import json
import importlib
from django.views import View
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from utils import auth
from api import config
from repository import models
from api.service import asset

ck = "8kasoimnasodn8687asdfkmasdf"

auth_list=[]

@auth.api_auth
def asset(request):
    pass


class AssetView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssetView, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth.api_auth)
    def get(self, request, *args, **kwargs):
        """
        获取今日未更新的资产 - 适用SSH或Salt客户端
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # test = {'user': '用户名', 'pwd': '密码'}
        # result = json.dumps(test,ensure_ascii=True)
        # result = json.dumps(test,ensure_ascii=False)
        # return HttpResponse(result)

        # test = {'user': '用户名', 'pwd': '密码'}
        # result = json.dumps(test,ensure_ascii=True)
        # result = json.dumps(test,ensure_ascii=False)
        # return HttpResponse(result,content_type='application/json')

        # test = {'user': '用户名', 'pwd': '密码'}
        # return JsonResponse(test, json_dumps_params={"ensure_ascii": False})

        response = asset.get_untreated_servers()
        return JsonResponse(response.__dict__)

    # @method_decorator(auth.api_auth)
    # def post(self, request, *args, **kwargs):
    #     """
    #     更新或者添加资产信息
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return: 1000 成功;1001 接口授权失败;1002 数据库中资产不存在
    #     """
    #
    #     server_info = json.loads(request.body.decode('utf-8'))
    #     server_info = json.loads(server_info)
    #     # ret = {'code': 1000, 'message': ''}
    #     # print(server_info)
    #     hostname = server_info['hostname']
    #
    #     ret = {'code': 1000, 'message': '[%s]更新完成' % hostname}
    #     # server_info 最新汇报服务器所有信息
    #
    #     # 根据主机名去数据库中获取相关信息
    #     server_obj = models.Server.objects.filter(hostname=hostname).select_related('asset').first()
    #     if not server_obj:
    #         ret['code'] = 1002
    #         ret['message'] = '[%s]资产不存在' % hostname
    #         return JsonResponse(ret)
    #
    #     for k, v in config.PLUGINS_DICT.items():
    #         module_path, cls_name = v.rsplit('.', 1)
    #         cls = getattr(importlib.import_module(module_path), cls_name)
    #         response = cls.process(server_obj, server_info, None)
    #         if not response.status:
    #             ret['code'] = 1003
    #             ret['message'] = "[%s]资产更新异常" % hostname
    #         if hasattr(cls, 'update_last_time'):
    #             cls.update_last_time(server_obj, None)
    #
    #     return JsonResponse(ret)

    @method_decorator(auth.api_auth)
    def post(self, request, *args, **kwargs):
        """
        更新或者添加资产信息
        :param request:
        :param args:
        :param kwargs:
        :return: 1000 成功;1001 接口授权失败;1002 数据库中资产不存在
        """

        server_info = json.loads(request.body.decode('utf-8'))
        server_info = json.loads(server_info)
        # ret = {'code': 1000, 'message': ''}
        # print(server_info)
        hostname = server_info['hostname']

        ret = {'code': 1000, 'message': '[%s]更新完成' % hostname}
        # server_info 最新汇报服务器所有信息

        # 根据主机名去数据库中获取相关信息
        server_obj = models.Server.objects.filter(hostname=hostname).select_related('asset').first()
        if not server_obj:
            ret['code'] = 1002
            ret['message'] = '[%s]资产不存在' % hostname
            return JsonResponse(ret)

        # ========》 server_obj服务器对象 ；server_info  《==========
        # 硬盘 或 网卡 或 内存
        # 硬盘：增删改
        # 1. server_obj反向关联硬盘表，获取数据库中硬盘信息
        # [
        #     {'slot': "#1", 'size': '100'},
        #     {'slot': "#2", 'size': '60'},
        #     {'slot': "#3", 'size': '88'},
        # ]
        # old_list = ['#1','#2','#3']
        # 2. server_info['disk'] 新汇报的硬盘数据
        # {
        #     "#1":{'slot': "#1", 'size': '90'},
        #     "#4":{'slot': "#4", 'size': '40'},
        # }
        # new_list = ['#1','#4']
        #3. 更新['#1'] 删除['#2','#3'] 增加 ['#4']

        #4. # 增加 ['#4']
        """
            for i in  ['#4']:
                data_dict = dic[i]
                models.Diks.objces.create(**data_dict)


       """




        return JsonResponse(ret)