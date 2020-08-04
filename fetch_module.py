import requests
import time

def getUserInfo(userId):
    url = 'https://codeforces.com/api/user.info'

    params = {
        'handles': userId
    }

    response = requests.get(url, params)
    data = response.json()

    if(data['status'] != 'OK'):
        print(data['comment'])
        return False

    user = data['result'][0]

    return user

def displayUserInfo(userId):
    user = getUserInfo(userId)

    if(user == False): return

    print()
    if('firstName' in user.keys() and 'lastName' in user.keys()):
        print('Name    :', user['firstName'], user['lastName'])
    if('handle' in user.keys()):
        print('Handle  :', user['handle'])
    if('rating' in user.keys() and 'maxRating' in user.keys()):
        print('Rating  :', user['rating'], '(max.', user['maxRating'], ')')
    if('rank' in user.keys() and 'maxRank' in user.keys()):
        print('Rank    :', user['rank'], '(max.', user['maxRank'], ')')
    if('city' in user.keys()):
        print('City    :', user['city'])
    if('country' in user.keys()):
        print('Country :', user['country'])

    print()
    if('friendOfCount' in user.keys()):
        print('FriendOf:', user['friendOfCount'])
    if('contribution' in user.keys()):
        print('Contrib.:', user['contribution'])
    if('organization' in user.keys()):
        print('Org.    :', user['organization'])

    return True

def getUserProblems(userId):
    url = 'https://codeforces.com/api/user.status'

    params = {
        'handle' : userId,
        'count'  : 100000,
        'gym'    : False
    }

    response = requests.get(url, params)
    data = response.json()

    #if(data['status'] != 'OK'):
    #    print('User handle not found!')
    #    return
    
    submissions = data['result']

    problems = set()
    solved = set()

    for sub in submissions:
        problem = sub['problem']

        if(problem['contestId'] >= 100000): continue  #Gym Ids

        problem_pair = (problem['contestId'], problem['index'])
        
        problems.add(problem_pair)
        if(sub['verdict'] == 'OK'):
            solved.add(problem_pair)

    solved = sorted(list(solved))

    isSolved = dict()
    for problem in problems:
        isSolved[problem] = 0
    for problem in solved:
        isSolved[problem] = 1

    unsolved = []
    for problem in problems:
        if(isSolved[problem] == 0):
            unsolved.append(problem)

    return {
        'solved'  : solved,
        'unsolved': unsolved
    }

def getUserProblemsDetailed(userId):
    url = 'https://codeforces.com/api/user.status'

    params = {
        'handle' : userId,
        'count'  : 100000,
        'gym'    : False
    }

    response = requests.get(url, params)
    data = response.json()

    #if(data['status'] != 'OK'):
    #    print('User handle not found!')
    #    return
    
    submissions = data['result']

    problems = set()
    solved = set()
    tags = dict()

    for sub in submissions:
        problem = sub['problem']

        if(problem['contestId'] >= 100000): continue  #Gym Ids

        problem_pair = (problem['contestId'], problem['index'])

        tags[problem_pair] = problem['tags']
        
        problems.add(problem_pair)
        if(sub['verdict'] == 'OK'):
            solved.add(problem_pair)

    solved = sorted(list(solved))

    isSolved = dict()
    for problem in problems:
        isSolved[problem] = 0
    for problem in solved:
        isSolved[problem] = 1

    unsolved = []
    for problem in problems:
        if(isSolved[problem] == 0):
            unsolved.append(problem)

    return {
        'solved'  : solved,
        'unsolved': unsolved,
        'tags'    : tags
    }

def checkUserActivity(userId):
    url = 'https://codeforces.com/api/user.status'

    params = {
        'handle' : userId,
        'count'  : 1,
        'gym'    : False
    }

    response = requests.get(url, params)
    data = response.json()
    
    last_submission = data['result'][0]
    last_time = last_submission['author']['startTimeSeconds']
    cur_time = int(round(time.time()))
    one_day = 60 * 60 * 24

    print('Hey ', userId, '!', sep='')

    if((cur_time - last_time) / one_day >= 2):
        print("It's been", (cur_time - last_time)//one_day, "days since you've attempted a problem.")
        print("Why don't you try one?")
        return

    url = 'https://codeforces.com/api/user.rating'

    params = {
        'handle' : userId
    }

    response = requests.get(url, params)
    data = response.json()

    ratings = data['result'][-5:]

    gross_rating = ratings[-1]['newRating'] - ratings[0]['oldRating']

    if(gross_rating > 50):
        print('Your rating over the past 5 contests have increased by', gross_rating)
        print('Keep the good work going!')
        return

    if(gross_rating >= 0):
        gorss_rating = '+' + str(gross_rating)
    
    print('Your cummulative rating change over the past 5 contests is', gross_rating)
    print("Why don't you solve some more problems?")
        
def printUserProblemsStat(problems):
    print()
    print('Attempted:', len(problems['solved'])+len(problems['unsolved']))
    print('Solved   :', len(problems['solved']))
    print('Unsolved :', len(problems['unsolved']))
