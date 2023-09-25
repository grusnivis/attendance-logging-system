import csv
import os
import pandas as pd

def merge_teacher():
    path = '/home/pi/ALS_SHARED/Authorized User Masterlist/'

    # CHANGE FILENAME HERE
    filename = 'AuthorizedUsers'

    mainfile = str(path + os.sep + filename + '.csv')
    # Raspberry Pi 1
    copy1 = str(path + os.sep + filename + '00000000944de39a.csv')
    # Raspberry Pi 2
    copy2 = str(path + os.sep + filename + '00000000781547eb.csv')
    name1 = '00000000944de39a.csv'
    name2 = '00000000781547eb.csv'
    try:
        with open(mainfile, 'r', encoding='utf-8') as f:
            file_read = csv.reader(f)
            masterArray = list(file_read)
        masterFlag = 1
        print(filename + ".csv found.")
    except FileNotFoundError:
        masterFlag = 0
        print(filename + ".csv does not exist.")

    try:
        with open(copy1, 'r', encoding='utf-8') as f:
            file_read = csv.reader(f)
            copy1Array = list(file_read)
            copy1mdate = os.path.getmtime(copy1)
        copy1Flag = 1
        print(filename + name1 + " found.")
    except FileNotFoundError:
        copy1Flag = 0
        print(filename + name1 + " does not exist.")

    try:
        with open(copy2, 'r', encoding='utf-8') as f:
            file_read = csv.reader(f)
            copy2Array = list(file_read)
            copy2mdate = os.path.getmtime(copy2)
        copy2Flag = 1
        print(filename + name2 + " found.")
    except FileNotFoundError:
        copy2Flag = 0
        print(filename + name2 + " does not exist.")

    if masterFlag == 1 and ((copy1Flag == 1 and copy2Flag == 0) or (copy1Flag == 0 and copy2Flag == 1)):
        print("Only one sub-file detected. . . Starting merge. . .")
        l = len(masterArray)
        i = 1
        l = l - 2
        copy = []

        if copy1Flag == 1:
            copy = copy1Array
            name = '00000000944de39a.csv'
            length = len(copy1Array)
        elif copy2Flag == 1:
            copy = copy2Array
            name = '00000000781547eb.csv'
            length = len(copy2Array)

        # If copy files are different sizes
        if length > len(masterArray) or length < len(masterArray):
            if length < (len(masterArray)):
                print("The file " + filename + name + " contains less entries existing than the master file. . . Updating "
                                                      "master file with data found. . .")
            elif length > (len(masterArray)):
                print("The file " + filename + name + " contains more entries existing than the master file. . . The file "
                                                      "could be outdated, or the master file was edited manually in the "
                                                      "middle of the creation of this file. Updating master file. . .")
            for i in range(len(copy)):
                nameExists = 0
                header = 0
                for j in range(len(masterArray)):
                    if i == 0:
                        header = 1
                        continue
                    else:
                        if (masterArray[j][1] == copy[i][1] and masterArray[j][2] == copy[i][2]) and (
                                masterArray[j][0] != copy[i][0]):
                            nameExists = 1
                            if copy[i][0] == '':
                                continue
                            masterArray[j][0] = copy[i][0]
                            print(
                                "Entry " + copy[i][2] + " " + copy[i][3] + " exists. Changing RFID to one found in copy: " +
                                copy[i][0])
                            continue
                        elif masterArray[j][1] == copy[i][1] and masterArray[j][2] == copy[i][2]:
                            nameExists = 1
                            continue
                if nameExists == 0 and header == 0:
                    print("New entry for database: " + copy[i][2] + " " + copy[i][3] + " with RFID: " + copy[i][0])
                    masterArray.append(copy[i])

            print(filename + '.csv has been successfully updated.')
            pd.DataFrame(masterArray).to_csv(path + os.sep + filename + '.csv', index=False, header=None, encoding="utf-8")
            os.remove(path + os.sep + filename + name)
            print("Copy file has been removed.")

        else:
            while l >= 0:
                if masterArray[i][0]:
                    if masterArray[i][0] == copy[i][0]:
                        print("Retaining Value. Same data for all three files.")
                    else:
                        if not (copy[i][0]):
                            pass
                        else:
                            print('Swapping ' + masterArray[i][0] + ' for ' + copy[i][0])
                            masterArray[i][0] = copy[i][0]
                    i = i + 1
                    l = l - 1
                else:
                    if not (copy[i][0]):
                        pass
                    else:
                        print("New RFID entry for " + masterArray[i][2] + " " + masterArray[i][3] + ": " + copy[i][0])
                        masterArray[i][0] = copy[i][0]
                    i = i + 1
                    l = l - 1

            print(filename + '.csv has been successfully updated.')
            pd.DataFrame(masterArray).to_csv(path + os.sep + filename + '.csv', index=False, header=None, encoding="utf-8")
            os.remove(path + os.sep + filename + name)
            print("Copy file has been removed.")

    elif masterFlag == 1 and copy1Flag == 1 and copy2Flag == 1:
        print("Two sub-files detected. . .Starting merge. . .")
        i = 1;
        l = len(masterArray)

        # - 1 for array syntax, another - 1 to ignore header
        l = l - 2

        if copy1mdate > copy2mdate:
            copy = copy1Array
            other = copy2Array
            name = '00000000944de39a.csv'
            print(copy1 + " is newer")
        else:
            copy = copy2Array
            other = copy1Array
            name = '00000000781547eb.csv'
            print(copy2 + " is newer")

        if not (len(copy) == len(masterArray) and len(other) == len(masterArray)):
            while len(copy) < len(masterArray) or len(copy) > len(masterArray):
                # if either copy is lesser or greater
                if len(copy) < len(masterArray):
                    print(
                        "The file " + filename + name + " contains less entries existing than the master file. . . Updating "
                                                        "master file with data found. . .")
                else:
                    print(
                        "Newer copy " + filename + name + " contains more entries existing than the master file. . . The file "
                                                          "could be outdated, or the master file was edited manually in the "
                                                          "middle of the creation of this file. . . Updating master file. . .")
                for i in range(len(copy)):
                    nameExists = 0
                    header = 0
                    for j in range(len(masterArray)):
                        if i == 0:
                            header = 1
                            continue
                        else:
                            if (masterArray[j][1] == copy[i][1] and masterArray[j][2] == copy[i][2]) and (
                                    masterArray[j][0] != copy[i][0]):
                                nameExists = 1
                                if not copy[i][0]:
                                    continue
                                masterArray[j][0] = copy[i][0]
                                print(
                                    "Entry " + copy[i][2] + " " + copy[i][
                                        3] + " exists. Changing RFID to one found in copy: " +
                                    copy[i][0])
                                continue
                            elif masterArray[j][1] == copy[i][1] and masterArray[j][2] == copy[i][2]:
                                nameExists = 1
                                continue
                    if nameExists == 0 and header == 0:
                        print("New entry for database: " + copy[i][2] + " " + copy[i][3] + " with RFID: " + copy[i][0])
                        masterArray.append(copy[i])
                copy = masterArray
                print(filename + '.csv has been successfully updated.')
                pd.DataFrame(masterArray).to_csv(path + os.sep + filename + ".csv", index=False, header=None,
                                                 encoding="utf-8")
                pd.DataFrame(copy).to_csv(path + os.sep + filename + name, index=False, header=None, encoding="utf-8")
                os.remove(path + os.sep + filename + name)
                temp = copy
                copy = other
                other = temp
                if name == '00000000944de39a.csv':
                    name = '00000000781547eb.csv'
                else:
                    name = '00000000944de39a.csv'
                print("Copy file has been removed.")

        elif len(copy) == len(masterArray) and len(other) == len(masterArray):
            while l >= 0:
                if masterArray[i][0]:
                    if masterArray[i][0] == copy1Array[i][0] and masterArray[i][0] == copy2Array[i][0]:
                        print("Retaining Value. Same data for all three files.")
                    else:
                        if not (copy1Array[i][0]) and not (copy2Array[i][0]):
                            pass
                        elif (copy1Array[i][0]) and not (copy2Array[i][0]):
                            print('Swapping ' + masterArray[i][0] + ' for ' + copy1Array[i][0])
                            masterArray[i][0] = copy1Array[i][0]
                        elif (copy2Array[i][0]) and not (copy1Array[i][0]):
                            print('Swapping ' + masterArray[i][0] + ' for ' + copy2Array[i][0])
                            masterArray[i][0] = copy2Array[i][0]
                        else:
                            if copy1mdate > copy2mdate:
                                print('Swapping ' + masterArray[i][0] + ' for ' + copy1Array[i][0])
                                masterArray[i][0] = copy1Array[i][0]
                            else:
                                print('Swapping ' + masterArray[i][0] + ' for ' + copy2Array[i][0])
                                masterArray[i][0] = copy2Array[i][0]
                    i = i + 1
                    l = l - 1
                else:
                    if not (copy1Array[i][0]) and not (copy2Array[i][0]):
                        pass
                    elif (copy1Array[i][0]) and not (copy2Array[i][0]):
                        print("New RFID entry for " + masterArray[i][2] + " " + masterArray[i][3] + ": " + copy1Array[i][0])
                        masterArray[i][0] = copy1Array[i][0]
                    elif (copy2Array[i][0]) and not (copy1Array[i][0]):
                        print("New RFID entry for " + masterArray[i][2] + " " + masterArray[i][3] + ": " + copy2Array[i][0])
                        masterArray[i][0] = copy2Array[i][0]
                    else:
                        if copy1mdate > copy2mdate:
                            print(
                                "New RFID entry for " + masterArray[i][2] + " " + masterArray[i][3] + ": " + copy1Array[i][
                                    0])
                            masterArray[i][0] = copy1Array[i][0]
                        else:
                            print(
                                "New RFID entry for " + masterArray[i][2] + " " + masterArray[i][3] + ": " + copy2Array[i][
                                    0])
                            masterArray[i][0] = copy2Array[i][0]
                    i = i + 1
                    l = l - 1

            print(filename + '.csv has been successfully updated.')
            pd.DataFrame(masterArray).to_csv(path + os.sep + filename + '.csv', index=False, header=None, encoding="utf-8")
            os.remove(path + os.sep + filename + '00000000944de39a.csv')
            os.remove(path + os.sep + filename + '00000000781547eb.csv')
            print("Copy files have been removed.")
    else:
        print("Program skipped. Either the master file, or the copy files do not exist.")
