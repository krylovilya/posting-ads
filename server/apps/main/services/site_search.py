from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import QuerySet

from apps.main.models import Ad


def site_search_for_ads(search_request: str) -> QuerySet[Ad]:
    """Поиск объявлений."""
    vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
    query = SearchQuery(search_request)
    return Ad.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
