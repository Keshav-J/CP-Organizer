import requests
import webbrowser
import random

from fetch_module import getUserInfo
from fetch_module import displayUserInfo
from fetch_module import getUserProblems
from fetch_module import printUserProblemsStat


def openURL(url):
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)

def loadUnsolved(userId):
    problems = getUserProblems(userId)

    m = dict()
    print()
    print('Unsolved problems:')
    for prob in problems['unsolved']:
        print(*prob)
        if(prob[1] not in m.keys()):
            m[prob[1]] = []
        m[prob[1]].append(prob[0])

    printUserProblemsStat(problems)
    
    print()
    for code in sorted(m.keys()):
        print(code, '\t', len(m[code]))

    choiceCode = ''
    while(len(choiceCode) == 0):
        choiceCode = input('Any particular choice (A/B/.../-):')

    if(choiceCode in m.keys()):
        n = len(m[choiceCode])
        
        prob = (m[choiceCode][random.randint(0, n-1)], choiceCode)

    else:
        if(choiceCode != '-'):
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

    idx = 1
    for t in tags:
        print(idx, t)
        idx += 1

    print()
    ch = list(map(int, input('Enter your choices (space-separated): ').split()))

    url = 'https://codeforces.com/api/problemset.problems'

    params = {
        'tags' : ''
    }

    for i in ch:
        params['tags'] += tags[i-1] + ';'

    print()
    print('Choosen tags:')
    print('-------------')
    for idx in ch:
        print(tags[idx-1])
    print()
    
    response = requests.get(url, params)
    data = response.json()

    if(data['status'] != 'OK'):
        print(data['comment'])
        return

    problems = []

    for prob in data['result']['problems']:
        if('rating' in prob.keys()):
            problems.append((prob['rating'], prob['contestId'], prob['index'], prob['name']))
        else:
            problems.append((0, prob['contestId'], prob['index'], prob['name']))
    
    problems.sort()

    if(len(problems) == 0):
        print('Oops! No problem found with that combination of tags...')
        return

    i = 1
    for prob in problems:
        print(i, *prob, sep='\t')
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
userChoice = -1
userHandle = ''
while(userHandle == ''):
    userHandle = input('Enter your codeforces user handle: ')
    if(getUserInfo(userHandle) == False):
        userHandle = ''

while(userChoice != 7):
    print()
    print('1. User Profile')
    print('2. Show Solved Problems')
    print('3. Show unolved Problems')  
    print('4. Load an unsolved Problems')
    print('5. Load a new Problem')
    print('6. Change User ')
    print('7. Exit')

    userChoice = -1
    while(userChoice not in range(1, 8)):
        userChoice = input('Enter Your choice: ')
        if(userChoice in ['1', '2', '3', '4', '5', '6', '7']):
            userChoice = int(userChoice)
    
    if(userChoice == 1):
        displayUserInfo(userHandle)

    elif(userChoice == 2 or userChoice == 3):
        problems = getUserProblems(userHandle)
        m = dict()

        print()

        if(userChoice == 2):
            print('Solved problems:')
            for prob in problems['solved']:
                print(*prob)
                if(prob[1] not in m.keys()):
                    m[prob[1]] = 0
                m[prob[1]] += 1
        else:
            print('Unsolved problems:')
            for x in problems['unsolved']:
                print(x[0], x[1])
                if(x[1] not in m.keys()):
                    m[x[1]] = 0
                m[x[1]] += 1
                
        printUserProblemsStat(problems)

        print()
        for x in sorted(m.keys()):
            print(x, '\t', m[x])

    elif(userChoice == 4):
        loadUnsolved(userHandle)

    elif(userChoice == 5):
        loadNewProblem()

    elif(userChoice == 6):
        userHandle = ''
        while(userHandle == ''):
            userHandle = input('Enter your codeforces user handle: ')
            if(getUserInfo(userHandle) == False):
                userHandle = ''

    print()
