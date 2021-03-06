'''
url table
'''

from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from core.api.user import (
    userinfo,
    ldapauth,
    login_auth,
    login_register
)
from core.api.dashboard import (
    dashboard
)
from core.api.managerdb import (
    management_db,
    management_env,
    management_service,
    dingding
)
from core.api.auditorder import (
    audit,
    del_order,
    getsql
)
from core.api.record import (
    record_order,
    order_detail
)
from core.api.applygrained import (
    audit_grained,
    apply_grained
)
from core.api.meta import Meta
from core.api.sqlorder import sqlorder
from core.api.serachsql import search, query_worklf, Query_order
from core.api.osc import osc_step
from core.api.myorder import order
from core.api.myorderdetail import myorderdetail
from core.api.general import addressing, exAES
from core.api.setting import setting_view
from core.api.authgroup import auth_group
from core.api.apollo import Apollo

urlpatterns = [
    url(r'^api/v1/exaes', exAES.as_view()),
    url(r'^api/v1/authgroup/(.*)', auth_group.as_view()),
    url(r'^api/v1/getsql', getsql.as_view()),
    url(r'^api/v1/setting/(.*)', setting_view.as_view()),
    url(r'^api/v1/query_order', Query_order.as_view()),
    url(r'^api/v1/query_worklf', query_worklf.as_view()),
    url(r'^api/v1/userinfo/(.*)', userinfo.as_view()),
    url(r'^api/v1/loginregister/(.*)', login_register.as_view()),
    url(r'^api/v1/audit_grained/(.*)', audit_grained.as_view()),
    url(r'^api/v1/apply_grained', apply_grained.as_view()),
    url(r'^api/v1/workorder/(.*)', addressing.as_view()),
    url(r'^api/v1/orderdetail/(.*)', myorderdetail.as_view()),
    url(r'^api/v1/myorder', order.as_view()),
    url(r'^api/v1/management_db/(.*)', management_db.as_view()),
    url(r'^api/v1/audit_sql', audit.as_view()),
    url(r'^api/v1/sqlsyntax/(.*)', sqlorder.as_view()),
    url(r'^api/v1/record/(.*)', record_order.as_view()),
    url(r'^api/v1/homedata/(.*)', dashboard.as_view()),
    url(r'^api/v1/dingding', dingding.as_view()),
    url(r'^api/v1/detail', order_detail.as_view()),
    url(r'^api/v1/search', search.as_view()),
    url(r'^api/v1/ldapauth', ldapauth.as_view()),
    url(r'^api/v1/undoOrder', del_order.as_view()),
    url(r'^api/v1/osc/(.*)', osc_step.as_view()),
    url(r'^api/v1/management_env/(.*)', management_env.as_view()),
    url(r'^api/v1/management_service/(.*)', management_service.as_view()),
    url(r'^api-token-auth/', login_auth.as_view()),
    url(r'^api/v1/meta/', Meta.as_view()),
    url(r'^api/v1/apollo/(.*)$', Apollo.as_view()),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
urlpatterns = format_suffix_patterns(urlpatterns)
