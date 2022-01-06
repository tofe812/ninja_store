from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.orm import create_schema
from typing import List
from apiv1.models import Company


company_router = Router(tags=['company'])

CompanyIn = create_schema(Company, exclude=['id'])
CompanyOut = create_schema(Company)


@company_router.post('')
def create_company(request, payload: CompanyIn):
    print(payload.dict())
    test = payload.dict()
    company = Company.objects.create(**test)
    return {'id': company.id}


@company_router.get('/{id}', response=CompanyOut)
def get_company(request, id: int):
    company = get_object_or_404(Company, id=id)
    return company


@company_router.get('', response=List[CompanyOut])
def list_companys(request):
    qs = Company.objects.all()
    return qs


@company_router.put('/{id}')
def update_company(request, id: int, payload: CompanyIn):
    company = get_object_or_404(Company, id=id)
    test = payload.dict()
    for attr, value in test.items():
        setattr(company, attr, value)
    company.save()
    return {"success": True}


@company_router.delete('/{id}')
def delete_company(request, id: int):
    company = get_object_or_404(Company, id=id)
    company.delete()
    return {"success": True}




