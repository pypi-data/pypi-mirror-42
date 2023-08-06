import numpy as np
import heapq as hq
from collections import defaultdict
import numbers
import psutil
import operator as op
from functools import reduce
from math import floor, ceil


def pearsoncc(x, y):
    """ Compute Pearson Correlation Coefficient. """
    x = (x - x.mean(0)) / x.std(0)
    y = (y - y.mean(0)) / y.std(0)
    return (x * y).mean()


def le(x, y):
    return x - y


def ge(x, y):
    return y - x


def logb(x, b):
    """
    :type x: float
    :param x: number to transform

    :type b: float
    :param b: base to transform

    transform natural log to log base b
    """
    return np.log(x) / np.log(b)


def humanize_bytesize(size: int):
    """
    transforms an integer to a human readeable.
    1024 -> 1.0 KB
    """
    if size == 0:
        return '0B'
    size_name = ('B', "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(np.floor(logb(size, 1024)))
    p = np.power(1024, i)
    s = round(size / float(p), 2)
    return '{} {}'.format(s, size_name[i])


def expand_matrix_row(matrix, max_size, actual_size):
    """
    :type matrix: ndarray
    :param matrix: NxM matrix

    :type max_size: int
    :param max_size: max size of new rows to add

    :type actual_size: int
    :param actual_size: number of rows to ignore

    add rows with zeros to the end of the matrix
    """
    return np.append(matrix,
                     np.zeros((max_size - actual_size, matrix.shape[1]), dtype=matrix.dtype), axis=0)


def expand_matrix_col(matrix, max_size, actual_size):
    """
    add columns of zeros to the right of the matrix
    """
    return np.append(matrix,
                     np.zeros((matrix.shape[0], max_size - actual_size), dtype=matrix.dtype), axis=1)


def expand_rows_cols(x, n_rows=2, n_cols=2):
    if len(x.shape) == 2:
        x = np.hstack((x, np.zeros((x.shape[0], n_cols))))
        x = np.vstack((x, np.zeros((n_rows, x.shape[1]))))
    return x


def is_binary(array, include_null=True):
    if include_null is False:
        return np.count_nonzero((array != 0) & (array != 1)) == 0
    else:
        return np.all((array == 0) | (array == 1) | (np.isnan(array)))


def is_integer(array):
    mask = np.isnan(array)
    if any(mask):
        return all(np.equal(np.mod(array[~mask], 1), 0))
    else:
        return all(np.equal(np.mod(array, 1), 0))


def is_integer_if(array, card_size=4):
    return is_integer(array) and np.unique(array).size >= card_size


def index_if_type_row(array, fn, **params):
    return [i for i, row in enumerate(array) if fn(row, **params)]


def index_if_type_col(array, fn, **params):
    return [i for i, col in enumerate(array.T) if fn(col, **params)]


def unique_size(array):
    mask = np.isnan(array)
    array[mask] = -1
    return np.unique(array).size


def features2rows(data):
    """
    :type data: ndarray

    transforms a matrix of dim (n, m) to a matrix of dim (n*m, 2) where
    each row has the form [feature_column, feature_data]
    e.g
    [['a', 'b'], ['c', 'd'], ['e', 'f']] => [[0, 'a'], [0, 'c'], [0, 'e'], [1, 'b'], [1, 'd'], [1, 'f']]
    """
    ndata = np.empty((data.shape[0] * data.shape[1], 2), dtype=data.dtype)
    index = 0
    for ci, column in enumerate(data.T):
        for value in column:
            ndata[index] = np.asarray([ci, value])
            index += 1 
    return ndata


def missing(column):
    return (np.count_nonzero(np.isnan(column)) / float(column.size)) * 100


def zeros(column):
    return ((column.size - np.count_nonzero(column)) / float(column.size)) * 100


def features_fmtype(fmtypes, fmtype):
    map_col = defaultdict(list)
    for ci, c_fmtype in enumerate(fmtypes):
        map_col[c_fmtype].append(ci)
    return map_col[fmtype.id]


def swap_noise(x, y, p=.15, cols=1):
    indexes_o = [int(round(i, 0)) for i in np.random.uniform(0, x.size-1, size=int(round(x.size * p, 0)))]
    indexes_d = [int(round(i, 0)) for i in np.random.uniform(0, x.size-1, size=int(round(x.size * p, 0)))]

    matrix = np.c_[x, y]
    vo = matrix[indexes_o, cols]
    vd = matrix[indexes_d, cols]
    for s0, s1, nv0, nv1 in zip(indexes_o, indexes_d, vo, vd):
        matrix[s1, cols] = nv0
        matrix[s0, cols] = nv1
    return matrix


def max_type(items: list):
    sizeof = [np.dtype(type(e)).num for e in items]
    types = [type(e) for e in items]
    if len(sizeof) == 0:
        return None
    v = max(zip(sizeof, types), key=lambda x: x[0])
    return v[1]


def max_dtype(dtypes: np.dtype) -> np.dtype:
    if dtypes is not None:
        sizeof_dtype = [(dtype, dtype.num) for _, (dtype, _) in dtypes.fields.items()]
        if len(sizeof_dtype) > 0:
            return max(sizeof_dtype, key=lambda x: x[1])[0]


def filter_sample(stream, label, col_index):
    if col_index is None:
        for e in stream:
            if e == label:
                yield e
    else:
        for row in stream:
            if row[col_index] == label:
                yield row


def num_splits(length: int, batch_size: int) -> int:
    if isinstance(length, float) or batch_size is None:
        return 0
    elif 0 < batch_size <= length:
        if length % batch_size > 0:
            r = 1
        else:
            r = 0
        return int((length / batch_size) + r)
    else:
        return 1


def wsr(stream, k):
    heap = []

    def hkey(w):
        return -np.random.exponential(1./w)

    for item, weight in stream:
        if len(heap) < k:
            hq.heappush(heap, (hkey(weight), item))
        elif hkey(weight) > heap[0][0]:
            hq.heapreplace(heap, (hkey(weight), item))

    while len(heap) > 0:
        yield hq.heappop(heap)[1]


def wsrj(stream, k):
    reservoir = []

    def hkey(w):
        return np.random.exponential(1./w)

    for item, weight in stream:
        if len(reservoir) < k:
            hq.heappush(reservoir, (hkey(weight), item))
        else:
            break

    if len(reservoir) == 0:
        return

    while True:
        t_w = reservoir[0][0]
        r = np.random.uniform(0, 1)
        x_w = np.log(r) / np.log(t_w)
        w_c = 0
        for item, weight in stream:
            if 0 < x_w - w_c <= weight:
                r2 = np.random.uniform(t_w, 1)
                k_i = r2**(1./weight)
                hq.heapreplace(reservoir, (k_i, item))                
                break
            w_c += weight
        
        if all(False for _ in stream):
            break

    while len(reservoir) > 0:
        yield hq.heappop(reservoir)[1]


def nested_shape(chunk, dtypes):
    shapes = {}
    if len(chunk) == len(dtypes):
        for group, value in zip(dtypes.names, chunk):
            shapes[group] = nested_shape_aux(value)
    else:
        if len(dtypes) == 1:
            shapes[dtypes.names[0]] = nested_shape_aux(chunk)
        else:
            raise Exception("Not defined shape")
    return shapes


def nested_shape_aux(x) -> list:
    if hasattr(x, 'shape'):
        return list(x.shape)
    elif isinstance(x, tuple) or isinstance(x, list):
        dim = [len(x)]
        shapes = []
        for e in x:
            shapes.append(nested_shape_aux(e))
        for ant, p in zip(shapes, shapes[1:]):
            if ant != p:
                raise Exception("Not defined shape: {}".format(shapes))
        if len(shapes) > 0:
            dim.extend(shapes[0])
        return dim
    elif isinstance(x, numbers.Number) or isinstance(x, str):
        return []


def calc_chunks(shape, dtypes, memory_allowed=1, adj_factor=0.095):
    free_memory = psutil.virtual_memory().free / len(shape.groups())
    chunks = {}
    for group, (dtype, _) in dtypes.fields.items():
        presition = dtype.num if dtype.num > 0 else 1
        chunksize_val = floor(((memory_allowed * free_memory) / presition) * adj_factor)
        used_total_size = reduce(op.mul, [dtype.num] + list(shape[group]))
        if used_total_size < chunksize_val:
            chunks[group] = shape[group]
        else:
            factor = chunksize_val / used_total_size
            chunks[group] = tuple([ceil(val*factor) for val in shape[group]])
    return chunks
