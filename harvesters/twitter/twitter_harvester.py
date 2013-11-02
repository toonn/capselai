import codecs
import twitter

tw = twitter.Api(
        consumer_key='jxuT0U0d55qkDURTiRdeFg',
        consumer_secret='MwmuJ7he4tLqixbscHA80QYpHUvHZggCZxDCHGT0unI',
        access_token_key='Ya6pzMxB90mNS2O1QpHRbqEnqyDMukQqQMnFGCMG',
        access_token_secret='I4xkiyyGINNqAzc06CBWTqKQCWsH2xYbirSwGo7Qz4')

print 'Planting seeds...'
seeds = [
    '#news',
    '#fail',
    '#economy',
    '#startup',
    '#android',
    '#app',
    '#education',
    '#climate',
    '#drought',
    '#globalwarming',
    '#computerscience',
    '#cs',
    '#opensource',
    '#github',
    '@github',
    '#datamining',
    '#ai',
    '#nsa',
    '#spying',
    '@nsa',
    '#nasa',
    '@nasa',
    '#kuleuven',
    '#cantus',
    '#cooking',
    u'#\u7b11',
    '#law',
    '#ethiopia'
    ]

print 'Growing the crops...'
tweets_per_seed = 100
# This for loop could easily be replaced by a dictionary comprehension.
#
# harvest = {seed : [plant.GetText() for plant in tw.GetSearch(term=seed,
#                    count= tweets_perkseed]
#            for seed in seeds} 
#
# However for clarity, ease of understanding and the possible future
# need to add timing constraints because of twitter's rate limits, we use
# an ordinary for loop.
harvest = {}
for seed in seeds:
    plants = tw.GetSearch(term=seed, count=tweets_per_seed)
    crops = [plant.GetText() for plant in plants]
    harvest[seed] = crops

print 'Bringing in the harvest...'
for name, crop in harvest.iteritems():
    file = codecs.open(name + '.tweets', 'w', 'utf-8')
    file.write('\n'.join(crop))
    file.close()
