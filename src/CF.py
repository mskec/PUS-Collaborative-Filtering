import sys
import math
from operator import itemgetter
from decimal import Decimal, ROUND_HALF_UP

from utils import *
from query import Query
from query import QueryType


def read_input_data():
    data = {}
    item_number, user_number = sys.stdin.readline().split()

    # TODO 10 is min value
    checkintvalue(item_number, 3, 100, 'N must be between 10 and 100!')
    checkintvalue(user_number, 5, 100, 'M must be between 10 and 100!')

    data['item_number'] = int(item_number)
    data['user_number'] = int(user_number)

    data['item_user_matrix'] = []
    # data['item_user_matrix'] = [sys.stdin.readline().split() for _ in xrange(data['item_number'])]
    for _ in xrange(data['item_number']):
        line = sys.stdin.readline().split()
        for x in xrange(len(line)):
            line[x] = int(line[x]) if line[x] != 'X' else line[x]       # TODO this can be done with map
        data['item_user_matrix'].append(line)

    query_number = sys.stdin.readline()
    checkintvalue(query_number, 1, 100, 'Q must be between 1 and 100!')

    data['query_number'] = int(query_number)
    data['queries'] = []
    for _ in xrange(data['query_number']):
        query = sys.stdin.readline().split()

        checkintvalue(query[0], 1, data['item_number'])
        checkintvalue(query[1], 1, data['user_number'])
        checkintvalue(query[2], 0, 1, 'Type must be 0 or 1')
        checkintvalue(query[3], 1, min(data['item_number'], data['user_number']))

        if query[2] == 1:
            query[0], query[1] = query[1], query[0]

        query_type = QueryType.ITEM_ITEM if int(query[2]) == 0 else QueryType.USER_USER
        data['queries'].append(Query(int(query[0])-1, int(query[1])-1, query_type, int(query[3])))

    return data


def row_subtract_mean(row):
    tmp_row = filter(lambda x: x != 'X', row)
    mean = sum(tmp_row) / float(len(tmp_row))

    return map(lambda x: x-mean if x != 'X' else 'X', row)


def calc_rating(query, matrix, matrix_avg):
    static_row = matrix_avg[query.item_idx]

    similarities = []
    for x in xrange(len(matrix_avg)):
        if x != query.item_idx:
            sim = calc_cosine_similarity(static_row, matrix_avg[x])
            if sim >= 0:
                similarities.append((x, sim))

    similarities = sorted(similarities, key=itemgetter(1), reverse=True)

    first_k_similarities = similarities[: (query.k if query.k <= len(similarities) else len(similarities))]

    sum_sim = sum([pair[1] for pair in first_k_similarities])
    rating_sim = 0.0
    for sim in first_k_similarities:
        if matrix[sim[0]][query.user_idx] != 'X':
            rating_sim += (matrix[sim[0]][query.user_idx] * sim[1])

    return rating_sim / sum_sim


def calc_cosine_similarity(rx, ry):
    # sim = rx * ry / (||rx|| * ||ry||)

    def reduce_abs(x, y):
        real_y = y if y != 'X' else 0
        return x + (real_y*real_y)

    rx_abs = math.sqrt(reduce(reduce_abs, rx, 0))
    ry_abs = math.sqrt(reduce(reduce_abs, ry, 0))

    # TODO zip + reduce
    dot_product = 0
    for i in xrange(len(rx)):
        if rx[i] != 'X' and ry[i] != 'X':
            dot_product += rx[i] * ry[i]

    return dot_product / (rx_abs * ry_abs)


def format_rating(rating):
    return Decimal(Decimal(rating).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))


def main():
    data = read_input_data()

    item_item_matrix = data['item_user_matrix']
    item_item_matrix_avg = map(row_subtract_mean, item_item_matrix)

    user_user_matrix = zip(*item_item_matrix)       # Transposing matrix
    user_user_matrix_avg = map(row_subtract_mean, user_user_matrix)

    # Compute every query
    for query in data['queries']:
        rating = 0.0

        if QueryType.ITEM_ITEM == query.query_type:
            rating = calc_rating(query, item_item_matrix, item_item_matrix_avg)

        elif QueryType.USER_USER == query.query_type:
            rating = calc_rating(query, user_user_matrix, user_user_matrix_avg)

        print format_rating(rating)

if __name__ == '__main__':
    main()