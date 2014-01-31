from index import app
from flask import render_template, request
from config import BASE_URL
from query import api_feed, drive_to_json


@app.route('/')
def index():
    page_url = BASE_URL + request.path
    page_title = 'Vermonters In Sochi'
    stories = api_feed([262757810], numResults=10)

    field_list = ['name', 'event', 'age', 'home', 'career', 'story',
        'us', 'italy', 'canada']
    athletes = drive_to_json('0AtWnpcGxoF0xdFE4QU56eTZnN0wwNjZ2NDMwN2RoeXc', field_list)

    for i in athletes:
        print i

    social = {
        'title': "",
        'subtitle': "",
        'img': "",
        'description': "",
        'twitter_text': "",
        'twitter_hashtag': ""
    }

    return render_template('content.html',
        page_title=page_title,
        social=social,
        stories=stories,
        athletes=athletes,
        page_url=page_url)
