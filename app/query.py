#!/usr/bin/python
import json
import requests
import Image
import ImageOps
import urllib
import os
from bs4 import BeautifulSoup as Soup
from datetime import datetime
from cStringIO import StringIO
from config import NPR_API_KEY, ABSOLUTE_PATH


def api_feed(tag, numResults=1, char_limit=240, thumbnail=False):
    """Query the NPR API using given tag ID, return dictionary of results.
    Call this function in views.py to get a list of stories for a given tag"""

    stories = query_api(tag, numResults)

    story_list = []
    for story in stories:
        link = story['link'][0]['$text']
        date = convert_date(story['storyDate']['$text'])
        title = story['title']['$text'].strip()
        byline = story['byline'][0]['name']['$text']

        try:
            story_image = story['image'][0]['crop'][0]
            image = story_image['src']
            image = generate_thumbnail(image, preserve_ratio=True, size=(120, 100))
            width = story_image['width']
            height = story_image['height']
            if int(width) > int(height):
                landscape = True
            else:
                landscape = False
        except KeyError:
            image = False  # set equal to url string for default image
            landscape = False

        try:
            audio = {}
            audio_file = story['audio'][0]
            audio['mp3'] = audio_file['format']['mp3'][0]['$text'].split('?')[0]
            audio['duration'] = audio_file['duration']['$text']
        except KeyError:
            audio = False

        full_text = [i['$text'] for i in story['text']['paragraph'] if len(i) > 1]
        # if len(i) > 1 ignores pars w/ no text, i.e. when images or audio

        text = full_text[:1]

        if thumbnail:
            try:
                image_url = story['image'][0]['crop'][0]['src']
                image = generate_thumbnail(image_url, size=(100, 100))
            except KeyError:
                image = False

        story_list.append({
            'title': title,
            'date': date,
            'link': link,
            'image': image,
            'text': text,
            'byline': byline,
            'audio': audio,
            'landscape': landscape
        })

    return story_list


def reporter_list(tag, numResults=50):
    """Queries the API for bylines and returns an ordered list of name, twitter
    and a path to a photo. Reporters ordered by number of stories for tag.
    Call in views.py, returns reporters with more than 1 story and a photo"""

    stories = query_api(tag, numResults)

    name_list = []
    reporters = []
    for story in stories:
        name = story['byline'][0]['name']['$text']
        if name not in name_list:
            name_list.append(name)
            byline = {}
            byline['name'] = name
            try:
                url = story['byline'][0]['link'][0]['$text']
                byline['url'] = reporter_image(url)
                byline['count'] = 1
                reporters.append(byline)
            except KeyError:
                pass
        else:
            for reporter in reporters:
                if reporter['name'] == name:
                    reporter['count'] += 1

    reporters = sorted(reporters, key=lambda k: k['count'], reverse=True)

    with open('app/static/data/twitter.json') as f:
        twitter_dict = json.load(f)

    ranked_list = []
    for reporter in reporters:
        for twitter in twitter_dict['reporters']:
            if reporter['name'] == twitter['name']:
                reporter['handle'] = twitter['handle']
        if reporter['url'] and reporter['count'] > 1:
            ranked_list.append(reporter)

    return ranked_list


def query_api(tag, numResults=10):
    """Hits the NPR API, returns JSON story list"""

    id_string = ','.join([str(s) for s in tag])
    query = ('http://api.npr.org/query?orgid=692' +
        '&fields=title,byline,storyDate,image,text,audio' +
        '&sort=dateDesc' +
        '&action=Or' +
        '&output=JSON' +
        '&numResults=%d' +
        '&id=%s' +
        '&apiKey=%s') % (numResults, id_string, NPR_API_KEY)

    r = requests.get(query)
    j = json.loads(r.text)
    stories = j['list']['story']

    return stories


def reporter_image(url):
    """Takes reporter URL from byline and returns URL to reporter's image"""

    r = requests.get(url)
    page = r.text
    soup = Soup(page)
    person_card = soup.find_all(id="person-card")[0]
    try:
        image = person_card.find_all('img')[0].get('src')
        thumbnail = generate_thumbnail(image, size=(80, 80))
    except IndexError:
        image = False
        thumbnail = False

    return thumbnail


# Convert this to accept a URL OR a directory
def generate_thumbnail(image_url, preserve_ratio=False, size=(220, 165)):
    """Take an image src, generate a thumbnail, return new path"""

    filename = image_url.rsplit('/', 1)[1]
    path_to_read = 'img/thumbnails/' + filename
    path_to_save = ABSOLUTE_PATH + 'static/' + path_to_read

    if not os.path.isfile(path_to_save):
        img_file = urllib.urlopen(image_url)
        img = StringIO(img_file.read())
        image = Image.open(img)
        if preserve_ratio:
            width = image.size[0]
            height = image.size[1]
            new_height = size[0] * height / width
            size = (size[0], new_height)
        im = ImageOps.fit(image, size, Image.ANTIALIAS)
        im.save(path_to_save)

    return path_to_read


def convert_date(timestamp):
    """Converts API timestamp to publication-ready dateline"""

    day = timestamp[5:7]
    month = datetime.strptime(timestamp[8:11], '%b').strftime('%B')
    year = timestamp[12:16]
    date = month + ' ' + day + ", " + year
    return date


def grab_ss(key, sheet='od6'):
    """Grabs a google spreadsheet and turns it into a JSON object"""

    url = ("https://spreadsheets.google.com/feeds/" +
        "list/%s/%s/public/values?alt=json") % (key, sheet)
    r = requests.get(url)
    j = json.loads(r.text)
    json_ss = j['feed'].get('entry', '')

    return json_ss


def drive_to_json(key, field_list, sheet='od6'):
    """Called in views, takes a google drive spreadsheet key and a list of
    fields and returns a list of dictionaries of those fields"""

    rows = grab_ss(key, sheet)
    results = []
    for row in rows:
        result = {}
        for field in field_list:
            result[field] = row['gsx$%s' % (field)]['$t']
        results.append(result)

    return results
