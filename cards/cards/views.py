from django.http import HttpResponseRedirect
from .services.generate_device_id import gen_smth
from .models import Card, DiscountPercent

def generate_cards(request):
    print(request.POST)
    if request.POST['number'] == '':
        return HttpResponseRedirect("/cards/card/")
    for i in range(int(request.POST['number'])):
        percent = DiscountPercent.objects.get(name='default')
        card = Card(series=request.POST['series'],number=gen_smth(3),created_at=request.POST['date_start_0'],date_end=request.POST['date_end_0'],summa_purchases=0,status='Active',percent=percent)
        card.save()
    return HttpResponseRedirect("/cards/card/")
