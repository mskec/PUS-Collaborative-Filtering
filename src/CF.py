# coding=utf-8
import sys
import math
from operator import itemgetter
from decimal import Decimal, ROUND_HALF_UP


from utils import *


class QueryType():
    ITEM_ITEM, USER_USER = range(2)


def read_input_data():
    data = {}
    item_number, user_number = sys.stdin.readline().split()

    # TODO 10 is min value
    checkintvalue(item_number, 5, 100, 'N must be between 10 and 100!')
    checkintvalue(user_number, 5, 100, 'M must be between 10 and 100!')

    data['item_number'] = int(item_number)
    data['user_number'] = int(user_number)

    convert_to_int = lambda c: int(c) if c != 'X' else c
    data['item_user_matrix'] = [map(convert_to_int, sys.stdin.readline().split()) for _ in xrange(data['item_number'])]

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

        if query[2] == '1':
            query[0], query[1] = query[1], query[0]

        query_type = QueryType.ITEM_ITEM if query[2] == '0' else QueryType.USER_USER

        data['queries'].append(
            {'item_idx': int(query[0])-1, 'user_idx': int(query[1])-1, 'query_type': query_type, 'k': int(query[3])}
        )

    return data


def row_subtract_mean(row):
    tmp_row = filter(lambda x: x != 'X', row)
    mean = sum(tmp_row) / float(len(tmp_row))

    return map(lambda x: x-mean if x != 'X' else 'X', row)


def calc_rating(query, matrix, matrix_avg):
    static_row = matrix_avg[query['item_idx']]

    similarities = []   # List of tuples (matrix_item_idx, similarity)

    for x in xrange(len(matrix_avg)):
        if x != query['item_idx'] and matrix[x][query['user_idx']] != 'X':
            sim = calc_cosine_similarity(static_row, matrix_avg[x])
            if sim >= 0:
                similarities.append((x, sim))

    similarities = sorted(similarities, key=itemgetter(1), reverse=True)

    first_k_similarities = similarities[: (query['k'] if query['k'] <= len(similarities) else len(similarities))]

    sum_sim = sum([pair[1] for pair in first_k_similarities])
    rating_sim = 0.0
    for sim in first_k_similarities:
        rating_sim += (matrix[sim[0]][query['user_idx']] * sim[1])

    return rating_sim / sum_sim


# sim = rx • ry / (||rx|| * ||ry||)
def calc_cosine_similarity(rx, ry):
    rx_norm = math.sqrt(reduce((lambda x, y: x + math.pow(y if y != 'X' else 0, 2)), rx, 0))
    ry_norm = math.sqrt(reduce((lambda x, y: x + math.pow(y if y != 'X' else 0, 2)), ry, 0))
    dot_product = reduce((lambda x, y: x + (y[0] * y[1] if y[0] != 'X' and y[1] != 'X' else 0)), zip(rx, ry), 0)

    return dot_product / (rx_norm * ry_norm)


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

        if QueryType.ITEM_ITEM == query['query_type']:
            rating = calc_rating(query, item_item_matrix, item_item_matrix_avg)

        elif QueryType.USER_USER == query['query_type']:
            rating = calc_rating(query, user_user_matrix, user_user_matrix_avg)

        print format_rating(rating)

if __name__ == '__main__':
    main()
