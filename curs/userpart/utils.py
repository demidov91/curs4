from clientpart.models import Campaign

def get_advertisment_to_show(request):
    adv = request.session.get('last_seen_adv')
    if not adv:
        try:
            adv = Campaign.actives.all()[:1].get()
        except Campaign.DoesNotExist:
            return None