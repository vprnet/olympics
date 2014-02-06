from index import app
from flask import render_template, request
from config import BASE_URL, ABSOLUTE_PATH
from query import api_feed, drive_to_json, generate_thumbnail


@app.route('/')
def index():
    page_url = BASE_URL + request.path
    page_title = 'Vermonters In Sochi'
    stories = api_feed([262757810], numResults=10)

    field_list = ['name', 'event', 'age', 'home', 'career', 'story',
        'us', 'italy', 'canada', 'credit', 'result2014']
    athletes = drive_to_json('0AtWnpcGxoF0xdFE4QU56eTZnN0wwNjZ2NDMwN2RoeXc', field_list)
    results = drive_to_json('0AtWnpcGxoF0xdFE4QU56eTZnN0wwNjZ2NDMwN2RoeXc',
        ['name', 'event', 'medal'],
        sheet='od5')

    sports = drive_to_json('0AtWnpcGxoF0xdFE4QU56eTZnN0wwNjZ2NDMwN2RoeXc',
        ['name', 'event1', 'vermonter1', 'event2', 'vermonter2', 'event3', 'vermonter3', 'event4', 'vermonter4'],
        sheet='od4')
    for sport in sports:
        sport['events'] = [sport['event1'],
            sport['event2'],
            sport['event3'],
            sport['event4']]
        sport['vermonters'] = [sport['vermonter1'],
            sport['vermonter2'],
            sport['vermonter3'],
            sport['vermonter4']]

    photos = drive_to_json('0AtWnpcGxoF0xdFE4QU56eTZnN0wwNjZ2NDMwN2RoeXc',
        ['url', 'caption', 'credit'],
        sheet='od7')
    photos[0]['url'] = generate_thumbnail(ABSOLUTE_PATH + photos[0]['url'],
        preserve_ratio=True, size=(2000, 1000))
    photos[1]['url'] = generate_thumbnail(ABSOLUTE_PATH + photos[1]['url'],
        size=(375, 250))
    photos[2]['url'] = generate_thumbnail(ABSOLUTE_PATH + photos[2]['url'],
        size=(375, 250))
    updated = drive_to_json('0AtWnpcGxoF0xdFE4QU56eTZnN0wwNjZ2NDMwN2RoeXc',
        ['updated'],
        sheet='oda')

    for athlete in athletes:
        athlete['image'] = "%s.jpg" % (athlete['name'].title().replace(' ', '-'))

    social = {
        'title': "Vermonters in Sochi",
        'subtitle': "VPR's Coverage Of The 2014 Olympics",
        'img': photos[0]['url'],
        'description': "Follow Kelly Clark, Hannah Kearney and other Vermont Olympians as they compete in Russia.",
        'twitter_text': "Olympics 2014: Vermonters in Sochi",
        'twitter_hashtag': "Olympics,VT,Sochi2014"
    }

    return render_template('content.html',
        page_title=page_title,
        social=social,
        stories=stories,
        athletes=athletes,
        results=results,
        sports=sports,
        photos=photos,
        updated=updated,
        page_url=page_url)
