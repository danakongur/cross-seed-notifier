from fastapi import FastAPI, Request
from pydantic import BaseModel
import apprise
import os

''' json data example
{'title': 'cross-seed', 'body': 'search: Injected The New Normal S01 1080p WEB-DL DD+ 5.1 x264-TrollHD from 1 trackers: TorrentLeech', 'extra': {'event': 'RESULTS', 'name': 'The New Normal S01 1080p WEB-DL DD+ 5.1 x264-TrollHD', 'infoHashes': ['55c7d323f24211c777e4ef4d3372caabd6985187'], 'trackers': ['TorrentLeech'], 'source': 'search', 'result': 'INJECTED'}}
 '''

discordWebhookURL = os.getenv("DISCORD_WEBHOOK_URL")

class ExtraData(BaseModel):
    event: str
    name: str
    infoHashes: list[str]
    trackers: list[str]
    source: str
    result: str

class CrossSeedNotification(BaseModel):
    title: str
    body: str
    extra: ExtraData

app = FastAPI()

apprise_instance = apprise.Apprise()
apprise_instance.add(discordWebhookURL)

def constructDiscordMessage(jsonData: CrossSeedNotification) -> str:
    data =  f"""### Cross seed {jsonData.extra.result.lower()}
Torrent: {jsonData.extra.name}
Trackers: {str(*jsonData.extra.trackers)}
Source: {jsonData.extra.source}"""
    return data

def answer(data):
    try:
        success = apprise_instance.notify(body=constructDiscordMessage(data), body_format=apprise.NotifyFormat.MARKDOWN)
        if success:
            return {"status": f"Notification sent"}
        else:
            return {"status": f"Failed to send notification"}
    except Exception as e:
        return {"status": f"Sending got error {e}"}

@app.get("/")
async def root():
    return {"message": "Needs a json body"}

@app.post("/")
async def postroot(data: CrossSeedNotification):
    return answer(data)

@app.get("/health")
async def healtcheck():
    return {"status": "healthy"}


