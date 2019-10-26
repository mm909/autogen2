# Mikian Musser
# github/mm909

"""             DISCLAMER FROM AUTHOR             """
''' Please make sure your tests also pass autogen '''
'''     Only use this to help your development    '''
"""             DISCLAMER FROM AUTHOR             """

import os
import glob
from progress import *

""" CHANGE """
BADTESTS  = "/home/mussem1/460/Tests/Phase4/Espresso/BadTests/*"
GOODTESTS = "/home/mussem1/460/Tests/Phase4/Espresso/GoodTests/*"
""" CHANGE """

badTests  = (glob.glob(BADTESTS))
goodTests = (glob.glob(GOODTESTS))

# Compile before every run, error if needed
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
ant()

print("\nGlobing BAD tests  : " + BADTESTS)
print("Globing GOOD tests : " + GOODTESTS + "\n")


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

testGood()
testBad()
