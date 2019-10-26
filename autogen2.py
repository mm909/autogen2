# Mikian Musser
# https://github.com/mm909/autogen2

"""             DISCLAMER FROM AUTHOR             """
''' Please make sure your tests also pass autogen '''
'''     Only use this to help your development    '''
"""             DISCLAMER FROM AUTHOR             """

import os
import glob
import argparse
from progress import *

""" CHANGE """
BADTESTS  = "/home/mussem1/460/Tests/Phase4/Espresso/BadTests/*"
GOODTESTS = "/home/mussem1/460/Tests/Phase4/Espresso/GoodTests/*"
""" CHANGE """

parser = argparse.ArgumentParser(
                                 description = 'autogen2 built for phase 4 CS460',
                                 epilog = "autogen2 - https://github.com/mm909/autogen2"
                                )

parser.add_argument(
                               '-nocomp',
                     dest    = 'compCLA',
                     action  = 'store_false',
                     default = True,
                     help    = 'Does not compile with ant before running.'
                    )

parser.add_argument(
                               '-all',
                     dest    = 'allCLA',
                     action  = 'store_true',
                     default = False,
                     help    = 'Runs all tests (Good and Bad).'
                    )

parser.add_argument(
                               '-good',
                     dest    = 'goodCLA',
                     action  = 'store_true',
                     default = False,
                     help    = 'Runs all good tests.'
                    )

parser.add_argument(
                               '-bad',
                     dest    = 'badCLA',
                     action  = 'store_true',
                     default = False,
                     help    = 'Runs all bad tests.'
                    )

args = parser.parse_args()

if not (args.badCLA or args.goodCLA or args.allCLA):
    print("\n\tMust select a set of tests: -good | -bad | -all\n")
    exit()

""" ant   : Compile with ant """
""" output: Errors if needed """
def ant():
    print("\nCompiling...")
    os.system('ant clean > antcleanmessages.txt')
    os.system('ant > antmessages.txt')
    f=open("antmessages.txt", "r")
    if f.mode == 'r':
        contents = f.read()
        if not "BUILD SUCCESSFUL" in contents:
            print(contents)
            exit()
    os.system('clear')
    print("\nCompile: BUILD SUCCESSFUL")

if args.compCLA:
    ant()
else:
    print("\nCompiling Skipped.")

print('\n')
if args.allCLA or args.goodCLA:
    goodTests = (glob.glob(GOODTESTS))
    print("Globing GOOD tests : " + GOODTESTS)
if args.allCLA or args.badCLA:
    badTests  = (glob.glob(BADTESTS))
    print("Globing BAD tests  : " + BADTESTS)
print('\n')


""" testGood : Run all good tests     """
""" output   : Count of passed/failed """
""" output   : Failed file names      """
def testGood():
    passed = []
    failed = []
    print("       -- Running Good Tests -- ")
    with Bar(max=len(goodTests)) as pbar:
        for test in goodTests:
            os.system('./espressoc '+ test +' > mine 2> /dev/null')
            os.system('./espressocr '+ test +' > his 2> /dev/null')
            os.system('diff mine his > differences.txt')

            f=open("differences.txt", "r")
            if f.mode == 'r':
                contents =f.read()
                if contents != "":
                    failed.append(test)
                else:
                    passed.append(test)
            pbar.next()
            pbar.update()

        if(len(failed) > 0):
            print("\n\n\tPassed : " + str(len(passed)))
            print("\tFailed : " + str(len(failed)))
            print("\n\tFailed: ")
            for fail in failed:
                faillist = fail.split('/')
                print("\t\t" + faillist[len(faillist) - 1])
                pass
            print("\n")
        else:
            print("\n              All Passed.\n")

""" testBad : Run all bad tests      """
""" output  : Our error message      """
""" output  : His error message      """
def testBad():
    passed = []
    failed = []
    ourMessages = []
    hisMessages = []
    print("       -- Running Bad Tests -- ")
    with Bar(max=len(badTests)) as pbar:
        for test in badTests:
            os.system('./espressoc '+test+' > mine 2> /dev/null')
            os.system('./espressocr '+test+' > his 2> /dev/null ')
            os.system('diff mine his > differences.txt')

            myOutput = open("mine", "r")
            myOutputText = myOutput.read()
            myOutputTextList = myOutputText.split("\n")
            lastLine = "";
            for string in myOutputTextList[len(myOutputTextList) - 2].split(" ")[1:]:
                lastLine = lastLine + string + " "
                pass
            myFinal = lastLine
            if "S = U = C = C = E = S = S" in myFinal:
                myFinal = "*** Finished without ERROR ***"

            hisOutput = open("his", "r")
            hisOutputText = hisOutput.read()
            hisOutputTextList = hisOutputText.split("\n")
            lastLine = "";
            for string in hisOutputTextList[len(hisOutputTextList) - 2].split(" ")[1:]:
                lastLine = lastLine + string + " "
                pass
            hisFinal = lastLine

            if(myFinal == hisFinal):
                passed.append(test)
            else:
                failed.append(test)

                ourMessages.append(myFinal);
                hisMessages.append(hisFinal);
            pbar.next()
            pbar.update()


    if(len(ourMessages) != 0):
        print("\n\tPassed : " + str(len(passed)))
        print("\tFailed : " + str(len(failed)))
        print("\n")
        for i,message in enumerate(ourMessages):
            faillist = failed[i].split('/')
            print("\tFailed " + faillist[len(faillist) - 1] + ":")
            print("\t\tMine > " + ourMessages[i])
            print("\t\tHis  > " + hisMessages[i])
            print("\n")
    else:
        print("              No Errors.\n")

if args.allCLA or args.goodCLA:
    testGood()
if args.allCLA or args.badCLA:
    testBad()
