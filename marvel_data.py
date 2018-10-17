import requests as rq
import re

def get_marvel_characters():
    """
    Constructs the Superhero, Supervillain, and Ambiguous characters and stores them into a set

    input:
        none
    output:
        three sets: superheroes, supervillains, ambiguous respectively.
    """

    a_set = set()

    for faction in ["superheroes, supervillains"]:
        # WikiPedia page containing the list of marvel superheroes or supervillains
        data = rq.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Marvel_Comics_%s" % character_type).json()

        cont = data['continue']['cmcontinue']  # initial continue key to progress through the pages


        for entry in data['query']['categorymembers']:
            a_set.add((entry['title']).encode('utf-8'))
        while True:
            try:
                data = rq.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Marvel_Comics_%s&cmcontinue=%s" % (character_type, cont)).json()
                cont = data['continue']['cmcontinue']

                for entry in data['query']['categorymembers']:
                    a_set.add(entry['title'].encode('utf-8'))
            except KeyError:  # When there is a KeyError, then there are no more pages to continue through
                f.close()
                break




def get_content_page_characters(character_list, location):
    """
    Gets the content page of the characters in a list (that is not in  ambiguous).
    Uses two functions that 1) verifies if the name is a valid file name. 2) requests the markup page of one character
    Stores it into a .txt file into location specified. The directory must exist before calling.

    inputs:
        a_list: any iterable data type. In this case, it is a set of the superhero names.
        location: directory or path where to store the .txt file
    """


    def verify_fname(string):
        # TODO: Add more invalid chars
        if string.find(r'"') != -1:
            return string.replace(r'"', " ",2) + " (Unicode conflict)"
        else:
            return string


    def get_contents(character):
        query = r'https://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content' % character
        datum = rq.get(query).json()
        #EDITED
        return datum['query']['pages'].values()[0]['revisions'][0]['*']


    for item in character_list:
        item = item.decode('utf-8')
        print("Getting character content for %s" % item)
        fname = verify_fname(item).encode('utf-8')

        # if item not in ambiguous:
        #     path = "%s/%s.txt" % (location, fname)
        # else:
        #     path = "Characters/Ambiguous/%s.txt" % fname
        # with open(path, 'w') as f:
        #     f.write((get_contents(item)).encode('utf-8'))
    f.close()

def get_page_size(character):
    link = "https://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=size" % character
    data = rq.get(link).json()
    return data['query']['pages'].values()[0]['revisions'][0]['size']
