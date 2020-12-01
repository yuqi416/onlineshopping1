"""onlineshopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from Einkaufswagen.views import Wagen_legen, Wagen_Seite, Waren_delete, Bestellung_abgeben_Seite, \
    Bestellung_abegeben_fertig, Bestellung_erfolgreich
from Waren.views import index, Waren_Seite, Waren_katg

urlpatterns = [
    path('admin/', admin.site.urls),
    # Homepage
    re_path(r'^index/$', index),
    # Waren_Seite
    re_path(r'^Waren_Seite/$', Waren_Seite),
    # In den Warenkorb legen
    re_path(r'^Wagen_legen/$', Wagen_legen),
    # Waren_katg Seite
    re_path(r'^Waren_katg/$', Waren_katg),
    # Einkaufswagen Seite
    re_path(r'^Wagen_Seite/$', Wagen_Seite),
    # delete ware von Einkaufswagen
    re_path(r'^Waren_delete/$', Waren_delete),
    # Bestellung abgeben Seite(Empfaenger Information ist leer)
    re_path(r'^Bestellung_abgeben_Seite/$', Bestellung_abgeben_Seite),
    # Bestellung hat schon abgegeben(Empfaenger Information speichern)
    re_path(r'^Bestellung_abegeben_fertig/$', Bestellung_abegeben_fertig),
    # Bestellung erfolgreich zeigen
    re_path(r'^Bestellung_erfolgreich/$', Bestellung_erfolgreich),
]
