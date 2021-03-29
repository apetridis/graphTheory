import wikipedia, networkx as nx
import sys
from bs4 import BeautifulSoup
import re
import random
#for my recurcive function tobe able to run 1m times.
sys.setrecursionlimit(1000000)


startingKey = input("Enter starting key: ")
print(startingKey)
path = input("Enter path for .gefx file: e.g C:/Users/Αλέξανδρος Πετρίδης/Desktop/gephi/social_graph.gexf: ")
print("In the same file pagerank_"+startingKey+".txt will be created")


def correlation(page):
    html = BeautifulSoup(page.html(), features="html.parser")
    endlist = []
    if html.find(id="See_also") != None :
        try:
            mylist = html.find(id="See_also").find_next("ul").find_all("a")
            #checking if we have the correct see also section
            for i in range(len(mylist)):
                try:
                    if re.search("Portal:.+", mylist[i].get("title")):
                        mylist = html.find(id="See_also").find_next("ul").find_next("ul").find_all("a")
                        break
                except TypeError:
                    print("TypeError")
        except AttributeError:
            print("This page html cannot be parsed")
            # endlist = []
            return []

        for i in range(len(mylist)):
            endlist.append(mylist[i].get("title"))
    else:
        print("There is no See also section so '", page.title , "' will have no children.")
    return endlist

def wiki(title):
    try:
        page = wikipedia.WikipediaPage(title)
    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.WikipediaPage(e.options[0])
    except KeyError:
        print(KeyError)
        return 0;
    return page

G = nx.Graph()

def createchilds(parent):
    if nx.number_of_nodes(G) < 500: #last child will go into when we have 500 nodes
        childs = correlation(parent)
        for x in range(len(childs)):
            if not G.has_node(childs[x]):
                G.add_node(childs[x])
                print("Node '", childs[x], "' added.")
                G.add_edge(parent.title, childs[x])
                newparent = wiki(wikipedia.search(childs[x], results=1))
                if newparent == 0:
                    break;
                try:
                    createchilds(newparent)
                except wikipedia.exceptions.WikipediaException as e:
                    print(e)
            else:
                G.add_edge(parent.title, childs[x])


first_parent = wiki(wikipedia.search(startingKey, results=1))
G.add_node(first_parent.title)
print("Node '", first_parent.title, "' added.")
createchilds(first_parent)


f = open("C:/Users/Αλέξανδρος Πετρίδης/Desktop/gephi/pagerank_"+startingKey+".txt", "w+", encoding="utf-8")
pr = nx.pagerank(G)
list_of_pr = [f'{key} : {pr[key]}' for key in pr]
[f.write(f'{st}\n') for st in list_of_pr]


print(nx.info(G))
density = nx.density(G)
print("Network density:", density)
triadic_closure = nx.transitivity(G)
print("Triadic closure:", triadic_closure)


nx.draw(G, with_labels=True)
nx.write_gexf(G, path)