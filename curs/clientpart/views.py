from django.shortcuts import render


def index(request):
    return render(request, 'all_campaigns.html', {})
