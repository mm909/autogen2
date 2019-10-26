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
BADTESTS      = "/home/mussem1/460/Tests/Phase4/Espresso/BadTests/*"
GOODTESTS     = "/home/mussem1/460/Tests/Phase4/Espresso/GoodTests/*"
BADTESTSPLUS  = "/home/mussem1/460/Tests/Phase4/Espresso+/BadTests/*"
GOODTESTSPLUS = "/home/mussem1/460/Tests/Phase4/Espresso+/GoodTests/*"
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
                               '-plus',
                     dest    = 'plusCLA',
                     action  = 'store_true',
                     default = False,
                     help    = 'Run espresso plus test.'
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

parser.add_argument(
                               '-sg',
                     dest    = 'sgCLA',
                     action  = 'store',
                     default = "",
                     help    = 'Tests a single \'good\' file.'
                    )

parser.add_argument(
                               '-sb',
                     dest    = 'sbCLA',
                     action  = 'store',
                     default = "",
                     help    = 'Tests a single \'bad\' file.'
                    )

args = parser.parse_args()

if not (args.badCLA or args.goodCLA or args.allCLA or args.sgCLA != "" or args.sbCLA != ""):
    print("\n\tMust select one of the following: \n\t -good \n\t -bad \n\t -all \n\t -sg|-sb [File] \n")
    exit()

if args.sgCLA != "" or args.sgCLA != "" :
    tempSplit = args.sgCLA.split('.')[1]
    if(tempSplit != "java"):
        print("\n\tGiven file must be .java\n")
        exit()

""" ant   : Compile with ant """
""" output: Errors if needed """
def ant():
    print("\n Compiling...")
    os.system('ant clean > antcleanmessages.txt')
    os.system('ant > antmessages.txt')
    f=open("antmessages.txt", "r")
    if f.mode == 'r':
        contents = f.read()
        if not "BUILD SUCCESSFUL" in contents:
            print(contents)
            exit()
    os.system('clear')
    print("\n Compile: BUILD SUCCESSFUL")

if args.compCLA:
    ant()
else:
    os.system('clear')
    print("\n Compiling Skipped.")

if not (args.sgCLA != "" or args.sbCLA != ""):
    print('\n')

if args.allCLA or args.goodCLA:
    if not args.plusCLA:
        goodTests = (glob.glob(GOODTESTS))
        print(" Globing GOOD tests : " + GOODTESTS)
    else:
        goodTests = (glob.glob(GOODTESTSPLUS))
        print(" Globing GOOD tests : " + GOODTESTSPLUS)
if args.allCLA or args.badCLA:
    if not args.plusCLA:
        badTests  = (glob.glob(BADTESTS))
        print(" Globing BAD tests  : " + BADTESTS)
    else:
        badTests  = (glob.glob(BADTESTSPLUS))
        print(" Globing BAD tests  : " + BADTESTSPLUS)


if not (args.sgCLA != "" or args.sbCLA != ""):
    print('\n')

""" Tests a single good file """
def testGood(file):
    print("\n Running Good Test on: " + file)
    os.system('./espressoc '+ file +' > mine 2> /dev/null')
    os.system('./espressocr '+ file +' > his 2> /dev/null')
    os.system('diff mine his > differences.txt')

    f = open("differences.txt", "r")
    if f.mode == 'r':
        contents = f.read()
        if contents != "":
            print("\n\tFailed\n")
        else:
            print("\n\tPassed\n")

""" testGood : Run all good tests     """
""" output   : Count of passed/failed """
""" output   : Failed file names      """
def testGoodAll():
    passed = []
    failed = []
    print("       -- Running Good Tests -- ")
    with Bar(max=len(goodTests)) as pbar:
        for test in goodTests:
            os.system('./espressoc '+ test +' > mine 2> /dev/null')
            os.system('./espressocr '+ test +' > his 2> /dev/null')
            os.system('diff mine his > differences.txt')

            f = open("differences.txt", "r")
            if f.mode == 'r':
                contents = f.read()
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

""" Tests a single bad file """
def testBad(file):
    print("\n Running Bad Test on: " + file)
    os.system('./espressoc ' + file + ' > mine 2> /dev/null')
    os.system('./espressocr ' + file + ' > his 2> /dev/null ')
    os.system('diff mine his > differences.txt')

    myOutput = open("mine", "r")
    myOutputText = myOutput.read()
    myOutputTextList = myOutputText.split("\n")
    lastLine = "";
    for string in myOutputTextList[len(myOutputTextList) - 2].split(" ")[1:]:
        lastLine = lastLine + string + " "
        pass
    myFinal = lastLine
    if "S = U = C = C = E = S = S" in myOutputText:
        myFinal = "*** Finished without ERROR ***"

    hisOutput = open("his", "r")
    hisOutputText = hisOutput.read()
    hisOutputTextList = hisOutputText.split("\n")
    lastLine = "";
    for string in hisOutputTextList[len(hisOutputTextList) - 2].split(" ")[1:]:
        lastLine = lastLine + string + " "
        pass
    hisFinal = lastLine

    if myFinal == hisFinal:
        print("\n\tPassed\n")
    else:
        print("\n\tFailed " + file + ":")
        print("\t\tMine > " + myFinal)
        print("\t\tHis  > " + hisFinal)
        print("\n")


""" testBad : Run all bad tests      """
""" output  : Our error message      """
""" output  : His error message      """
def testBadAll():
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

            if myFinal == hisFinal:
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
        print("              All Passed.\n")

if args.allCLA or args.goodCLA:
    testGoodAll()
if args.allCLA or args.badCLA:
    testBadAll()
if args.sgCLA != "":
    testGood(args.sgCLA)
if args.sbCLA != "":
    testBad(args.sbCLA)
