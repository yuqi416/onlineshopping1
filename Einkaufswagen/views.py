import time

from django.shortcuts import render, redirect

# Create your views here.
from Einkaufswagen.models import BestellungInfo, BestellungDetails
from Waren.models import WarenInfo

# In den Warenkorb legen
def Wagen_legen(request):
    """ in Warenkorb und cookie legen, in cookie ist: Waren_id:menge"""

    # Holen die gelieferte Ware id
    ware_id = request.GET.get("id", " ")
    if ware_id:  # wenn ware existiert
        url_von_vorher_Waren_seite = request.META["HTTP_REFERER"]
        # Holen response
        response = redirect(url_von_vorher_Waren_seite)
        # Holen die vorherigen Menge der Ware im Warenkorb
        ware_menge = request.COOKIES.get(ware_id)
        # wenn schon im Warenkorb, menge+1
        if ware_menge:
            ware_menge = int(ware_menge) + 1
        # sonst setze die Menge als 1
        else:
            ware_menge = 1
        # Speichern Ware id in cookie
        response.set_cookie(ware_id, ware_menge)
    return response


# Einkaufswagen Seite zeigen
def Wagen_Seite(request):
    # Waren liste in Einkaufswagen
    waren_in_Einkaufswagen_list = []

    # Waren Menge in Einkaufswagen
    waren_gesamt_Menge_in_Einkaufswagen = 0

    # Gesamt Preis in Einkaufswagen
    waren_gesamt_Preis_in_Einkaufswagen = 0

    # Holen Daten aud cookie waren_id:waren_menge
    all_waren = request.COOKIES.items()
    for waren_id, waren_menge in all_waren:
        # waren_id muss digit sein,
        # wenn jetzt diese waren_menge nicht ein Teil von Waren,pruefen naechste waren_id
        if not waren_id.isdigit():
            continue
        # Holen die Waren in den aktuell durchlaufenen Cookies
        get_waren = WarenInfo.objects.get(id=waren_id)
        get_waren.waren_menge = int(waren_menge)  # menge jeder Ware
        # Gesamt Preis dieser Ware
        ware_gesamt_preis = get_waren.waren_menge * get_waren.Ware_Preis
        # Waren in waren_in_Einkaufswagen_list ablegen
        waren_in_Einkaufswagen_list.append(get_waren)
        # rechnen gezamt Waren Menge in Einkaufswagen
        waren_gesamt_Menge_in_Einkaufswagen += int(waren_menge)
        # Gesamt Preis in Einkaufswagen
        waren_gesamt_Preis_in_Einkaufswagen += ware_gesamt_preis

    return render(request, "Wagen_Seite.html", {'waren_in_Einkaufswagen_list': waren_in_Einkaufswagen_list,
                                                  'waren_gesamt_Menge_in_Einkaufswagen': waren_gesamt_Menge_in_Einkaufswagen,
                                                  'waren_gesamt_Preis_in_Einkaufswagen': waren_gesamt_Preis_in_Einkaufswagen,

                                                 })


# delete Waren von Einkaufswagen
def Waren_delete(request):
    # get ware id, die zu entfernt wird
    ware_id = request.GET.get('id', '')
    if ware_id:
        url_von_vorher_Einkaufswagen_seite = request.META['HTTP_REFERER']
        response = redirect(url_von_vorher_Einkaufswagen_seite)
        # wenn diese Ware in cookies
        ware_menge = request.COOKIES.get(ware_id, '')
        if ware_menge:
            response.delete_cookie(ware_id)

    return response

# Bestellung abgeben Seite(Empfaenger Information ist leer)
def Bestellung_abgeben_Seite(request):
    # Waren liste in Einkaufswagen
    waren_in_Einkaufswagen_list = []

    # Waren Menge in Einkaufswagen
    waren_gesamt_Menge_in_Einkaufswagen = 0

    # Gesamt Preis in Einkaufswagen
    waren_gesamt_Preis_in_Einkaufswagen = 0

    # Holen Daten aud cookie waren_id:waren_menge
    all_waren = request.COOKIES.items()
    for waren_id, waren_menge in all_waren:
        # waren_id muss digit sein,
        # wenn jetzt diese waren_menge nicht ein Teil von Waren,pruefen naechste waren_id
        if not waren_id.isdigit():
            continue
        # Holen die Waren in den aktuell durchlaufenen Cookies
        get_waren = WarenInfo.objects.get(id=waren_id)
        get_waren.waren_menge =int(waren_menge)  # menge jeder Ware
        # Gesamt Preis dieser Ware
        ware_gesamt_preis = int(waren_menge) * get_waren.Ware_Preis
        # Waren in waren_in_Einkaufswagen_list ablegen
        waren_in_Einkaufswagen_list.append(get_waren)
        # rechnen gezamt Waren Menge in Einkaufswagen
        waren_gesamt_Menge_in_Einkaufswagen += int(waren_menge)
        # Gesamt Preis in Einkaufswagen
        waren_gesamt_Preis_in_Einkaufswagen += ware_gesamt_preis

    return render(request,'Bestellung_abgeben_Seite.html', {'waren_in_Einkaufswagen_list':waren_in_Einkaufswagen_list,
                                                           'waren_gesamt_Menge_in_Einkaufswagen':waren_gesamt_Menge_in_Einkaufswagen,
                                                           'waren_gesamt_Preis_in_Einkaufswagen':waren_gesamt_Preis_in_Einkaufswagen,})

# Bestellung hat schon abgegeben(Empfaenger Information speichern)
def Bestellung_abegeben_fertig(request):
    Adresse = request.POST.get("Adresse", ' ')
    Empfaenger = request.POST.get("Empfaenger", ' ')
    Telefonnummer = request.POST.get("Telefonnummer", ' ')
    Anmerkung = request.POST.get('Anmerkung', ' ')

    # Instanzieren Bestellung
    Bestellung_Info = BestellungInfo()
    Bestellung_Info.Bestellung_Add = Adresse
    Bestellung_Info.Bestellung_Empf = Empfaenger
    Bestellung_Info.Bestellung_Tel = Telefonnummer
    Bestellung_Info.Bestellung_Anmerkung = Anmerkung

    # Bestellungnummer Instanz erzeugen
    Bestellung_Info.Bestellung_Nummer = str(time.time()*1000)+str(time.perf_counter()*100000)

    # Bestellung speichern in Datenbank
    Bestellung_Info.save()
    # jump nach Bestellung_erfolgreich Seite
    response = redirect('Waren/Bestellung_erfolgreich/?id=%s'%Bestellung_Info.Bestellung_Nummer)
    # Holen Daten aud cookie waren_id:waren_menge
    all_waren = request.COOKIES.items()
    for waren_id, waren_menge in all_waren:
        # waren_id muss digit sein,
        # wenn jetzt diese waren_menge nicht ein Teil von Waren,pruefen naechste waren_id
        if not waren_id.isdigit():
            continue
        # Holen waren Objekte
        waren_in_korb = WarenInfo.objects.get(id = waren_id)
        # erzeugen BestellungDetails Instanz
        Bestellung_details = BestellungDetails()
        # addieren Waren Objekte in BestellungDetails
        Bestellung_details.Ware_Kate = waren_in_korb
        # Menge der Waren
        Bestellung_details.Ware_Meng = waren_menge
        # gehort Bestellung
        Bestellung_details.Ware_Bestellung = Bestellung_Info

        # Waren in Datanbank speichern
        Bestellung_details.save()
        # delete Daten von Einkaufswagen(in cookie)
        response.delete_cookie(waren_id)

    return response

# Bestellung erfolgreich zeigen
def Bestellung_erfolgreich(request):
    # holen gegebene Bestellungs id
    Bestellung_id = request.GET.get("id")
    # holen Bestellung Instanz
    Bestellung_info=BestellungInfo.objects.get(Bestellung_Nummer=Bestellung_id)
    Bestellung_waren_list=BestellungDetails.objects.filter(Ware_Bestellung=Bestellung_info)
    gesamt_preis_Wagen=0
    gesamt_num_Wagen=0
    for ware in Bestellung_waren_list:
        waren_gesamt_preis=ware.WarenInfo.Ware_Preis * ware.Ware_Meng
        gesamt_preis_Wagen+=waren_gesamt_preis
        gesamt_num_Wagen+=ware.Ware_Meng

    return render(request,"Bestellung_erfolgreich.html",{"Bestellung_info":Bestellung_info,
                              'Bestellung_waren_list':Bestellung_waren_list,
                              'gesamt_preis_Wagen':gesamt_preis_Wagen,
                              'gesamt_num_Wagen':gesamt_num_Wagen,})





