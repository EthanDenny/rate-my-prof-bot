from parse_query import parse_query

import sys


query = sys.argv[1]
query = query.replace(' ', '+')

success, firstName, lastName, avgRating, wouldTakeAgainPercent, avgDifficulty = parse_query(query)

if success:
    msg = f'{firstName} {lastName}: Average rating is {avgRating} and {wouldTakeAgainPercent}% would take again, with an average difficulty of {avgDifficulty}'
    print(msg)
