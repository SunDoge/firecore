import firecore
import functools

FIRECORE_LIBSONNET = 'jsonnet/firecore.libsonnet'


# def test_eval_snippet():
#     snippet = "{a:1, b:2}"
#     expected = dict(a=1, b=2)
#     output = firecore.config.from_snippet(snippet)
#     assert output == expected


# def test_linked_list():
#     import_firecore = "local lib = import '{}';".format(FIRECORE_LIBSONNET)
#     main = """
#     lib.linkedList({
#         c: {name: 'c', next:: null},
#         a: {name: 'a', next:: 'b'},
#         b: {name: 'b', next:: 'c'},
#     })
#     """
#     output = firecore.config.from_snippet(import_firecore + main, jpathdir='.')
#     assert len(output) == 3
#     for index, name in enumerate(['a', 'b', 'c']):
#         assert output[index]['name'] == name
