import requests

def fetch_leetcode_daily():
    url = "https://leetcode.com/graphql"
    
    # GraphQL query as a string
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        date
        link
        question {
          title
          difficulty
        }
      }
    }
    """
    payload = {"query": query}
    response = requests.post(url, json=payload)
    data = response.json()
    title = data["data"]["activeDailyCodingChallengeQuestion"]["question"]["title"]
    link = data["data"]["activeDailyCodingChallengeQuestion"]["link"]
    difficulty =  data["data"]["activeDailyCodingChallengeQuestion"]["question"]["difficulty"]


    hashMap = {
        "title": title,
        "link": link,
        "difficulty" : difficulty
    }

    return hashMap
print(fetch_leetcode_daily() )