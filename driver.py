import requests
import webbrowser
import random

def userInfo(user):
    url = 'https://codeforces.com/api/user.info'

    params = {
        'handles': user
    }

    r = requests.get(url, params)
    data = r.json()

    #print(data)
    #print()

    if(data['status'] != 'OK'):
        print(data['comment'])
        return

    user = data['result'][0]

    #for p in user:
    #    print(p, ': ', user[p], sep='')
    
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


def contestList():
    url = 'https://codeforces.com/api/contest.list'

    r = requests.get(url)
    data = r.json()

    if(data['status'] != 'OK'):
        print('Some error occured while fetching Contest list.. Try again..!')
        return

    contests = []
    #print(data)
    for x in data['result']:
        contests.append(x['id'])
        #print(x['id'])

    return contests

def contestDetails(cid, user):
    print(cid)
    url = 'https://codeforces.com/api/contest.standings'

    params = {
        'contestId' : cid,
        'handles'   : user
    }

    r = requests.get(url, params)
    data = r.json()

    
    #print(data)
    if(data['status'] != 'OK'): return
    data = data['result']

    '''
    for x in data:
        print(x)

    #print(data['contest'])
    for x in data['contest']:
        print(x, data['contest'][x])

    print()
    #print(data['problems'])
    for x in data['problems']:
        print()
        for y in x:
            print(y, x[y])

    #print(data['rows'])
    for x in data['rows']:
        #print(x)
        for y in x:
            print(y)
            print(x[y])
        for y in x['problemResults']:
            print(y)
    '''
    for x in data['rows']:
        i = 0
        for y in x['problemResults']:
            if(y['points'] > 0):
                print(x['party']['contestId'], chr(65+i), y['points'])
            i += 1

def userStatus(user):
    url = 'https://codeforces.com/api/user.status'

    params = {
        'handle' : user,
        'count'  : 100000,
        'gym'    : False
    }

    r = requests.get(url, params)
    data = r.json()

    #print(data)
    if(data['status'] != 'OK'):
        print('User handle not found!')
        return
    data = data['result']

    ls = set()
    s = set()
    m = dict()
    for sub in data:
        prob = sub['problem']
        if(prob['contestId'] >= 100000): continue
        
        ls.add((prob['contestId'], prob['index']))
        if(sub['verdict'] == 'OK'):
            s.add((prob['contestId'], prob['index']))
            m[(prob['contestId'], prob['index'])] = 1
        else:
            if((prob['contestId'], prob['index']) not in m.keys()):
                m[(prob['contestId'], prob['index'])] = 0

    solved = sorted(list(s))
    #for x in solved:
    #    print(x[0], x[1])

    unsolved = []
    for x in ls:
        if(m[x] == 0):
            unsolved.append(x)

    '''
    print()
    print('Unsolved problems:')
    unsolved = sorted(unsolved)
    for x in unsolved:
        print(x[0], x[1])
        #print('https://codeforces.com/contest/' + str(x[0]) + '/problem/' + x[1])

    print()
    print('Attempted:', len(solved)+len(unsolved))
    print('Solved   :', len(solved))
    print('Unsolved :', len(unsolved))
    '''
    
    return {
        'solved'  : solved,
        'unsolved': unsolved
    }

def getUser():
    user = input('Enter user handle: ')
    while(len(user) == 0):
        user = input('Enter user handle: ')
    return user

def getUserDetails():
    user = input('Enter user handle: ')
    userInfo(user)    

def getSolvedNaive():
    contests = contestList()
    print('Total Contests:', len(contests))

    for x in contests:
        contestDetails(x, 'Keshav_J')

def getMyProblems(user):
    problems = userStatus(user)
    return problems

def printMyProblemsStat(problems):
    print()
    print('Attempted:', len(problems['solved'])+len(problems['unsolved']))
    print('Solved   :', len(problems['solved']))
    print('Unsolved :', len(problems['unsolved']))

def openURL(url):
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)

def loadUnsolved():
    user = input('Enter user handle: ')
    problems = getMyProblems(user)

    m = dict()
    print()
    print('Unsolved problems:')
    for x in problems['unsolved']:
        print(x[0], x[1])
        if(x[1] not in m.keys()):
            m[x[1]] = []
        m[x[1]].append(x[0])

    '''
    print()
    print('Links:')
    for x in problems['unsolved']:
        print('https://codeforces.com/contest/' + str(x[0]) + '/problem/' + x[1])
    '''

    printMyProblemsStat(problems)
    
    print()
    for x in sorted(m.keys()):
        print(x, '\t', len(m[x]))    

    ch = ''
    while(len(ch) == 0):
        ch = input('Any particular choice (A/B/.../-):')

    if(ch in m.keys()):
        n = len(m[ch])
        
        prob = (m[ch][random.randint(0, n-1)], ch)

    else:
        if(ch != '-'):
            print('Oops! No unsolved problem in that index')
        print('Choosing random problem...')

        unsolved = problems['unsolved']
        n = len(unsolved)

        prob = unsolved[random.randint(0, n-1)]

    print('Loading problem', prob[0], '/', prob[1])

    url = 'https://codeforces.com/contest/' + str(prob[0]) + '/problem/' + prob[1]
    
    openURL(url)


def loadNewProblem():
    print('Choose tag(s):')
    print('--------------')

    tags = ['2-sat', 'binary search', 'bitmasks', 'brute force', 'chinese remainder theorem',
            'combinotorics', 'constructive algorithms', 'data structures', 'dfa and similar',
            'divide and conquer', 'dp', 'dsu', 'expression parsing', 'fft', 'flows', 'games',
            'grometry', 'graph matchings', 'graphs', 'greedy', 'hashing', 'implementation',
            'interactive', 'math', 'matrices', 'meet-in-the-middle', 'number theory',
            'probabilities', 'schedules', 'shortest paths', 'sortings',
            'string suffix structures', 'strings', 'ternary search', 'trees', 'two pointers']

    i = 1
    for p in tags:
        print(i, p)
        i += 1

    print()
    ch = list(map(int, input('Enter your choices: ').split()))

    url = 'https://codeforces.com/api/problemset.problems'

    params = {
        'tags' : ''
    }

    for i in ch:
        params['tags'] += tags[i-1] + ';'

    print()
    print('Choosen tags:')
    print('-------------')
    for i in ch:
        print(tags[i-1])

    r = requests.get(url, params)
    data = r.json()

    #print(data)

    if(data['status'] != 'OK'):
        print(data['comment'])
        return

    problems = []

    for p in data['result']['problems']:
        problems.append((p['rating'], p['contestId'], p['index'], p['name']))

    problems.sort()

    if(len(problems) == 0):
        print('No problem with that combination of tags')
        return

    i = 1
    for p in problems:
        print(i, *p, sep='\t')
        i += 1

    ch = int(input('Choose a problem (0 for random): '))

    n = len(problems)
    if(ch in range(1, n+1)):
        prob = problems[ch-1]
    else:
        prob = problems[random.randint(0, n-1)]

    print()
    print('Loading problem...')
    print('Name   : ', prob[3])
    print('Contest: ', prob[1], '/', prob[2])
    print('Rating : ', prob[0])
    

    url = 'https://codeforces.com/contest/' + str(prob[1]) + '/problem/' + prob[2]
    
    openURL(url)
    

# Driver Code
ch = 0
while(ch != 6):
    print('1. User Profile')
    print('2. Show Solved Problems')
    print('3. Show unolved Problems')  
    print('4. Load an unsolved Problems')
    print('5. Load a new Problem')
    print('6. Exit')

    ch = -1
    while(ch not in range(1, 7)):
        ch = input()
        if(ch in ['1', '2', '3', '4', '5', '6']):
            ch = int(ch)
    
    if(ch == 1):
        user = getUser()
        userInfo(user)

    elif(ch == 2):
        user = getUser()
        problems = getMyProblems(user)

        m = dict()
        print()
        print('Solved problems:')
        for x in problems['solved']:
            print(x[0], x[1])
            if(x[1] not in m.keys()):
                m[x[1]] = 0
            m[x[1]] += 1
                
        printMyProblemsStat(problems)

        print()
        for x in sorted(m.keys()):
            print(x, '\t', m[x])

    elif(ch == 3):
        user = getUser()
        problems = getMyProblems(user)
        m = dict()

        print()
        print('Unsolved problems:')
        for x in problems['unsolved']:
            print(x[0], x[1])
            if(x[1] not in m.keys()):
                m[x[1]] = 0
            m[x[1]] += 1

        '''    
        print()
        print('Links:')
        for x in problems['unsolved']:
            print('https://codeforces.com/contest/' + str(x[0]) + '/problem/' + x[1])
        '''
        
        printMyProblemsStat(problems)

        print()
        for x in sorted(m.keys()):
            print(x, '\t', m[x])

    elif(ch == 4):
        loadUnsolved()

    elif(ch == 5):
        loadNewProblem()

    print()
