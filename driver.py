import requests
import webbrowser
import random
import pandas as pd

from fetch_module import getUserInfo
from fetch_module import displayUserInfo
from fetch_module import getUserProblems
from fetch_module import getUserProblemsDetailed
from fetch_module import checkUserActivity
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

    low = input('Enter minimum rating: ')
    if(low.isdigit()): low = int(low)
    else             : low = 0

    high = input('Enter maximum rating: ')
    if(high.isdigit()): high = int(high)
    else              : high = 3500

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
        if('rating' not in prob.keys()):
            prob['rating'] = 0

        if(low <= prob['rating'] and prob['rating'] <= high):
            problems.append((prob['rating'], prob['contestId'], prob['index'], prob['name']))
    
    problems.sort()

    if(len(problems) == 0):
        print('Oops! No problem found with that combination of tags...')
        return

    i = 1
    print(*('#', 'Rating', 'Contest', 'Index', 'Problem Name'), sep='\t')
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

def showStats(userId):
    problems = getUserProblemsDetailed(userId)

    solvedProblems = problems['solved']
    unsolvedProblems = problems['unsolved']
    problemTags = problems['tags']
    
    #for p in problemTags:
    #    print(p, problemTags[p])

    tags = ['2-sat', 'binary search', 'bitmasks', 'brute force', 'chinese remainder theorem',
            'combinatorics', 'constructive algorithms', 'data structures', 'dfs and similar',
            'divide and conquer', 'dp', 'dsu', 'expression parsing', 'fft', 'flows', 'games',
            'geometry', 'graph matchings', 'graphs', 'greedy', 'hashing', 'implementation',
            'interactive', 'math', 'matrices', 'meet-in-the-middle', 'number theory',
            'probabilities', 'schedules', 'shortest paths', 'sortings', '*special',
            'string suffix structures', 'strings', 'ternary search', 'trees', 'two pointers']

    solvedTags = dict()
    unsolvedTags = dict()
    
    for tag in tags:
        solvedTags[tag] = 0
        unsolvedTags[tag] = 0

    for problem in solvedProblems:
        for tag in problemTags[problem]:
            solvedTags[tag] += 1

    for problem in unsolvedProblems:
        for tag in problemTags[problem]:
            unsolvedTags[tag] += 1

    #print(solvedTags)
    #print(unsolvedTags)

    table = [[tag, solvedTags[tag], unsolvedTags[tag]] for tag in tags]
    table.sort(key = lambda x: x[1]*1000+x[2], reverse = True)

    print(pd.DataFrame(table))
    print()

    category = {
            'exp' : [['Title', 'Solved', 'Unsolved']],
            'med' : [['Title', 'Solved', 'Unsolved']],
            'beg' : [['Title', 'Solved', 'Unsolved']],
            'zer' : [['Title', 'Solved', 'Unsolved']]
        }
    
    for tag in table:
        if(tag[1]+tag[2] >= 100):
            category['exp'].append(tag)
        elif(tag[1]+tag[2] >= 25):
            category['med'].append(tag)
        elif(tag[1]+tag[2] >= 1):
            category['beg'].append(tag)
        else:
            category['zer'].append(tag)

    if(len(category['exp']) > 0):
        print('Tags you have some solid experience in:')
        print(pd.DataFrame(category['exp']))
        print()

    if(len(category['med']) > 0):
        print('Tags you have reasonable experience and need to work on:')
        print(pd.DataFrame(category['med']))
        print()

    if(len(category['beg']) > 0):
        print('Tags you have very little experience and need to focus:')
        print(pd.DataFrame(category['beg']))
        print()

    if(len(category['zer']) > 0):
        print('Tags you have not yet touched:')
        print(pd.DataFrame(category['zer']))
        print()

# Driver Code

file = open("userHandle.txt", "r")
userHandle = file.read()
file.close()

userChoice = -1
while(userHandle == '' or (getUserInfo(userHandle) == False)):
    userHandle = input('Enter your codeforces user handle: ')

file = open("test.txt", "w")
file.write(userHandle)
file.close()
    
checkUserActivity(userHandle)

n = 8
while(userChoice != n):
    print()
    print('1. User profile')
    print('2. Show solved Problems')
    print('3. Show unolved Problems')  
    print('4. Load an unsolved Problems')
    print('5. Load a new Problem')
    print('6. Show my stats')
    print('7. Change User Handle')
    print('8. Exit')

    userChoice = -1
    while(userChoice < 1 or n < userChoice):
        userChoice = input('Enter Your choice: ')
        if(userChoice.isdigit()):
            userChoice = int(userChoice)
        else:
            userChoice = -1
    
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
        showStats(userHandle)

    elif(userChoice == 7):
        userHandle = ''
        while(userHandle == '' or (getUserInfo(userHandle) == False)):
            userHandle = input('Enter your codeforces user handle: ')
        
        file = open("userHandle.txt", "w")
        file.write(userHandle)
        file.close()

    print()
