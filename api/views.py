from django.shortcuts import get_object_or_404
from typing import List
from ninja import NinjaAPI, Form, File
from ninja.files import UploadedFile
from .schemas import CakeOrderSchema, CakeOrderModelSchema, CatalogCakeSchema, \
    CatalogCakeModelSchema, UpdateCustomCakeSchema
from .models import Inside, CakeForm, Deko, OutsideColours, CakeBatter, OutsideContent, CatalogCake, \
    CakeOrder, CakeShopAssistant, DekoOrder, Tester
from random import randint

api = NinjaAPI()

root = 'https://mekan-torten.de'

def if_null(object_query, value):
                try:
                    return getattr(object_query, value)
                except AttributeError:
                    return 'SEÇİLMEMİŞ!'


# @api.get('/ip-test')
# def ip_test(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     x: int
#     if x_forwarded_for:
#         my_ip = x_forwarded_for.split(',')[0]
#         x = 1
#     else:
#         my_ip = request.META.get('REMOTE_ADDR')
#         x = 2
#     tester = Tester.objects.create(string=my_ip)
#     return f'{my_ip} :::::: {x}'

@api.get('/cake-content')
def cake_content(request, language: str):
    if language == 'de':
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
        dekos = Deko.objects.all()
        dekos_list = []
        for deko in dekos:
            deko_details = {}
            deko_details['id'] = deko.id
            deko_details['description'] = deko.description
            deko_details['price'] = deko.price
            if deko.picture:
                deko_details['picture'] = deko.picture.url
            if deko.size:
                deko_details['size'] = deko.size
            dekos_list.append(deko_details)
        outside_colours = object_name(OutsideColours)
        outside_contents = object_name(OutsideContent)
        cake_batters = object_name(CakeBatter)
        shop_assistants = object_name(CakeShopAssistant)
        cake_text_materials = ['Dunkle Schrift', 'Helle Schrift']
        return {'forms': forms, 'insides': insides, 'dekos': dekos_list, 'outside_colours': outside_colours,
                'outside_contents': outside_contents, 'cake_batters': cake_batters, 'text_materials': cake_text_materials,
                'shop_assistants': shop_assistants}
    elif language == 'tr':
        dekos = Deko.objects.all()
        dekos_list = []
        for deko in dekos:
            deko_details = {}
            deko_details['id'] = deko.id
            deko_details['description'] = deko.description_tr
            deko_details['price'] = deko.price
            if deko.picture:
                deko_details['picture'] = deko.picture.url
            if deko.size:
                deko_details['size'] = deko.size
            dekos_list.append(deko_details)
        def get_forms_tr():
            objects_list = []
            for form in CakeForm.objects.all():
                objects_list.append(form.description_tr)
            return objects_list
        def get_insides_tr():
            objects_list = []
            for inside in Inside.objects.all():
                objects_list.append(inside.description_tr)
            return objects_list
        def get_outside_colours_tr():
            objects_list = []
            for outside_colour in OutsideColours.objects.all():
                objects_list.append(outside_colour.name_tr)
            return objects_list
        def get_outside_contents_tr():
            objects_list = []
            for outside_content in OutsideContent.objects.all():
                objects_list.append(outside_content.name_tr)
            return objects_list
        def get_cake_batters_tr():
            objects_list = []
            for cake_batter in CakeBatter.objects.all():
                objects_list.append(cake_batter.name_tr)
            return objects_list
        def get_text_materials_tr():
            objects_list = ['Beyaz Yazı', 'Siyah Yazı']
            return objects_list
        def get_shop_assistants():
            objects_list = []
            for shop_assistant in CakeShopAssistant.objects.all():
                objects_list.append(shop_assistant.name)
            return objects_list
        return {'forms': get_forms_tr(), 'insides': get_insides_tr(), 'dekos': dekos_list, 'outside_colours': get_outside_colours_tr(),
                'outside_contents': get_outside_contents_tr(), 'cake_batters': get_cake_batters_tr(), 'text_materials': get_text_materials_tr(),
                'shop_assistants': get_shop_assistants()}
        

@api.get('/get-catalog-model/{cake_nr}')
def get_catalog_model(request, cake_nr):
    catalog_cake = get_object_or_404(CatalogCake, cake_nr=cake_nr)
    catalog_cake_details = {}
    catalog_cake_details['cake_nr'] = str(catalog_cake.cake_nr)
    catalog_cake_details['name'] = str(catalog_cake.name)
    catalog_cake_details['description'] = str(catalog_cake.description)
    catalog_cake_details['inside'] = str(catalog_cake.inside)
    if catalog_cake.picture:
        catalog_cake_details[
            'picture'] = f'{root}{catalog_cake.picture.url}'
    catalog_cake_details['inside'] = str(catalog_cake.inside)
    catalog_cake_details['cakebatter'] = str(catalog_cake.cakebatter)
    catalog_cake_details['outside_content'] = str(
        catalog_cake.outside_content)
    catalog_cake_details['outside_colour'] = str(
        catalog_cake.outside_colour)
    catalog_cake_details['persons'] = catalog_cake.persons
    if catalog_cake.picture:
            catalog_cake_details['picture'] = f'{root}{catalog_cake.picture.url}'
    catalog_cake_details['form'] = str(catalog_cake.form)
    catalog_cake_details['floors'] = catalog_cake.floors
    if catalog_cake.deko.exists():
        deko_list = []
        for deko in catalog_cake.deko.all():
            deko_dict = {}
            deko_dict['id'] = deko.deko_model.id
            deko_dict['description'] = deko.deko_model.description
            deko_dict['price'] = deko.deko_model.price
            if deko.deko_model.picture:
                deko_dict['image'] = f'{root}{deko.deko_model.picture.url}'
            if deko.deko_model.size:
                deko_dict['size'] = deko.size
            deko_dict['amount'] = deko.amount
            deko_list.append(deko_dict)
        catalog_cake_details['dekos'] = deko_list
    catalog_cake_details['price'] = catalog_cake.price
    return catalog_cake_details


@api.get('/get-catalog-models')
def get_catalog_models(request):
    cake_models = CatalogCake.objects.all()
    cake_model_list = []
    for cake_model in cake_models:
        cake_model_details = {}
        cake_model_details['cake_nr'] = str(cake_model.cake_nr)
        cake_model_details['name'] = str(cake_model.name)
        cake_model_details['description'] = str(cake_model.description)
        if cake_model.picture:
            cake_model_details[
                'picture'] = f'{root}{cake_model.picture.url}'
        cake_model_details['inside'] = str(cake_model.inside)
        cake_model_details['cakebatter'] = str(cake_model.cakebatter)
        cake_model_details['outside_content'] = str(cake_model.outside_content)
        cake_model_details['outside_colour'] = str(cake_model.outside_colour)
        cake_model_details['persons'] = cake_model.persons
        if cake_model.picture:
            cake_model_details['picture'] = f'{root}{cake_model.picture.url}'
        cake_model_details['persons'] = cake_model.persons
        cake_model_details['form'] = str(cake_model.form)
        cake_model_details['floors'] = cake_model.floors
        if cake_model.deko.exists():
            deko_list = []
            for deko in cake_model.deko.all():
                deko_dict = {}
                deko_dict['id'] = deko.deko_model.id
                deko_dict['description'] = deko.deko_model.description
                deko_dict['price'] = deko.deko_model.price
                if deko.deko_model.picture:
                    deko_dict['picture'] = deko.deko_model.price.picture.url
                if deko.deko_model.size:
                    deko_dict['size'] = deko.deko_model.price.size
                deko_dict['amount'] = deko.amount
                deko_list.append(deko_dict)
            cake_model_details['dekos'] = deko_list
        cake_model_details['price'] = cake_model.price
        cake_model_list.append(cake_model_details)
    return cake_model_list


@api.get('/get-cake-order/{order_id}')
def get_cake_order(request, order_id, language: str):
    cake_order = get_object_or_404(CakeOrder, order_id=order_id)
    cake_order_details = {}
    if cake_order.cake_model:
        cake_order_details['type'] = 'catalog_cake_order'
        cake_order_details['cake_model'] = str(cake_order.cake_model)
    else:
        cake_order_details['type'] = 'custom_cake_order'
    cake_order_details['order_id'] = str(cake_order.order_id)
    if language == "de":
        cake_order_details['inside'] = str(cake_order.inside)
        cake_order_details['cakebatter'] = str(cake_order.cakebatter)
        cake_order_details['outside_content'] = str(cake_order.outside_content)
        cake_order_details['outside_colour'] = str(cake_order.outside_colour)
        cake_order_details['persons'] = cake_order.persons
        cake_order_details['form'] = str(cake_order.form)
        cake_order_details['floors'] = cake_order.floors
        if cake_order.picture:
            cake_order_details[
                'picture'] = f'{root}{cake_order.picture.url}'
        if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
        id_list = []
        id_reference_list = {}
        for deko_object in cake_order.deko.all():
            id_list.append(deko_object.deko_model.id)
        deko_list = []
        for deko_object in cake_order.deko.all():
            id_reference_list[deko_object.deko_model.id] = deko_object.amount
        for deko in Deko.objects.all():
            if deko.id in id_list:
                deko_details = {}
                deko_details['id'] = deko.id
                deko_details['description'] = deko.description
                deko_details['price'] = deko.price
                deko_details['amount'] = id_reference_list[deko.id]
                deko_list.append(deko_details)
            else:
                deko_details = {}
                deko_details['id'] = deko.id
                deko_details['description'] = deko.description
                deko_details['price'] = deko.price
                deko_details['amount'] = 0
                deko_list.append(deko_details)
        cake_order_details['dekos'] = deko_list
        if cake_order.text:
            cake_order_details['text'] = cake_order.text
            cake_order_details['text_material'] = cake_order.textmaterial
        cake_order_details['order_date'] = str(cake_order.order_date)
        cake_order_details['order_time'] = str(cake_order.order_time)[:5]
        cake_order_details['deadline_date'] = str(cake_order.deadline_date)
        cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
        cake_order_details['customer_name'] = cake_order.customer_name
        cake_order_details['customer_surname'] = cake_order.customer_surname
        cake_order_details['customer_phone'] = cake_order.customer_phone
        cake_order_details['customer_mail'] = cake_order.customer_mail
        cake_order_details['customer_info'] = cake_order.customer_info
        cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
        cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
        cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
        cake_order_details['price'] = cake_order.price
        if cake_order.got_payment:
            cake_order_details['got_payment'] = 1
        else:
            cake_order_details['got_payment'] = 0
        if cake_order.cake_finished:
            cake_order_details['cake_finished'] = 1
            cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
            cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
        else:
            cake_order_details['cake_finished'] = 0
        if cake_order.canceled:
            cake_order_details['canceled'] = 1
        else:
            cake_order_details['canceled'] = 0
        if cake_order.customer_recieved_cake:
            cake_order_details['customer_recieved_cake'] = 1
            cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
            cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
        else:
            cake_order_details['customer_recieved_cake'] = 0
        return cake_order_details
    elif language == "tr":
        cake_order_details['inside'] = if_null(cake_order.inside, 'description_tr')
        cake_order_details['cakebatter'] = if_null(cake_order.cakebatter, 'name_tr')
        cake_order_details['outside_content'] = if_null(cake_order.outside_content, 'name_tr')
        cake_order_details['outside_colour'] = if_null(cake_order.outside_colour, 'name_tr')
        cake_order_details['persons'] = cake_order.persons
        cake_order_details['form'] = if_null(cake_order.form, 'description_tr')
        cake_order_details['floors'] = cake_order.floors
        if cake_order.picture:
            cake_order_details[
                'picture'] = f'{root}{cake_order.picture.url}'
        if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
        id_list = []
        id_reference_list = {}
        for deko_object in cake_order.deko.all():
            id_list.append(deko_object.deko_model.id)
        deko_list = []
        for deko_object in cake_order.deko.all():
            id_reference_list[deko_object.deko_model.id] = deko_object.amount
        for deko in Deko.objects.all():
            if deko.id in id_list:
                deko_details = {}
                deko_details['id'] = deko.id
                deko_details['description'] = deko.description_tr
                deko_details['price'] = deko.price
                deko_details['amount'] = id_reference_list[deko.id]
                deko_list.append(deko_details)
            else:
                deko_details = {}
                deko_details['id'] = deko.id
                deko_details['description'] = deko.description_tr
                deko_details['price'] = deko.price
                deko_details['amount'] = 0
                deko_list.append(deko_details)
        cake_order_details['dekos'] = deko_list
        if cake_order.text:
            cake_order_details['text'] = cake_order.text
            if cake_order.textmaterial == 'Helle Schrift':
                cake_order_details['text_material'] = 'Beyaz Yazı'
            if cake_order.textmaterial == 'Dunkle Schrift':
                cake_order_details['text_material'] = 'Siyah Yazı'
        cake_order_details['order_date'] = str(cake_order.order_date)
        cake_order_details['order_time'] = str(cake_order.order_time)[:5]
        cake_order_details['deadline_date'] = str(cake_order.deadline_date)
        cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
        cake_order_details['customer_name'] = cake_order.customer_name
        cake_order_details['customer_surname'] = cake_order.customer_surname
        cake_order_details['customer_phone'] = cake_order.customer_phone
        cake_order_details['customer_mail'] = cake_order.customer_mail
        cake_order_details['customer_info'] = cake_order.customer_info
        cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
        cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
        cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
        cake_order_details['price'] = cake_order.price
        if cake_order.got_payment:
            cake_order_details['got_payment'] = 1
        else:
            cake_order_details['got_payment'] = 0
        if cake_order.cake_finished:
            cake_order_details['cake_finished'] = 1
            cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
            cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
        else:
            cake_order_details['cake_finished'] = 0
        if cake_order.canceled:
            cake_order_details['canceled'] = 1
        else:
            cake_order_details['canceled'] = 0
        if cake_order.customer_recieved_cake:
            cake_order_details['customer_recieved_cake'] = 1
            cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
            cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
        else:
            cake_order_details['customer_recieved_cake'] = 0
        return cake_order_details

@api.get('/get-cake-orders')
def get_cake_orders(request, language:str):
    cake_orders = CakeOrder.objects.filter(canceled=False).order_by('-id')
    cake_order_list = []
    for cake_order in cake_orders:
        cake_order_details = {}
        if cake_order.cake_model:
            cake_order_details['type'] = 'catalog_cake_order'
            cake_order_details['cake_model'] = str(cake_order.cake_model)
        else:
            cake_order_details['type'] = 'custom_cake_order'
        cake_order_details['order_id'] = str(cake_order.order_id)
        if language == "de":
            cake_order_details['inside'] = str(cake_order.inside)
            cake_order_details['cakebatter'] = str(cake_order.cakebatter)
            cake_order_details['outside_content'] = str(cake_order.outside_content)
            cake_order_details['outside_colour'] = str(cake_order.outside_colour)
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = str(cake_order.form)
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                cake_order_details['text_material'] = cake_order.textmaterial
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
        elif language == "tr":
            cake_order_details['inside'] = if_null(cake_order.inside, 'description_tr')
            cake_order_details['cakebatter'] = if_null(cake_order.cakebatter, 'name_tr')
            cake_order_details['outside_content'] = if_null(cake_order.outside_content, 'name_tr')
            cake_order_details['outside_colour'] = if_null(cake_order.outside_colour, 'name_tr')
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = if_null(cake_order.form, 'description_tr')
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                if cake_order.textmaterial == 'Helle Schrift':
                    cake_order_details['text_material'] = 'Beyaz Yazı'
                if cake_order.textmaterial == 'Dunkle Schrift':
                    cake_order_details['text_material'] = 'Siyah Yazı'
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
    return cake_order_list


@api.get('/get-active-cake-orders')
def get_active_cake_orders(request, language:str):
    cake_orders = CakeOrder.objects.filter(customer_recieved_cake=False, canceled=False).order_by('-id')
    cake_order_list = []
    for cake_order in cake_orders:
        cake_order_details = {}
        if cake_order.cake_model:
            cake_order_details['type'] = 'catalog_cake_order'
            cake_order_details['cake_model'] = str(cake_order.cake_model)
        else:
            cake_order_details['type'] = 'custom_cake_order'
        cake_order_details['order_id'] = str(cake_order.order_id)
        if language == "de":
            cake_order_details['inside'] = str(cake_order.inside)
            cake_order_details['cakebatter'] = str(cake_order.cakebatter)
            cake_order_details['outside_content'] = str(cake_order.outside_content)
            cake_order_details['outside_colour'] = str(cake_order.outside_colour)
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = str(cake_order.form)
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                cake_order_details['text_material'] = cake_order.textmaterial
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
        elif language == "tr":
            cake_order_details['inside'] = if_null(cake_order.inside ,'description_tr')
            cake_order_details['cakebatter'] = if_null(cake_order.cakebatter, 'name_tr')
            cake_order_details['outside_content'] = if_null(cake_order.outside_content, 'name_tr')
            cake_order_details['outside_colour'] = if_null(cake_order.outside_colour, 'name_tr')
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = if_null(cake_order.form, 'description_tr')
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                if cake_order.textmaterial == 'Helle Schrift':
                    cake_order_details['text_material'] = 'Beyaz Yazı'
                if cake_order.textmaterial == 'Dunkle Schrift':
                    cake_order_details['text_material'] = 'Siyah Yazı'
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
    return cake_order_list


@api.get('/get-past-cake_orders')
def get_past_cake_orders(request, language:str):
    cake_orders = CakeOrder.objects.filter(customer_recieved_cake=True, canceled=False).order_by('-id')
    cake_order_list = []
    for cake_order in cake_orders:
        cake_order_details = {}
        if cake_order.cake_model:
            cake_order_details['type'] = 'catalog_cake_order'
            cake_order_details['cake_model'] = str(cake_order.cake_model)
        else:
            cake_order_details['type'] = 'custom_cake_order'
        cake_order_details['order_id'] = str(cake_order.order_id)
        if language == "de":
            cake_order_details['inside'] = str(cake_order.inside)
            cake_order_details['cakebatter'] = str(cake_order.cakebatter)
            cake_order_details['outside_content'] = str(cake_order.outside_content)
            cake_order_details['outside_colour'] = str(cake_order.outside_colour)
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = str(cake_order.form)
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                cake_order_details['text_material'] = cake_order.textmaterial
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
        elif language == "tr":
            cake_order_details['inside'] = if_null(cake_order.inside, 'description_tr')
            cake_order_details['cakebatter'] = if_null(cake_order.cakebatter, 'name_tr')
            cake_order_details['outside_content'] = if_null(cake_order.outside_content, 'name_tr')
            cake_order_details['outside_colour'] = if_null(cake_order.outside_colour, 'name_tr')
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = if_null(cake_order.form, 'description_tr')
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                if cake_order.textmaterial == 'Helle Schrift':
                    cake_order_details['text_material'] = 'Beyaz Yazı'
                if cake_order.textmaterial == 'Dunkle Schrift':
                    cake_order_details['text_material'] = 'Siyah Yazı'
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
    return cake_order_list


@api.get('/pasta-ustasi')
def pasta_ustasi(request, language:str):
    cake_orders = CakeOrder.objects.filter(cake_finished=False, got_payment=True, customer_recieved_cake=False, canceled=False).order_by('-id')
    cake_order_list = []
    for cake_order in cake_orders:
        cake_order_details = {}
        if cake_order.cake_model:
            cake_order_details['type'] = 'catalog_cake_order'
            cake_order_details['cake_model'] = str(cake_order.cake_model)
        else:
            cake_order_details['type'] = 'custom_cake_order'
        cake_order_details['order_id'] = str(cake_order.order_id)
        if language == "de":
            cake_order_details['inside'] = str(cake_order.inside)
            cake_order_details['cakebatter'] = str(cake_order.cakebatter)
            cake_order_details['outside_content'] = str(cake_order.outside_content)
            cake_order_details['outside_colour'] = str(cake_order.outside_colour)
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = str(cake_order.form)
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                cake_order_details['text_material'] = cake_order.textmaterial
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
        elif language == "tr":
            cake_order_details['inside'] = if_null(cake_order.inside, 'description_tr')
            cake_order_details['cakebatter'] = if_null(cake_order.cakebatter, 'name_tr')
            cake_order_details['outside_content'] = if_null(cake_order.outside_content, 'name_tr')
            cake_order_details['outside_colour'] = if_null(cake_order.outside_colour, 'name_tr')
            cake_order_details['persons'] = cake_order.persons
            cake_order_details['form'] = if_null(cake_order.form, 'description_tr')
            cake_order_details['floors'] = cake_order.floors
            if cake_order.picture:
                cake_order_details[
                    'picture'] = f'{root}{cake_order.picture.url}'
            if cake_order.example_picture:
                cake_order_details[
                    'example_picture'] = f'{root}{cake_order.example_picture.url}'
            id_list = []
            id_reference_list = {}
            for deko_object in cake_order.deko.all():
                id_list.append(deko_object.deko_model.id)
            deko_list = []
            for deko_object in cake_order.deko.all():
                id_reference_list[deko_object.deko_model.id] = deko_object.amount
            for deko in Deko.objects.all():
                if deko.id in id_list:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = id_reference_list[deko.id]
                    deko_list.append(deko_details)
                else:
                    deko_details = {}
                    deko_details['id'] = deko.id
                    deko_details['description'] = deko.description_tr
                    deko_details['price'] = deko.price
                    deko_details['amount'] = 0
                    deko_list.append(deko_details)
            cake_order_details['dekos'] = deko_list
            if cake_order.text:
                cake_order_details['text'] = cake_order.text
                if cake_order.textmaterial == 'Helle Schrift':
                    cake_order_details['text_material'] = 'Beyaz Yazı'
                if cake_order.textmaterial == 'Dunkle Schrift':
                    cake_order_details['text_material'] = 'Siyah Yazı'
            cake_order_details['order_date'] = str(cake_order.order_date)
            cake_order_details['order_time'] = str(cake_order.order_time)[:5]
            cake_order_details['deadline_date'] = str(cake_order.deadline_date)
            cake_order_details['deadline_time'] = str(cake_order.deadline_time)[:5]
            cake_order_details['customer_name'] = cake_order.customer_name
            cake_order_details['customer_surname'] = cake_order.customer_surname
            cake_order_details['customer_phone'] = cake_order.customer_phone
            cake_order_details['customer_mail'] = cake_order.customer_mail
            cake_order_details['customer_info'] = cake_order.customer_info
            cake_order_details['shop_assistant_order'] = str(cake_order.shop_assistant_order)
            cake_order_details['shop_assistant_delivery'] = str(cake_order.shop_assistant_delivery)
            cake_order_details['shop_assistant_info'] = cake_order.shop_assistant_info
            cake_order_details['price'] = cake_order.price
            if cake_order.got_payment:
                cake_order_details['got_payment'] = 1
            else:
                cake_order_details['got_payment'] = 0
            if cake_order.cake_finished:
                cake_order_details['cake_finished'] = 1
                cake_order_details['cake_finished_date'] = str(cake_order.cake_finished_date)
                cake_order_details['cake_finished_time'] = str(cake_order.cake_finished_time)[:5]
            else:
                cake_order_details['cake_finished'] = 0
            if cake_order.canceled:
                cake_order_details['canceled'] = 1
            else:
                cake_order_details['canceled'] = 0
            if cake_order.customer_recieved_cake:
                cake_order_details['customer_recieved_cake'] = 1
                cake_order_details['customer_revieved_cake_date'] = cake_order.customer_recieved_date
                cake_order_details['customer_revieved_cake_time'] = str(cake_order.customer_recieved_time)[:5]
            else:
                cake_order_details['customer_recieved_cake'] = 0
            cake_order_list.append(cake_order_details)
    return cake_order_list


@api.post('/got-payment/{order_id}')
def got_payment(request, order_id):
    order = get_object_or_404(CakeOrder, order_id=order_id)
    order.got_payment = True
    order.save()
    return f'{order.order_id}_got_payment'


@api.post('/canceled/{order_id}')
def canceled(request, order_id):
    order = get_object_or_404(CakeOrder, order_id=order_id)
    order.canceled = True
    order.save()
    return f'{order.order_id}_canceled'


@api.post('/cake-finished/{order_id}')
def cake_finished(request, order_id):
    order = get_object_or_404(CakeOrder, order_id=order_id)
    order.cake_finished = True
    from datetime import datetime
    from pytz import timezone
    recieved_date = datetime.now(timezone('Europe/Berlin')).date()
    revieved_time = datetime.now(timezone('Europe/Berlin')).time()
    order.cake_finished_date = recieved_date
    order.cake_finished_time = revieved_time
    order.save()
    return f'{order.order_id}_cake_finished'


@api.post('customer_recieved_cake/{order_id}/{shop_assistant}')
def customer_recieved_cake(request, order_id, shop_assistant):
    sa = shop_assistant
    order = get_object_or_404(CakeOrder, order_id=order_id)
    def get_shop_assistant():
        shop_assistant = get_object_or_404(
            CakeShopAssistant, name=sa)
        return shop_assistant
    order.customer_recieved_cake = True
    order.shop_assistant_delivery = get_shop_assistant()
    from datetime import datetime
    from pytz import timezone
    recieved_date = datetime.now(timezone('Europe/Berlin')).date()
    revieved_time = datetime.now(timezone('Europe/Berlin')).time()
    order.customer_recieved_date = recieved_date
    order.customer_recieved_time = revieved_time
    order.save()
    return f'{order.order_id}_customer_recieved_cake_by_{str(order.shop_assistant_delivery)}_{recieved_date}_{revieved_time}'


@api.post('/create-cake-order')
def create_cake_order(request, cake_order_schema: CakeOrderSchema = Form(...)):
    def order_id_maker():
        test_number = randint(10000, 99999)
        while CakeOrder.objects.filter(order_id=test_number).exists():
            test_number = randint(10000, 99999)
        return test_number

    def get_inside():
        if cake_order_schema.language == 'de':
            inside = get_object_or_404(
                Inside, description=cake_order_schema.inside)
        elif cake_order_schema.language == 'tr':
            inside = get_object_or_404(
                Inside, description_tr=cake_order_schema.inside)
        return inside

    def get_cakebatter():
        if cake_order_schema.language == 'de':
            cakebatter = get_object_or_404(
                CakeBatter, name=cake_order_schema.cakebatter)
        elif cake_order_schema.language == 'tr':
            cakebatter = get_object_or_404(
                CakeBatter, name_tr=cake_order_schema.cakebatter)
        return cakebatter

    def get_outside_content():
        if cake_order_schema.language == 'de':
            outside_content = get_object_or_404(
                OutsideContent, name=cake_order_schema.outside_content)
        elif cake_order_schema.language == 'tr':
            outside_content = get_object_or_404(
                OutsideContent, name_tr=cake_order_schema.outside_content)
        return outside_content

    def get_outside_colour():
        if cake_order_schema.language == 'de':
            outside_colour = get_object_or_404(
                OutsideColours, name=cake_order_schema.outside_colour)
        elif cake_order_schema.language == 'tr':
            outside_colour = get_object_or_404(
                OutsideColours, name_tr=cake_order_schema.outside_colour)
        return outside_colour

    def get_cake_form():
        if cake_order_schema.language == 'de':
            cake_form = get_object_or_404(
                CakeForm, description=cake_order_schema.form)
        elif cake_order_schema.language == 'tr':
            cake_form = get_object_or_404(
                CakeForm, description_tr=cake_order_schema.form)
        return cake_form

    def get_shop_assistant():
        shop_assistant = get_object_or_404(
            CakeShopAssistant, name=cake_order_schema.shop_assistant_order)
        return shop_assistant
    
    def get_catalog_cake_model():
        if cake_order_schema.cake_model:
            cake_model = get_object_or_404(CatalogCake, cake_nr=cake_order_schema.cake_model)
        else:
            cake_model = None
        return cake_model
    
    def get_text_material():
        if cake_order_schema.language == 'de':
            return cake_order_schema.text_material
        elif cake_order_schema.language == 'tr':
            if cake_order_schema.text_material == 'Beyaz Yazı':
                return 'Helle Schrift'
            elif cake_order_schema.text_material == 'Siyah Yazı':
                return 'Dunkle Schrift'

    cake_order = CakeOrder.objects.create(order_id=order_id_maker(), cake_model=get_catalog_cake_model(), inside=get_inside(),
                                          cakebatter=get_cakebatter(),
                                          outside_content=get_outside_content(),
                                          outside_colour=get_outside_colour(),
                                          persons=cake_order_schema.persons, form=get_cake_form(),
                                          floors=cake_order_schema.floors,
                                          text=cake_order_schema.text,
                                          textmaterial=get_text_material(),
                                          deadline_date=cake_order_schema.deadline_date,
                                          deadline_time=cake_order_schema.deadline_time,
                                          customer_name=cake_order_schema.customer_name,
                                          customer_surname=cake_order_schema.customer_surname,
                                          customer_phone=cake_order_schema.customer_phone,
                                          customer_mail=cake_order_schema.customer_mail,
                                          customer_info=cake_order_schema.customer_info,
                                          shop_assistant_info=cake_order_schema.shop_assistant_info,
                                          price=cake_order_schema.price, shop_assistant_order=get_shop_assistant())
    if cake_order_schema.deko:
        dekos = str(cake_order_schema.deko[0]).split(',')
        n = 1
        while n < len(dekos):
            cake_order.deko.add(DekoOrder.objects.create(deko_model=Deko.objects.get(id=dekos[n - 1]), amount=dekos[n]))
            n += 2
    return {'created_cake_order': cake_order.order_id}


@api.post('/cake-order-add-picture')
def cake_order_add_picture(request, order_id: int = Form(...), picture: UploadedFile = File(...)):
    order = get_object_or_404(CakeOrder, order_id=order_id)
    order.picture = picture
    order.save()
    image_url = f'{root}{order.picture.url}'
    return {'url': image_url}


@api.post('/cake-order-add-example-picture')
def cake_order_add_example_picture(request, order_id: int = Form(...), picture: UploadedFile = File(...)):
    order = get_object_or_404(CakeOrder, order_id=order_id)
    order.example_picture = picture
    order.save()
    image_url = f'{root}{order.example_picture.url}'
    return {'url': image_url}


@api.post('/create-catalog-cake-model')
def create_catalog_cake_model(request, catalog_cake_schema: CatalogCakeSchema = Form(...)):
    def get_inside():
        inside = get_object_or_404(
            Inside, description=catalog_cake_schema.inside)
        return inside

    def get_cakebatter():
        cakebatter = get_object_or_404(
            CakeBatter, name=catalog_cake_schema.cakebatter)
        return cakebatter

    def get_outside_content():
        outside_content = get_object_or_404(
            OutsideContent, name=catalog_cake_schema.outside_content)
        return outside_content

    def get_outside_colour():
        outside_colour = get_object_or_404(
            OutsideColours, name=catalog_cake_schema.outside_colour)
        return outside_colour

    def get_cake_form():
        cake_form = get_object_or_404(
            CakeForm, description=catalog_cake_schema.form)
        return cake_form

    catalog_cake = CatalogCake.objects.create(cake_nr=catalog_cake_schema.cake_nr, name=catalog_cake_schema.name,
                                              description=catalog_cake_schema.description,
                                              inside=get_inside(),
                                              cakebatter=get_cakebatter(),
                                              outside_content=get_outside_content(),
                                              outside_colour=get_outside_colour(),
                                              persons=catalog_cake_schema.persons, form=get_cake_form(),
                                              floors=catalog_cake_schema.floors,
                                              price=catalog_cake_schema.price)
    if catalog_cake_schema.deko:
        deko_list = [i.split(',') for i in catalog_cake_schema.deko]
        for deko in deko_list[0]:
            catalog_cake.deko.add(Deko.objects.get(description=deko))
    return {'created_cake_order': catalog_cake.cake_nr}



@api.post('/update-custom-cake-order')
def update_custom_cake_order(request, data: UpdateCustomCakeSchema = Form(...)):
    order = CakeOrder.objects.get(order_id=data.order_id)

    def get_inside():
        if data.language == 'de':
            inside = get_object_or_404(
                Inside, description=data.inside)
        elif data.language == 'tr':
            inside = get_object_or_404(
                Inside, description_tr=data.inside)
        return inside

    def get_cakebatter():
        if data.language == 'de':
            cakebatter = get_object_or_404(
                CakeBatter, name=data.cakebatter)
        elif data.language == 'tr':
            cakebatter = get_object_or_404(
                CakeBatter, name_tr=data.cakebatter)
        return cakebatter

    def get_outside_content():
        if data.language == 'de':
            outside_content = get_object_or_404(
                OutsideContent, name=data.outside_content)
        elif data.language == 'tr':
            outside_content = get_object_or_404(
                OutsideContent, name_tr=data.outside_content)
        return outside_content

    def get_outside_colour():
        if data.language == 'de':
            outside_colour = get_object_or_404(
                OutsideColours, name=data.outside_colour)
        elif data.language == 'tr':
            outside_colour = get_object_or_404(
                OutsideColours, name_tr=data.outside_colour)
        return outside_colour

    def get_cake_form():
        if data.language == 'de':
            cake_form = get_object_or_404(
                CakeForm, description=data.form)
        elif data.language == 'tr':
            cake_form = get_object_or_404(
                CakeForm, description_tr=data.form)
        return cake_form
    
    def get_shop_assistant():
        shop_assistant = get_object_or_404(
            CakeShopAssistant, name=data.shop_assistant_order)
        return shop_assistant

    changed = {}
    if data:
        if data.inside:
            old_inside = order.inside
            order.inside = get_inside()
            changed['inside'] = f'{old_inside} changed to => {order.inside}'
        if data.cakebatter:
            old_cakebatter = order.cakebatter
            order.cakebatter = get_cakebatter()
            changed['cakebatter'] = f'{old_cakebatter} changed to => {order.cakebatter}'
        if data.outside_content:
            old_outside_content = order.outside_content
            order.outside_content = get_outside_content()
            changed['outside_content'] = f'{old_outside_content} changed to => {order.outside_content}'
        if data.outside_colour:
            old_outside_colour = order.outside_colour
            order.outside_colour = get_outside_colour()
            changed['outside_colour'] = f'{old_outside_colour} changed to => {order.outside_colour}'
        if data.persons:
            old_persons = order.persons
            order.persons = data.persons
            changed['persons'] = f'{old_persons} changed to => {order.persons}'
        if data.form:
            old_form = order.form
            order.form = get_cake_form()
            changed['form'] = f'{old_form} changed to => {order.form}'
        if data.floors:
            old_floors = order.floors
            order.floors = data.floors
            changed['floors'] = f'{old_floors} changed to => {order.floors}'
        if data.deko:
            old_dekos = order.deko.all()
            old_dekos_list = []
            for deko in old_dekos:
                old_dekos_list.append(deko)
            order.deko.all().delete()
            dekos = str(data.deko[0]).split(',')
            n = 1
            while n < len(dekos):
                if dekos[n] != 0:
                    order.deko.add(
                        DekoOrder.objects.create(deko_model=Deko.objects.get(id=dekos[n - 1]), amount=dekos[n]))
                    n += 2
            new_dekos_list = []
            for deko in order.deko.all():
                new_dekos_list.append(deko)
            changed['dekos'] = f'{old_dekos_list} changed to => {new_dekos_list}'
        if data.text:
            old_text = order.text
            order.text = data.text
            changed['text'] = f'{old_text} changed to => {order.text}'
        if data.text_material:
            old_text_material = order.textmaterial
            if data.language == 'de':
                order.textmaterial = data.text_material
                changed['text_material'] = f'{old_text_material} changed to => {order.textmaterial}'
            elif data.language == 'tr':
                if data.text_material == 'Beyaz Yazı':
                    order.textmaterial = 'Helle Schrift'
                elif data.text_material == 'Siyah Yazı':
                    order.textmaterial = 'Dunkle Schrift'
            changed['text_material'] = f'{old_text_material} changed to => {order.textmaterial}'
        if data.deadline_date:
            old_deadline_date = order.deadline_date
            order.deadline_date = data.deadline_date
            changed['deadline_date'] = f'{old_deadline_date} changed to => {order.deadline_date}'
        if data.deadline_time:
            old_deadline_time = order.deadline_time
            order.deadline_time = data.deadline_time
            changed['deadline_time'] = f'{old_deadline_time} changed to => {order.deadline_time}'
        if data.customer_name:
            old_customer_name = order.customer_name
            order.customer_name = data.customer_name
            changed['customer_name'] = f'{old_customer_name} changed to => {order.customer_name}'
        if data.customer_surname:
            old_customer_surname = order.customer_surname
            order.customer_surname = data.customer_surname
            changed['customer_name'] = f'{old_customer_surname} changed to => {order.customer_surname}'
        if data.customer_phone:
            old_customer_phone = order.customer_phone
            order.customer_phone = data.customer_phone
            changed['customer_phone'] = f'{old_customer_phone} changed to => {order.customer_phone}'
        if data.customer_mail:
            old_customer_mail = order.customer_mail
            order.customer_mail = data.customer_mail
            changed['customer_mail'] = f'{old_customer_mail} changed to => {order.customer_mail}'
        if data.customer_info:
            old_customer_info = order.customer_info
            order.customer_info = data.customer_info
            changed['customer_info'] = f'{old_customer_info} changed to => {order.customer_info}'
        if data.shop_assistant_order:
            old_shop_assistant_order = order.shop_assistant_order
            order.shop_assistant_order = get_shop_assistant()
            changed['shop_assistant_order'] = f'{old_shop_assistant_order} changed to => {order.shop_assistant_order}'
        if data.shop_assistant_info:
            old_shop_assistant_info = order.shop_assistant_info
            order.shop_assistant_info = data.shop_assistant_info
            changed['shop_assistant_info'] = f'{old_shop_assistant_info} changed to => {order.shop_assistant_info}'
        if data.price:
            old_price = order.price
            order.price = data.price
            changed['price'] = f'{old_price} changed to => {order.price}'
        order.save()
    return changed



