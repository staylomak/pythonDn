# -*- coding: utf-8 -*-


from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve


from rest_framework.authtoken.views import obtain_auth_token


from autenticacion.views import log_in, log_out
from autenticacion.views import home_to_dashboard, ProfileTemplateView
from emails.views import EmailDteInputView
from webhooks.views import SendGridRestWebhookView, SendGridApiWebhookView


urlpatterns = [
    # rutas de api rest
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token/', obtain_auth_token, name='obtener_auth_token'),

    # rutas api rest heredadas de APIView
    # en esta ruta entran las peticiones de correo desde un DTE
    url(r'^api/email/', EmailDteInputView.as_view()),

    # rutas modulo emails
    url(r'emails/', include('emails.urls', namespace='emails')),

    # rutas modulo empresas
    url(r'^empresas/', include('empresas.urls', namespace='empresas')),

    # rutas modulo perfiles
    url(r'^perfiles/', include('perfiles.urls', namespace='perfiles')),

    # rutas de las paginas html del tracking
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^customsearch/',
        include('customsearch.urls', namespace='customsearch')),
    url(r'^webhook-api/',
        SendGridApiWebhookView.as_view(), name='webhook_api'),

    # rutas para reportes
    url(r'^reports/', include('reports.urls', namespace='reports')),

    # url que recibe webhooks de sendgrid
    url(r'^webhook/', SendGridRestWebhookView.as_view(), name='webhook_rest'),
    url(r'^resumen/', include('resumen.urls', namespace="resumen")),

    # rutas de autenticación de usuarios
    url(r'^$', home_to_dashboard),
    url(r'^login/', log_in, name='login'),
    url(r'^logout/', log_out, name='logout'),
    url(r'^profile/', ProfileTemplateView.as_view(), name='profile'),

    # modulo Administrador Azurian
    url(r'^admin/', include(admin.site.urls)),

    # rutas estaticas
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),
]
