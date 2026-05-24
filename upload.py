import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# ==========================================
# CONFIGURATION
# ==========================================
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, file_path, title, description, tags, publish_at, category_id="27"):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id,          
            'defaultLanguage': 'en',            
            'defaultAudioLanguage': 'en'        
        },
        'status': {
            'privacyStatus': 'private',         
            'publishAt': publish_at,            
            'selfDeclaredMadeForKids': False,
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    
    print(f"Uploading and scheduling: {title}...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    
    print(f"Successfully uploaded and scheduled! ID: {response['id']}")

# ==========================================
# VIDEO METADATA
# ==========================================
videos_to_upload = [
    {
        "file": "May 27th — Saint Augustine of Canterbury, Missionary to England.mp4",
        "title": "May 27th, Saint Augustine of Canterbury, Missionary to England",
        "desc": """Saint Augustine of Canterbury brought the Gospel to England with perseverance, patience, and steady leadership. His life reminds us that planting faith takes time—but God grows what we faithfully begin.

Follow for a new saint every day

#SaintOfTheDay #May27 #May27Saint #SaintOfTheDayMay27 #AugustineOfCanterbury #SaintAugustineOfCanterbury #StAugustineOfCanterbury #Canterbury #MissionarySaint #Catholic #Christian #DailySaint #CatholicSaints #ChristianHistory #Faith #Shorts #CatholicShorts #ChristianShorts""",
        "tags": ["May 27 saint", "Saint of the day May 27", "saint may 27", "May 27 Catholic saint", "Augustine of Canterbury", "Saint Augustine of Canterbury", "St Augustine of Canterbury", "Canterbury saints", "English saints", "missionary saint", "bishop saint", "Church history", "Catholic saints", "Christian saints", "daily saint", "Catholic shorts", "Christian shorts"],
        "publish_at": "2026-05-27T15:00:00.000Z"
    },
    {
        "file": "May 28th — Saint Margaret Pole, Martyr of Conscience.mp4",
        "title": "May 28th, Saint Germanus of Paris",
        "desc": """Saint Germanus of Paris led with compassion and firmness—defending the poor and calling for justice. His life reminds us that faith isn’t passive…it steps in when something is wrong.

Follow for a new saint every day

#SaintOfTheDay #May28 #May28Saint #SaintOfTheDayMay28 #GermanusOfParis #SaintGermanus #StGermanus #Catholic #Christian #DailySaint #CatholicSaints #Justice #Charity #BishopSaint #France #Shorts #CatholicShorts #ChristianShorts""",
        "tags": ["May 28 saint", "Saint of the day May 28", "saint may 28", "May 28 Catholic saint", "Germanus of Paris", "Saint Germanus", "St Germanus", "French saints", "bishop saint", "charity", "justice", "Catholic saints", "Christian saints", "daily saint", "Catholic shorts", "Christian shorts"],
        "publish_at": "2026-05-28T15:00:00.000Z"
    },
    {
        "file": "May 29th — Saint Maximinus of Trier, Defender of Orthodoxy.mp4",
        "title": "May 29th, Pope Paul VI",
        "desc": """Pope Paul VI guided the Church through a time of major change with patience and conviction. His witness shows how leadership means staying faithful even in uncertainty.

Follow for a new saint every day

#SaintOfTheDay #May29 #May29Saint #SaintOfTheDayMay29 #PaulVI #PopePaulVI #SaintPaulVI #Catholic #Christian #DailySaint #CatholicSaints #ChurchHistory #Pope #Faith #Leadership #Shorts #CatholicShorts #ChristianShorts""",
        "tags": ["May 29 saint", "Saint of the day May 29", "saint may 29", "May 29 Catholic saint", "Paul VI", "Pope Paul VI", "Saint Paul VI", "pope saint", "Catholic popes", "Church history", "Vatican II", "leadership", "Catholic saints", "Christian saints", "daily saint", "Catholic shorts", "Christian shorts"],
        "publish_at": "2026-05-29T15:00:00.000Z"
    },
    {
        "file": "May 30th, Saint Joan of Arc, The Maid of Orléans.mp4",
        "title": "May 30th, Saint Joan of Arc, The Maid of Orléans",
        "desc": """Saint Joan of Arc trusted God’s call even when it made no sense to others. Her courage reminds us that faith sometimes means standing alone—but never without purpose.

Follow for a new saint every day

#SaintOfTheDay #May30 #May30Saint #SaintOfTheDayMay30 #JoanOfArc #SaintJoanOfArc #StJoanOfArc #Catholic #Christian #DailySaint #CatholicSaints #Courage #Faith #WomenSaints #France #ChristianHistory #Shorts #CatholicShorts #ChristianShorts""",
        "tags": ["May 30 saint", "Saint of the day May 30", "saint may 30", "May 30 Catholic saint", "Joan of Arc", "Saint Joan of Arc", "St Joan of Arc", "French saints", "women saints", "martyr saint", "Hundred Years War", "Catholic saints", "Christian saints", "courage", "faith", "daily saint", "Catholic shorts", "Christian shorts"],
        "publish_at": "2026-05-30T15:00:00.000Z"
    },
    {
        "file": "May 31st , Visitation of the Blessed Virgin Mary, The Meeting of Promise.mp4",
        "title": "May 31st, Visitation of the Blessed Virgin Mary, The Meeting of Promise",
        "desc": """The Visitation shows love in motion—Mary bringing Christ to Elizabeth with humility and joy. It reminds us that faith isn’t meant to stay hidden…it’s meant to be shared.

Follow for a new saint every day

#SaintOfTheDay #May31 #May31 #SaintOfTheDayMay31 #Visitation #BlessedVirginMary #Mary #Catholic #Christian #DailySaint #CatholicFaith #ChristianFaith #Gospel #Joy #Shorts #CatholicShorts #ChristianShorts""",
        "tags": ["May 31 feast", "Saint of the day May 31", "May 31 Catholic", "Visitation of Mary", "Blessed Virgin Mary", "Marian feast", "Gospel", "Catholic feast day", "Christian feast", "joy", "faith", "Catholic shorts", "Christian shorts"],
        "publish_at": "2026-05-31T15:00:00.000Z"
    }
]

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    youtube = get_authenticated_service()
    for vid in videos_to_upload:
        try:
            upload_video(youtube, vid["file"], vid["title"], vid["desc"], vid["tags"], vid["publish_at"])
        except Exception as e:
            print(f"Error uploading '{vid['file']}': {e}")