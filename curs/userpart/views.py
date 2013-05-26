from datetime import datetime


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404

from curs.utils import graph_db, datetime_serialize
from registration.utils import users_only, get_profile_node
from clientpart.models import Campaign

def show_adv(request,campaign_id):
    campaign = get_object_or_404(Campaign.objects, id=campaign_id)
    request.session['last_seen_adv'] = campaign
    campaign_node = campaign.get_node()
    is_accepted = campaign_node.is_related_to(get_profile_node(request.user), 0, Campaign.ACCEPTED_RELATION)
    return render(request, 'advert.html', {
        'campaign': campaign,
        'is_accepted': is_accepted,
        })


@users_only
def accept_adv(request, campaign_id):
    campaign_node = Campaign.nodes.get_or_none(id=campaign_id)
    if not campaign_node:
        raise Http404()
    acceptor = get_profile_node(request.user)
    graph_db.get_or_create_relationships((campaign_node, Campaign.ACCEPTED_RELATION, acceptor, {'time': datetime_serialize(datetime.now())}))
    messages.info(request, 'Proposal was successfully accepted.')
    return redirect('show_adv', campaign_id=campaign_id)