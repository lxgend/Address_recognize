# coding=utf-8
import os
import pandas as pd
from whoosh import index, qparser
from whoosh.fields import Schema, TEXT

# import data into pandas df and create index schema

grimm = pd.read_csv("~/grimm.csv")
schema = Schema(title=TEXT(stored=True, field_boost=2.0),
                text=TEXT)


# create and populate index
def populate_index(dirname, dataframe, schema):
    # Checks for existing index path and creates one if not present
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    print("Creating the Index")
    ix = index.create_in(dirname, schema)

    with ix.writer() as writer:
        # Imports stories from pandas df
        print("Populating the Index")
        for i in dataframe.index:
            add_stories(i, dataframe, writer)

def add_stories(i, dataframe, writer):
    writer.update_document(title=str(dataframe.loc[i, "story"]),
                           text=str(dataframe.loc[i, "text"]))




# creates index searcher
def index_search(dirname, search_fields, search_query):
    ix = index.open_dir(dirname)
    schema = ix.schema
    # Create query parser that looks through designated fields in index
    og = qparser.OrGroup.factory(0.9)
    mp = qparser.MultifieldParser(search_fields, schema, group=og)

    # This is the user query
    q = mp.parse(search_query)

    # Actual searcher, prints top 10 hits
    with ix.searcher() as s:
        results = s.search(q, limit=10)
        print("Search Results: ")
        print(results[0:10])

if __name__ == '__main__':
    populate_index("Grimm_Index", grimm, schema)
    index_search("Grimm_Index", ['title', 'text'], u"evil witch")
