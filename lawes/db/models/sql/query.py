
class Query(object):
    """
    A single SQL query.
    """
    def __init__(self, model):
        self.model = model
        self.q_object = None                        # lawes.db.models import Q
        self.order_by_query = ()                    # using for Model.objects.order_by(filter_query)
        self.skip = None                            # using for Model.objects.skip(skip)#
        self.limit = None                           # using for Model.objects.limit(limit)#

    def add_q(self, q_object):
        """
        :param q_object: lawes.db.models import Q
        :return:
        """
        if not self.q_object:
            self.q_object = q_object
        else:
            self.q_object = self.q_object & q_object

    def filter_comparsion(self, query):
        """ if found __gt, __gte, __lt, __lte, __ne in query, change to "$gt", "$gte", "$lt", "$lte", "$ne"
        >>> query = {"1__gt": 1,"2__gte": 2,"3__lt": 3,"4__lte": 4,"5__ne": 5, '6': 6, '7_text__search': '77' }
        >>> Query(None).filter_comparsion(query=query)
        {'1': {'$gt': 1}, '2': {'$gte': 2}, '3': {'$lt': 3}, '4': {'$lte': 4}, '5': {'$ne': 5}, '6': 6, '7': {'$regex': '7.*7', '$options': 'si'}}
        """
        c_query = {}
        match_tuple = ( '__gt', '__gte', '__lt', '__lte', '__ne', )
        for qkey in query:
            origin = True
            for match_key in match_tuple:
                if qkey.endswith(match_key):
                    match_key_to = match_key.replace('__', '$')
                    startpart, endpart = qkey.split(match_key)
                    c_query[startpart] = { match_key_to: query[qkey] }
                    origin = False
            if qkey.endswith('_text__search'):
                startpart, endpart = qkey.split('_text__search')
                if not isinstance(query[qkey], str):
                    raise TypeError('Can not _text__search with %s, only string' % ( type(query[qkey] ) ) )
                c_query[startpart] = {'$regex': '.*'.join(query[qkey]), '$options': 'si'}
                origin = False
            if origin is True:
                c_query[qkey] = query[qkey]
        return c_query

    def _as_sql(self, q_object):
        """
        >>> from lawes.db.models import Q
        >>> query = Q(name='lawes')
        >>> obj = Query(None)
        >>> obj._as_sql(q_object=query)
        {'name': 'lawes'}
        >>> query = query & Q(sex=1)
        >>> obj._as_sql(q_object=query)
        {'$and': [{'name': 'lawes'}, {'sex': 1}]}
        >>> query_other = Q(address='lawes street1') | Q(age__gt=2)
        >>> obj._as_sql(q_object=query_other)
        {'$or': [{'address': 'lawes street1'}, {'age': {'$gt': 2}}]}
        >>> obj._as_sql(q_object=query & query_other)
        {'$and': [{'$and': [{'name': 'lawes'}, {'sex': 1}]}, {'$or': [{'address': 'lawes street1'}, {'age': {'$gt': 2}}]}]}
        """
        filter_query = {}
        if q_object.q_right is None and q_object.q_left is None:
            if q_object.values:
                filter_query = self.filter_comparsion(dict(q_object.values))
        else:
            filter_query[q_object.connector] = [self._as_sql(q_object.q_left), self._as_sql(q_object.q_right) ]
        return filter_query

    def as_sql(self):
        filter_query = self._as_sql(self.q_object)
        return filter_query

    def execute_sql(self, collection):
        filter_query = self.as_sql()
        multi_data = collection.find(filter_query)
        # order by query
        if self.order_by_query:
            multi_data = multi_data.sort(*self.order_by_query)
        if not self.skip is None:
            multi_data = multi_data.skip(self.skip)
        if not self.limit is None:
            multi_data = multi_data.limit(self.limit)
        return multi_data