from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.orm import create_schema
from typing import List
from apiv1.models import Company, Category, Product


product_router = Router(tags=['product'])

ProductIn = create_schema(Product, exclude=['id'])
ProductOut = create_schema(Product)


@product_router.post('')
def create_product(request, payload: ProductIn):
    print(payload.dict())
    test = payload.dict()
    test['company'] = get_object_or_404(Company, id=test['company'])
    test['category'] = get_object_or_404(Category, id=test['category'])
    product = Product.objects.create(**test)
    return {'id': product.id}


@product_router.get('/{id}', response=ProductOut)
def get_product(request, id: int):
    product = get_object_or_404(Product, id=id, is_active=True)
    return product


@product_router.get('', response=List[ProductOut])
def list_products(request):
    if request.user.groups.filter(name='SuperAdmin').exists():
        qs = Product.objects.all()
        return qs
    else:
        qs = Product.objects.filter(is_active=True)
        return qs


@product_router.put('/{id}')
def update_product(request, id: int, payload: ProductIn):
    product = get_object_or_404(Product, id=id)
    test = payload.dict()
    test['company'] = get_object_or_404(Company, id=test['company'])
    test['category'] = get_object_or_404(Category, id=test['category'])
    for attr, value in test.items():
        setattr(product, attr, value)
    product.save()
    return {"success": True}


@product_router.delete('/{id}')
def delete_product(request, id: int):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return {"success": True}