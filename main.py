from tldr import tldr
import re
import requests
from fastapi import FastAPI

app = FastAPI()

def getPageContent (pageid):
    endpoint = """https://iris-sa.schibsted.tech/v1/pages/articles/"""
    res = requests.get(endpoint + pageid)
    data = res.json()
    toSummarize = []
    for key in data['items']:
        if (re.search('text', key)) and not re.search('text_ad', key) and key != 'text-title' and key != 'text-lead':
            toSummarize.append(data['items'][key]['text']['value'])
        if (re.search('list-', key)):
            for listitem in data['items'][key]['items']:
                toSummarize.append(listitem['value'])

    return [data['items']['text-title']['text']['value'], toSummarize]

@app.get("/summarize")
async def root(url: str):

    regex = "^https:\/\/www.(?P<domain>[a-zA-Z]+)\.no\/.+\/(?P<id>[a-zA-Z0-9]{6})\/.+$"
    #url = "https://www.aftenbladet.no/lokalt/i/L5bzWQ/mener-uro-og-mistillit-truer-politiets-evne-til-aa-gjoere-jobben"
    
    



    match = re.findall(regex, url)
    domain, id = match[0]
    title, content = getPageContent(id)
    text = ' '.join(content)

    summary_length = 0.3
    if (len(text) < 1000):
        summary_length = 0.4
    if (len(text) > 2500):
        summary_length = 0.3
    if (len(text) > 5000):
        summary_length = 0.15
    if (len(text) > 10000):
        summary_length = 0.1

    summary = tldr(text, summary_length) 
    return {
        "title": title,
        "originalLength": len(text),
        "summaryLength": len(summary),
        "summary": summary
        }