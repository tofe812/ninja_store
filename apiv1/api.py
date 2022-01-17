# from django.shortcuts import get_object_or_404
# from ninja import Router
# from ninja.orm import create_schema
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
# from typing import List
#
# from django.contrib.auth.models import User
from .models import Company, Category, Product, Cart, CartItem
from .routers.company import company_router
from .routers.product import product_router

api = NinjaExtraAPI(version='1.0')
api.register_controllers(NinjaJWTDefaultController)

api.add_router('/companies', company_router, auth=JWTAuth())
api.add_router('/products', product_router)







def cart(request):
    customer = request.user
    order, created = Cart.objects.get_or_create(user=customer)
    order_items = CartItem.objects.filter(cart=order)
    list_data = {}
    print(list_data)
    list_data['customer'] = customer.first_name + ' ' + customer.last_name
    list_data['total_price'] = 0
    list_data['products'] = {}

    count = 0
    for item in order.get_cart():
        count += 1
        list_data['total_price'] += item.product.price * item.quantity
        list_data['products'][count] = {'item': item.product.name,
                                        'quantity': item.quantity,
                                        'price': item.product.price}
    print(list_data)
    print('\n\n\n\n\n')
    return list_data

dis_list = [
    {
        'discount_name': 'dsp30',
        'discount_type': 'percentage',
        'max_discount': '3000',
        'discount_value': '30',
        'active': True,
    },
    {
        'discount_name': 'dsf3000',
        'discount_type': 'fixed',
        'max_discount': '3000',
        'discount_value': '3000',
        'active': True,
    },
]


@api.get('/cart/')
def test(request):
    if request.user.is_authenticated:
        return cart(request)
    return {'message': 'You are not logged in'}


@api.get('/checkout/')
def test2(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Cart.objects.get_or_create(user=customer)
        list_data = {}
        print(list_data)
        list_data['customer'] = customer.first_name + ' ' + customer.last_name
        list_data['total_price'] = order.total

        total_price = list_data['total_price']
        get_discount_id = 0

        discount = dis_list[get_discount_id]
        discount_price = 0

        if discount['active']:
            print('Discount is active')
            print(discount['discount_type'])
            if discount['discount_type'] == 'percentage':
                discount_value = float(total_price) * float(discount['discount_value']) / 100
                if discount_value > float(discount['max_discount']):
                    discount_value = round(float(discount['max_discount']), 2)
                print(discount_value)
                discount_price = round(float(total_price) - discount_value, 2)
            elif discount['discount_type'] == 'fixed':
                if float(discount['discount_value']) >= total_price:
                    print('its free!!')
                else:
                    discount_value = round(discount['discount_value'], 2)
                    discount_price = round(float(total_price) - float(discount_value), 2)

            else:
                print('Invalid discount type')
                discount = 0
                discount_price = 0
                discount_value = 0

        else:
            print('Discount is not active')
            discount = 0
            discount_price = 0
            discount_value = 0
        list_data['discount'] = discount
        list_data['discount_price'] = discount_price
        list_data['discount_value'] = discount_value


        print(list_data)
        print('\n\n\n\n\n')
        return list_data
    return {'message': 'You are not logged in'}




