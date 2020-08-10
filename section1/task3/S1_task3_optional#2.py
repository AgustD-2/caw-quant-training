from crypto_news_api import CryptoControlAPI
import pandas as pd
# Connect to the CryptoControl API
api = CryptoControlAPI("c570bf2c119d13e0cc9eb0b3d69d414d")

# Connect to a self-hosted proxy server (to improve performance) that points to cryptocontrol.io
proxyApi = CryptoControlAPI(
    "c570bf2c119d13e0cc9eb0b3d69d414d", "http://cryptocontrol_proxy/api/v1/public")

# Get top news
print(pd.DataFrame(api.getTopNews()))

# get latest russian news
print(pd.DataFrame(api.getLatestNews("ru")))

# get top bitcoin news
print(pd.DataFrame(api.getTopNewsByCoin("bitcoin")))

# get top EOS tweets
print(pd.DataFrame(api.getTopTweetsByCoin("eos")))

# get top Ripple reddit posts
print(pd.DataFrame(api.getLatestRedditPostsByCoin("ripple")))

# get reddit/tweets/articles in a single combined feed for NEO
print(api.getTopFeedByCoin("neo"))

# get latest reddit/tweets/articles (seperated) for Litecoin
print(api.getLatestItemsByCoin("litecoin"))

# get details (subreddits, twitter handles, description, links) for ethereum
print(api.getCoinDetails("ethereum"))
