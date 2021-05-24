
import tweepy
import logging
import os

logger = logging.getLogger()


def create_api():
    consumer_key = "cmLHm7z65P5AbkvRYTeFMMQ3X"
    consumer_secret = "bCSnfsXdmTQekYRAjf4oVrtPAqT54VPpjXFstvrHiXeY4udgWr"
    access_token ="1389247637212172291-to9A9NINRW6b9tm7qqXUG6kYP26Oej"
    access_token_secret = "kRk4iPuAHf9WB98ORsBQzDtxXaecs07dnT5yCyI2jSCaC"
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
    








