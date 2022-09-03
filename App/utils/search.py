from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from App.models import Recording, User, Composer
from django.db.models import Count
from django.contrib.postgres.search import TrigramDistance, TrigramSimilarity
from django.db.models.functions import Greatest
from SoundLib import settings

def obtain_result_by_search_rank(database, keyword, search_vector) :

    search_query = SearchQuery(keyword)
    results = database.objects.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(search=search_query).order_by('-rank')
    return results

def obtain_result_by_trigram_dist(database, fields, keyword) :

    results = database.objects.annotate(
        similarity=Greatest(
            *[TrigramSimilarity(search_field, keyword) for search_field in fields]
        )
    ).filter(similarity__gt=settings.SAERCH_SIMILARITY_THRSHOLD).order_by('-similarity')
    return results

def default_search(keyword) :

    RecordingSearchVector = \
        SearchVector('Name', weight='A')+\
        SearchVector('Composer__Name', weight='B')+\
        SearchVector('UploadUserName', weight='C')+\
        SearchVector('UploadUser__username', weight='C')+\
        SearchVector('Description', weight='D')
    
    UserSearchVector = \
        SearchVector('username', weight='A')+\
        SearchVector('Introduction', weight='D')
    
    ComposerSearchVector = \
        SearchVector('Name', weight='A')+\
        SearchVector('Introduction', weight='D')

    # RecordingSearchResults = obtain_result_by_search_rank(Recording, keyword, RecordingSearchVector)
    # UserSearchResults = obtain_result_by_search_rank(User, keyword, UserSearchVector).annotate(NumRecordings=Count('Recordings'))
    # ComposerSearchResults = obtain_result_by_search_rank(Composer, keyword, ComposerSearchVector)

    RecordingSearchField = ['Name', 'Composer__Name', 'UploadUserName', 'UploadUser__username', 'Description']
    UserSearchField = ['username', 'Introduction']
    ComposerSearchField = ['Name', 'Introduction']

    RecordingSearchResults = obtain_result_by_trigram_dist(Recording, RecordingSearchField, keyword)
    UserSearchResults = obtain_result_by_trigram_dist(User, UserSearchField, keyword)
    ComposerSearchResults = obtain_result_by_trigram_dist(Composer, ComposerSearchField, keyword)

    UserSearchResults = UserSearchResults.annotate(NumRecordings=Count('Recordings'))
    ComposerSearchResults = ComposerSearchResults.annotate(NumRecordings=Count('Recordings'))

    MergedResults = list(RecordingSearchResults) + list(UserSearchResults) + list(ComposerSearchResults)
    
    # sort the search results by similarity rank
    MergedResults = sorted(
        MergedResults,
        key=lambda instance: -instance.similarity
    )

    return MergedResults