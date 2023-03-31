from django.shortcuts import render, get_object_or_404, redirect
from api.models import Tester, CakeForm, Inside, DekoOrder, CatalogCake, CakeBatter, OutsideContent, OutsideColours, CakeShopAssistant, CakeOrder
from api.views import cake_content
from random import randint

update_url = 'https://drive.google.com/drive/folders/1eQC6XSit_SDCTKvn7tGSg-P7_XNACP0b?usp=sharing'

def update(request):
    return redirect(update_url)

def torte_home(request):
    return render(request, 'index.html')


def tortenkatalog(request):
    return render(request, 'tortenkatalog.html')


def cake_content():
    def object_name(query):
        query_dict = []
        n = 0
        queryset = query.objects.all()
        for i in queryset:
            name = str(i)
            query_dict.append(name)
            n += 1
        return query_dict

    forms = object_name(CakeForm)
    insides = object_name(Inside)
    # dekos = Deko.objects.all()
    # dekos_list = []
    # for deko in dekos:
    #     deko_details = {}
    #     deko_details['description'] = deko.description
    #     deko_details['price'] = deko.price
    #     if deko.picture:
    #         deko_details['picture'] = deko.picture.url
    #     if deko.size:
    #         deko_details['size'] = deko.size
    #     dekos_list.append(deko_details)
    outside_colours = object_name(OutsideColours)
    outside_contents = object_name(OutsideContent)
    cake_batters = object_name(CakeBatter)
    shop_assistants = object_name(CakeShopAssistant)
    cake_text_materials = ['Sahne', 'Fondant']
    return {'forms': forms, 'insides': insides, 'outside_colours': outside_colours,
            'outside_contents': outside_contents, 'cake_batters': cake_batters, 'text_materials': cake_text_materials,
            'shop_assistants': shop_assistants}


def torte_erstellen(request):
    context = cake_content()
    if request.method == "POST":
        vorname = request.POST.get('vorname')
        nachname = request.POST.get('nachname')
        telefonnummer = request.POST.get('telefonnummer')
        mail = request.POST.get('mail')
        date = request.POST.get('date')
        time = request.POST.get('time')
        agb = request.POST.get('agb')
        personen_anzahl = request.POST.get('personen_anzahl')
        stockwerke = request.POST.get('stockwerke')
        text_inhalt = request.POST.get('text_inhalt')
        tortentext = request.POST.get('tortentext')
        torten_foto = request.FILES.get('torten-foto')
        vorlage_foto = request.FILES.get('vorlage-foto')
        torten_info = request.POST.get('torten-info')

        def order_id_maker():
            test_number = randint(10000, 99999)
            while CakeOrder.objects.filter(order_id=test_number).exists():
                test_number = randint(10000, 99999)
            return test_number

        def get_inside():
            inside_contains = request.POST.get('inside')
            if Inside.objects.filter(description=inside_contains).exists():
                return Inside.objects.get(description=inside_contains)
            else:
                return None

        def get_cakebatter():
            cake_batter_contains = request.POST.get('kuchenteig')
            if CakeBatter.objects.filter(name=cake_batter_contains).exists():
                return CakeBatter.objects.get(name=cake_batter_contains)
            else:
                return None

        def get_outside_content():
            outside_contains = request.POST.get('aeussere-creme')
            if OutsideContent.objects.filter(name=outside_contains).exists():
                return OutsideContent.objects.get(name=outside_contains)
            else:
                return None

        def get_outside_colour():
            outside_colour_contains = request.POST.get('aussenfarbe')
            if OutsideColours.objects.filter(name=outside_colour_contains).exists():
                return OutsideColours.objects.get(name=outside_colour_contains)
            else:
                return None

        def get_cake_form():
            form_contains = request.POST.get('tortenform')
            if CakeForm.objects.filter(description=form_contains).exists():
                return CakeForm.objects.get(description=form_contains)
            else:
                return None

        created_order = CakeOrder.objects.create(order_id=order_id_maker(), inside=get_inside(), cakebatter=get_cakebatter(), outside_content=get_outside_content(), outside_colour=get_outside_colour(), persons=personen_anzahl, form=get_cake_form(), floors=stockwerke, picture=torten_foto, example_picture=vorlage_foto, text=text_inhalt, textmaterial=tortentext, deadline_date=date, deadline_time=time, customer_name=vorname, customer_surname=nachname, customer_phone=telefonnummer,customer_mail=mail, customer_info=torten_info, price=0)
        context = {
            'vorname': vorname,
            'nachname': nachname,
            'order_id': created_order.order_id
        }
        return render(request, 'erfolg.html', context)
    return render(request, 'torte_erstellen.html', context)


def foto(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        if CakeOrder.objects.filter(order_id=order_id).exists():
            order = CakeOrder.objects.get(order_id=order_id)
            if order.picture:
                context = {
                    'url': order.picture.url
                }
                if order.example_picture:
                    context['example_url'] = order.example_picture.url
                return render(request, 'foto_success.html', context)
            else:
                return render(request, 'foto_error.html', {'message': 'Bu siparişte baskı fotoğrafı mevcut değil!'})
        else:
            return render(request, 'foto_error.html',{'message': 'Bu numaraya ait sipariş bulunmamaktadır!'})

    return render(request, 'foto.html')


# def foto_kunde(request):
#     if request.method == "POST":
#         order_id = request.POST.get('order_id')
#         if CakeOrder.objects.filter(order_id=order_id).exists():
#             order = CakeOrder.objects.get(order_id=order_id)
#             if order.picture:
#                 context = {
#                     'url': order.picture.url
#                 }
#                 if order.example_picture:
#                     context['example_url'] = order.example_picture.url
#                 return render(request, 'foto_success.html', context)
#             else:
#                 return render(request, 'foto_error.html', {'message': 'Bu siparişte baskı fotoğrafı mevcut değil!'})
#         else:
#             return render(request, 'foto_error.html',{'message': 'Bu numaraya ait sipariş bulunmamaktadır!'})

#     return render(request, 'foto.html')







    

