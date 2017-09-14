# -*- coding: utf-8 -*-

import http.client
import urllib.parse
from flask import Flask, render_template

app = Flask(__name__)

info = {
    'name' : 'プライムビデオ閲覧期限まとめ',
    'url' : 'http://prime-video.mktia.com',
    'desc' : 'あの映画の閲覧期間はいつまで？もうすぐプライム会員特典で見られなくなるプライムビデオを一覧にまとめました。',
    'short_desc' : 'もうすぐ見られなくなるプライムビデオまとめ',
    }

base_url = 'www.amazon.co.jp'
connect = http.client.HTTPSConnection(base_url)


is_finish = False

def make_list(word):
    # Lists to save
    list = {}
    title_list = []
    url_list = []

    page = 1
    keyword = urllib.parse.quote(word)
    while(True):
        query = '/s?rh=k%3A' + keyword + '%2Cn%3A4217521051%2Cp_n_format_browse-bin%3A2792332051&keyword=' + keyword + '&ie=UTF8&page=' + str(page)

        connect.request('GET', query)

        response = connect.getresponse()
        byte_source = response.read()

        # Convert byte to UTF8 string
        source = byte_source.decode('utf-8')

        # delete source not using
        source = source[137000:237000]

        # Save a position
        start_position = 0
        end_position = 0

        # tags to find a title, url
        title_start_tag = 'noopener" title="'
        title_end_tag = '" h'
        url_start_tag = 'href="'
        url_end_tag = '">'
        
        if source.find(title_start_tag) == -1:
            # This page doesn't have the list
            break
        
        while(True):
            start_position = source.find(title_start_tag) + 17
            if start_position == 16:
                # When not find the tag
                break
            else:
                source = source[start_position:]
                end_position = source.find(title_end_tag)
                title = source[:end_position]
                
                start_position = source.find(url_start_tag) + 6
                source = source[start_position:]
                end_position = source.find(url_end_tag)
                url = source[:end_position]

                title_list.append(title)
                url_list.append(url)
                
        page += 1

    list['num'] = len(title_list)
    list['titles'] = title_list
    list['urls'] = url_list
    
    return list

    
@app.route('/')
def top_page():
    return render_template('index.html', info=info)
    
@app.route('/foreign')
def make_foreign_list():
    foreign_list = make_list('外国映画')
    return render_template('result.html', category='洋画', list=foreign_list, info=info)

@app.route('/japanese')
def make_japanese_list():
    japanese_list = make_list('日本映画')
    return render_template('result.html', category='邦画', list=japanese_list, info=info)

@app.route('/anime')
def make_anime_list():
    anime_list = make_list('アニメ')
    return render_template('result.html', category='アニメ', list=anime_list, info=info)
    
# Not use
@app.route('/kids-and-family')
def make_kids_list():
    kids_list = make_list('キッズ')
    return render_template('result.html', category='キッズ・ファミリー', list=kids_list, info=info)
    
@app.route('/music')
def make_music_list():
    music_list = make_list('ミュージック')
    return render_template('result.html', category='音楽', list=music_list, info=info)
    
@app.route('/tv-drama')
def make_drama_list():
    drama_list = make_list('テレビドラマ')
    return render_template('result.html', category='TV ドラマ', list=drama_list, info=info)
    
@app.route('/documentary')
def make_doc_list():
    doc_list = make_list('ドキュメンタリー')
    return render_template('result.html', category='ドキュメンタリー', list=doc_list, info=info)
    
@app.route('/tv-show')
def make_tv_list():
    tv_list = make_list('バラエティ')
    return render_template('result.html', category='バラエティ', list=tv_list, info=info)
    
@app.route('/hobby')
def make_hobby_list():
    hobby_list = make_list('ホビー')
    return render_template('result.html', category='趣味・実用', list=hobby_list, info=info)
    
# Not use
@app.route('/idol')
def make_idol_list():
    idol_list = make_list('アイドル')
    return render_template('result.html', category='アイドル', list=idol_list, info=info)
    
# Not use
@app.route('/sexy')
def make_sexy_list():
    sexy_list = make_list('エロス')
    return render_template('result.html', category='セクシー', list=sexy_list, info=info)

    
#@app.route('/end')
def end():
    exit()

    
if __name__ == '__main__':
    app.run()