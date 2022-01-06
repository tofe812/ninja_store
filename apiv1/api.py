# from django.shortcuts import get_object_or_404
# from ninja import Router
# from ninja.orm import create_schema
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
# from typing import List
#
# from django.contrib.auth.models import User
# from .models import Company, Category, Product
from .routers.company import company_router
from .routers.product import product_router

api = NinjaExtraAPI(version='1.0')
api.register_controllers(NinjaJWTDefaultController)

api.add_router('/companies', company_router, auth=JWTAuth())
api.add_router('/products', product_router)




