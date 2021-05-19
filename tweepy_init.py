import tweepy
import logging
import os

logger = logging.getLogger()


def create_api():
    consumer_key = "fok4Pu0OuWz4DTFQCB7SEl3Yt"
    consumer_secret = "eziGfY2pKr3vUG8o1H6usXDj7j3GyYTJT6TLaW8oAZLYItUph5"
    access_token = "922446690216374272-SaHTiSeOgJE5bLR5eHwg4hUrQr0ftTN"
    access_token_secret = "ZqnqmEKlwc3ilWDbliCbN4uQMGg3MT6iCUb0E8cKuuV4S"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print('verified successfully')
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


if __name__ == "__main__":
    create_api()
