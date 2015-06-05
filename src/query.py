

class QueryType():
    ITEM_ITEM, USER_USER = range(2)


class Query():

    """
        item_idx - item index in matrix
        user_idx - user index in matrix
        query_type - 0 item/item, 1 user/user
        k - maximum number of similar items/users
    """
    def __init__(self, item_idx, user_idx, query_type, k):
        self.item_idx = item_idx
        self.user_idx = user_idx
        self.query_type = query_type
        self.k = k

    def __str__(self):
        return '%d %d %d %d' % (self.item_idx, self.user_idx, self.query_type, self.k)