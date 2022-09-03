from math import ceil
from django.shortcuts import render
from App.models import User, Recording, Composer, get_all_available_composers
from App.utils.search import default_search
from django.conf import settings
from django.db.models import Count
from django.utils.translation import gettext as _

def render_index(OriginalRequest, SelectedTag=None, SelectedPage=None) :

    HavePages = True

    if SelectedTag is None :
        SelectedTag = "timeline"
    
    if SelectedPage is None :
        SelectedPage = 0
        HavePages = False

    SelectedItems = []
    AllComposers = []
    PageNum = 0

    if SelectedTag == "timeline" :
        RecordingList = Recording.objects.order_by('-UploadTime')
        PageNum = ceil(len(RecordingList)/settings.ITEMS_PER_PAGE)
        SelectedItems = RecordingList[SelectedPage*settings.ITEMS_PER_PAGE : (SelectedPage+1)*settings.ITEMS_PER_PAGE]
        HavePages = True
    elif SelectedTag == "members" :
        # annotate means count the related recordings of a user and save the result as a key
        UserList = User.objects.annotate(NumRecordings=Count('Recordings'))
        PageNum = ceil(len(UserList)/settings.ITEMS_PER_PAGE)
        SelectedItems = UserList[SelectedPage*settings.ITEMS_PER_PAGE: (SelectedPage+1)*settings.ITEMS_PER_PAGE]
        HavePages = True
    elif SelectedTag == "search" :
        SearchResults = default_search(OriginalRequest.POST.get('Keyword'))
        PageNum = ceil(len(SearchResults)/settings.ITEMS_PER_PAGE)
        SelectedItems = SearchResults[SelectedPage*settings.ITEMS_PER_PAGE: (SelectedPage+1)*settings.ITEMS_PER_PAGE]
        HavePages = True
    elif SelectedTag == "upload" :
        AllComposers = get_all_available_composers()
        HavePages = False
    elif SelectedTag == "composers" :
        AllComposers = get_all_available_composers()
        HavePages = True
    elif SelectedTag == "about" :
        HavePages = False
    
    context                 = {}
    context['hello']        = _('PKUpiano Sound Library!')
    context['List']         = SelectedItems
    context['SelectedTag']  = SelectedTag
    context['CurrentPage']  = SelectedPage
    context['AllComposers'] = AllComposers
    context['HavePages']    = HavePages
    context['PageRange']    = list(range(max(0, SelectedPage-2), min(PageNum, SelectedPage+3)))
    context['PagePrefix']   = '/index/'+SelectedTag+'/'
    context['PrevPage']     = max(0, SelectedPage-1)
    context['NextPage']     = max(min(PageNum-1, SelectedPage+1), 0)

    for item in context['List'] :
        if isinstance(item, User) :
            item.view(verbose=False)
    
    # context['user_authenticated'] = original_request.user.is_authenticated

    return render(OriginalRequest, 'index_{}.html'.format(SelectedTag), context)