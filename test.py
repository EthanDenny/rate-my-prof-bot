from parse_query import parse_query

import sys


query = sys.argv[1]
query = query.replace(' ', '+')

firstName, lastName, avgRating, wouldTakeAgainPercent, avgDifficulty = parse_query(query)

if len(firstName) != 0:
    msg = ''

    if len(firstName) > 1:
        msg += 'Found several professors, here are the top results:\n\n'
    for i in range(len(firstName)):
        percent = max(wouldTakeAgainPercent[i], 0)
        msg += f'{firstName[i]} {lastName[i]}: Average rating is {avgRating[i]} and {percent:.0f}% would take again, with an average difficulty of {avgDifficulty[i]}\n'
    
    print(msg[:-1])
