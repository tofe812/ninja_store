from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.orm import create_schema
from typing import List
from apiv1.models import Cart, CartItem, Discount
import json


cart_router = Router(tags=['cart'])

def cart_get(request):
    customer = request.user
    order, created = Cart.objects.get_or_create(user=customer)
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
        'max_discount': 5000,
        'discount_value': 30,
        'active': True,
    },
    {
        'discount_name': 'dsf3000',
        'discount_type': 'fixed',
        'max_discount': 3000,
        'discount_value': 3000,
        'active': True,
    },
]


@cart_router.get('/cart/')
def cart(request):
    if request.user.is_authenticated:
        return cart_get(request)
    return {'message': 'You are not logged in'}


@cart_router.get('/discount/{discount_name}/')
def discount(request, discount_name: str):
    if request.user.is_authenticated:
        customer = request.user
        try:
            discount = get_object_or_404(Discount, discount_name=discount_name)
        except:
            return {'message': 'Discount not found'}
        if customer in discount.user.all():
            order, created = Cart.objects.get_or_create(user=customer)
            list_data = {}
            list_data['customer'] = customer.first_name + ' ' + customer.last_name
            total_price = 0
            discount_only = 0
            final_price = 0
            products = discount.product.all()
            for item in order.get_cart():
                total_price += float(item.product.price * item.quantity)
                for product in products:
                    if item.product == product:
                        discount_only += float(item.product.price * item.quantity)
                        list_data['discount_only'] = discount_only
            list_data['not_in_discount'] = total_price - discount_only

            list_data['total_price'] = total_price

            if discount.active:
                print(discount.discount_type)
                if discount.discount_type == 'Percentage':
                    discount_value = float(discount_only) * float(discount.discount_value) / 100
                    if discount_value > float(discount.max_discount):
                        list_data['discount_value'] = round(float(discount.max_discount), 2)
                    else:
                        list_data['discount_value'] = round(discount_value, 2)
                    discount_price = round(float(discount_only) - discount_value, 2)
                    list_data['discounted_price'] = discount_price
                elif discount.discount_type == 'Fixed':
                    if float(discount.max_discount) >= discount_only:
                        list_data['discount_value'] = int(discount_only)
                        list_data['discounted_price'] = 0
                        list_data['message'] = 'its free'
                    else:
                        discount_value = round(discount.discount_value, 2)
                        list_data['discount_value'] = discount_value
                        discount_price = round(float(total_price) - float(discount_value), 2)
                        list_data['discounted_price'] = discount_price

                else:
                    return {'message': 'Discount type not found'}
                list_data['final_price'] = list_data['not_in_discount'] + list_data['discounted_price']
                return list_data

            return {'message': 'You already have this discount'}
        return {'message': 'You are not eligible for this discount'}
    return {'message': 'You are not logged in'}


# old method
@cart_router.get('/checkout/', deprecated=True)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Cart.objects.get_or_create(user=customer)
        list_data = {}
        list_data['customer'] = customer.first_name + ' ' + customer.last_name
        list_data['total_price'] = 0
        for item in order.get_cart():
            list_data['total_price'] += item.product.price * item.quantity

        total_price = list_data['total_price']
        get_discount_id = 0

        discount = dis_list[get_discount_id]
        list_data['discount'] = discount

        discount_price = 0
        discount_value = 0

        # check if discount is active
        if discount['active']:
            # check if discount is fixed or percentage
            if discount['discount_type'] == 'percentage':
                discount_value = float(total_price) * float(discount['discount_value']) / 100
                # check if discount is less than max discount
                if discount_value > float(discount['max_discount']):
                    list_data['discount_value'] = round(float(discount['max_discount']), 2)
                else:
                    list_data['discount_value'] = round(discount_value, 2)
                discount_price = round(float(total_price) - discount_value, 2)
                list_data['discount_price'] = discount_price
            elif discount['discount_type'] == 'fixed':
                # check if discount is less than max discount
                if float(discount['discount_value']) >= total_price:
                    list_data['discount_value'] = int(total_price)
                    list_data['discount_price'] = 0

                else:
                    discount_value = round(discount['discount_value'], 2)
                    print(discount_value)
                    list_data['discount_value'] = discount_value
                    discount_price = round(float(total_price) - float(discount_value), 2)
                    list_data['discount_price'] = discount_price
        return list_data
    return {'message': 'You are not logged in'}



