#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    Daty: wikidata library
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from bleach import clean
from bs4 import BeautifulSoup
from copy import deepcopy as copy
from os import mkdir
from os.path import exists, join, getmtime
from pprint import pprint
from re import sub
from requests import get
from time import time

from .config import Config
config = Config()

from .util import load, save

class Wikidata:
    def __init__(self, verbose=False):
        self.config = Config()
        self.verbose = verbose
        self.vars = []

    def select(self, var, statements, keep_data=False):
        """Return (select) the set of var that satisfy the statements.

        Args:
            var (dict): its keys can be 'URI' and 'Label';
            statements (list): of double dictionaries of the form:
                role ('s','p','o')
                  var

        Returns:
            (list) of results URI, or query sparql response if "keep_data" is True.
        """
        from pywikibot.data.sparql import SparqlQuery
        # We will transform them
        var = copy(var)
        statements = copy(statements)

        # Template
        template = """SELECT var WHERE {
          statements
        }
        """

        # Check that var is in the statements
        if not var in (var for s in statements for role,var in s.items()):
            print("WARNING: var not contained in constraints!")
            return []

        # Convert var and statements vars to SPARQL
        var = "?" + var["Label"]

        print("Select: statements")
        for s in statements:
            pprint(s)
            for role in s:
                print("Role")
                pprint(role)
                x = s[role]
                if not "URI" in x.keys() or x["URI"] == "":
                    s[role] = "?" + x["Label"]
                elif x["URI"].startswith("Q"):
                    s[role] = "wd:" + x["URI"]
                elif x["URI"].startswith("P"):
                    s[role] = "wdt:" + x["URI"]
                pprint(s[role])

        print("Select: Form the SPARQL statements")
        expr = ""
        for s in statements:
            print("s", s['s'])
            print("p", s['p'])
            print('o', s['o'])
            expr = "".join([expr, s['s'], " ", s['p'], " ", s['o'], ".\n"])
            print(expr)

        # Do the query
        query = sub('statements', expr, template)
        query = sub('var', var, query)

        #print(expr)
        print(query)
        sparql = SparqlQuery()

        # Return results
        if keep_data:
            return sparql.query(query)
        results = sparql.query(query)['results']['bindings']
        results = list(set([r[var[1:]]['value'].split("/")[-1] for r in results]))
        return results 

    def download(self, URI, use_cache=True, target=None):
        """

        Args:
            id (str): LQP id;
            use_cache (bool): whether to use cache;
        Returns:
            (dict) the downloaded entity as a dict
        """
        while True:
            try:
                from pywikibot import ItemPage, PropertyPage, Site
                site = Site('wikidata', 'wikidata')
                repo = site.data_repository()
                if target:
                    path = join(self.config.dirs['cache'], URI + 'target')
                else:
                    path = join(self.config.dirs['cache'], URI)
                if exists(path):
                    mtime = getmtime(path)
                    if (use_cache or time() - mtime < 604800):
                        try:
                            entity = load(path)
                            break
                        except AttributeError as e:
                            pass
                else:
                    print("light-downloading" if target else "dowloading", URI)
                    if URI.startswith("P"):
                        entity = PropertyPage(repo, URI).get()
                    elif URI.startswith("Q") or URI.startswith("L"):
                        entity = ItemPage(repo, URI).get()
                    else:
                        print("Not supported")
                        entity = {}
                    if target:
                        output = {}
                        for t in target:
                            if t == "Label":
                                output["Label"] = self.get_label(entity)
                            if t == "Description":
                                output["Description"] = self.get_description(entity)
                            if t == "Data":
                                output["Data"] = entity
                        entity = output
                    save(entity, path)
                    break
            except Exception as e:
                from pywikibot.exceptions import EntityTypeUnknownException
                if 'Page [[wikidata:' in str(e):
                    print(e)
                    entity = {}
                    break
                else:
                    if type(e) == EntityTypeUnknownException:
                        print(URI, "pywikibot meaningful error")
                    else:
                        print(URI)
                        raise e
        entity["URI"] = URI
        return entity

    def get_label(self, entity, language='en'):
        """Get entity label

        Args:
            entity (dict): output of <entity>Page.get;
            language (str): language of the label to be selected (default 'en')
        """
        if not entity:
            return "No available label"
        try:
            if language in entity['labels']:
                return entity['labels'][language]
            else:
                return "Select a secondary language"
        except Exception as e:
            raise e

    def get_description(self, entity, language='en'):
        if not entity:
            return "No available description in selected language"
        try:
            if language in entity['descriptions']:
                return entity['descriptions'][language]
            else:
                return "Select a secondary language"
        except Exception as e:
            print(entity)
            raise e

    def entity_search(self, query, entity):
        """

        """
        pass

    def search(self, query, verbose=False):
        """
        
        Args:
            query (str): what to search
        Returns:
            ({"URI":, "Label":, "Description":} in results)
        """
        pattern = 'https://www.wikidata.org/w/index.php?limit=20&search='
        page = get(pattern + query, timeout=10).content
        soup = BeautifulSoup(page, 'html.parser')
        results = []
        try:
            results = soup.find(name='ul', attrs={'class':'mw-search-results'})
            results = results.find_all(name='li', attrs={'class':'mw-search-result'})
            results = ({"URI":r.find(name="span", attrs={'class':'wb-itemlink-id'}).text.split("(")[1].split(")")[0],
                        "Label":clean(r.find(name="span", attrs={'class':'wb-itemlink-label'}).text),
                        "Description":clean(r.find(name='span', attrs={'class':'wb-itemlink-description'}).text)} for r in results)
        except Exception as e:
            results = []
            #if verbose:
            #    print(e)
        if self.verbose:
            pprint(results)
        return results
