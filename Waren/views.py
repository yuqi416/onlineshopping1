from django.shortcuts import render
from Waren.models import WarenKategorien, WarenInfo


# Create your views here.

# Homepage
def index(request):
    # Warenkategorie abfragen
    Kategorien_Waren = WarenKategorien.objects.all()

    # Holen die vier neuesten Waren aus jeder Kategorie
    for K in Kategorien_Waren:
        info = WarenInfo.objects.filter(Ware_Kategorien = K)
        waren_zeigen_list = info.order_by('-id')[:4]

    # zeigen Waren in Einkaufswagen(benutzen cookie: waren_id,waren_menge)
    waren_gesamt_Menge_in_Einkaufswagen = 0
    all_waren = request.COOKIES.items()
    for waren_id,waren_menge in all_waren:
        # waren_id muss digit sein,
        # wenn jetzt diese waren_menge nicht ein Teil von Waren,pruefen naechste waren_id
        if not waren_id.isdigit():
            continue
        # Holen die Waren in den aktuell durchlaufenen Cookies
        get_waren = WarenInfo.objects.get(id=waren_id)
        get_waren.waren_menge=waren_menge   # menge jeder Ware
        # rechnen gezamt Waren Menge in Einkaufswagen
        waren_gesamt_Menge_in_Einkaufswagen += int(waren_menge)

    #para3: daten muss in template gegeben werden
    # include:Warenkategorie,Waren in Einkaufswagen, gesamt Menge in Einkaufswagen
    return render(request, 'index.html',{
                                         'waren_gesamt_Menge_in_Einkaufswagen':waren_gesamt_Menge_in_Einkaufswagen,
                                         })

# Waren Information werden auf einer separaten Seite angezeigt
def Waren_Seite(request):
    # Warenkategorie abfragen
    Kategorien_Waren = WarenKategorien.objects.all()

    waren_gesamt_Menge_in_Einkaufswagen = 0
    all_waren = request.COOKIES.items()
    for waren_id, waren_menge in all_waren:
        # waren_id muss digit sein,
        # wenn jetzt diese waren_menge nicht ein Teil von Waren,pruefen naechste waren_id
        if not waren_id.isdigit():
            continue
        # Holen die Waren in den aktuell durchlaufenen Cookies
        get_waren = WarenInfo.objects.get(id=waren_id)
        get_waren.Ware_Meng = waren_menge  # menge jeder Ware
        # rechnen gezamt Waren Menge in Einkaufswagen
        waren_gesamt_Menge_in_Einkaufswagen += int(waren_menge)

    # Holen die id des übergebenen Ware
    akt_ware_id = request.GET.get("id", 1)
    # aktuelle Information des Ware
    akt_ware_info = WarenInfo.objects.get(id=akt_ware_id)


    return render(request, 'Waren_Seite.html', {"waren_gesamt_Menge_in_Einkaufswagen":waren_gesamt_Menge_in_Einkaufswagen,
                                                 "akt_ware_info":akt_ware_info})

# zeigen alle Waren von jede Kategorien
def Waren_katg(request):
    # Holen die gegebene Kategorien id
    katg_id = request.GET.get('katg', 1)
    katg_geg = WarenKategorien.objects.get(id = katg_id)
    # Holen alle Waren in diese Kategorien
    alle_waren_katg = WarenInfo.objects.filter(Ware_Kategorien = katg_geg)


    # Einkaufswagen
    waren_gesamt_Menge_in_Einkaufswagen = 0
    all_waren = request.COOKIES.items()
    for waren_id, waren_menge in all_waren:
        # waren_id muss digit sein,
        # wenn jetzt diese waren_menge nicht ein Teil von Waren,pruefen naechste waren_id
        if not waren_id.isdigit():
            continue
        # Holen die Waren in den aktuell durchlaufenen Cookies
        get_waren = WarenInfo.objects.get(id=waren_id)
        get_waren.Ware_Meng = waren_menge  # menge jeder Ware
        # rechnen gezamt Waren Menge in Einkaufswagen
        waren_gesamt_Menge_in_Einkaufswagen += int(waren_menge)
    return render(request, "Waren_katg.html", {'alle_waren_katg':alle_waren_katg,
                                               'katg_geg' : katg_geg,
                                               'waren_gesamt_Menge_in_Einkaufswagen': waren_gesamt_Menge_in_Einkaufswagen})