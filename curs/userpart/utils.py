from clientpart.models import Campaign

import logging
logger = logging.getLogger(__name__)


def get_advertisment_to_show(request):
    adv = request.session.get('last_seen_adv')
    if not adv:
        try:
            return Campaign.actives.all()[:1].get()
        except Campaign.DoesNotExist:
            return None