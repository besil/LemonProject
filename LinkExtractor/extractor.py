__author__ = 'besil'

from pprint import pprint

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es = Elasticsearch()

    # es.search(index="text_data", fields=["_id", "score"], size=limit, body=equery)

    query = {"query": {"match_all": {}}}

    res = es.search(index="text_data", body=query)

    pprint(res)
    print("Got {} hits".format(res['hits']['total']))

    # for hit in res['hits']['hits'][:2]:
    #     pprint(hit["_source"])
