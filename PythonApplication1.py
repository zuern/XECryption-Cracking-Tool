"""
This file is used to crack XEcryption encrypted documents.
Written by Kevin Zuern
Used for hackthissite.org realistic mission 6.

HOW TO USE:
        1. Create a file in the same directory as this script
        2. Call decryptFile('yourfilename') if you don't know the password
        3. Call decryptFile('yourfilename','passWord') if you know the pass.
        4. Follow the instructions.
"""

def sum(lis):
        total = 0
        for i in lis:
                total += i
        return total

def getASCIIsum(text):
    sum = 0
    for letter in text:
        sum += ord(letter)
    return sum

def collapseToIntegerSums(blocks):
    asInts = []
    for i in range(len(blocks)/3):
       asInts.append(sum(blocks[3*i:3*i+3]))                   # Sums each 3 number block into one int, and adds it to asInts
    return asInts

def findAbsoluteMin(encryptedFile):
    intList = []
    for line in encryptedFile:
        intList.append( collapseToIntegerSums(line) )
    minVal = intList[0][0]
    for lis in intList:
        for n in lis:
            minVal = min(n,minVal)
    return minVal

def isValidListofChars(lis):
    """Checks whether any of the 'characters' are not characters normally used in conversation"""
    totalrange = range(32,127)                              # a-z, A-Z 0-9
    totalrange.extend([10,17,0])                            # ' ', \n, ''

    for char in lis:
        if not char in totalrange:
            return False
    return True

def decryptLine(blocks, passwordValue=None):
    asInts = collapseToIntegerSums(blocks)
        
    # We know the password.
    if passwordValue != None:                           
        solutionSet = []

        for value in asInts:
            if value - passwordValue < 256:                        # I.e. is it a valid character?
                solutionSet.append(chr(value-passwordValue))        # Decrypt using password
        return ''.join(map(str,solutionSet))
    # We don't know the password.
    else:
       print "Can't decrypt without a password!"

def decryptFile(pathToFile, password=None):
    with open(pathToFile) as file:                                  # Open File at given path.
        encrypted = file.readlines()                                # Read File line by line

        # This loop normalizes the encrypted, removes whitespace, converts into list of integers
        for i in range(len(encrypted)):
            encrypted[i] = encrypted[i].strip('\t\n\r')
            encrypted[i] = map( int, filter( None,encrypted[i].split('.') ) )
        
        decryptedFile = []                                          # Will store the decrypted file.
        
        # We know the password!
        if password != None:
            for i in range(len(encrypted)):
                line = encrypted[i]
                decryptedFile.append(decryptLine(line,getASCIIsum(password)))   # Append decrypted line to the list
                print decryptedFile[i]                              # Print the decrypted text line by line.
        
        # Let's get cracking muhahahaha
        else:
            #################
            #     Steps:    #
            #################
            """
                1. Crack Password
                    a. Calculate maximum possible password value 'n'
                    b. Display first line of file decrypted with 0-n different passwords
                    c. User inputs line number of 'correct' decryption
                2. Decrypt whole file using user selected password value.
                3. Output to decrypted.txt
            """
            print "We don't know the password, so we'll show you a series of possible decryptions\nand output to 'possibilities.txt'"
            raw_input("Proceed?")

            # Okay let's calculate maximum possible password value...
            maxPossiblePassVal = findAbsoluteMin(encrypted)
            
            # Start Decrypting first line over and over until good all possibilities exhausted.
            firstLine = encrypted[0]
            possibilities = {}
            currentPasswordValue = 0

            print "Found range of possible passwords"
            import time
            time.sleep(2)
            print "Now cracking... (This can take a while)"

            while currentPasswordValue <= maxPossiblePassVal:
                message = decryptLine(firstLine,currentPasswordValue)
                if len(message) > 0:                                # We found a valid solution
                    possibilities[currentPasswordValue] = message   # Add it to the set.
                currentPasswordValue += 1

            print "Okay. We have done all possible decryptions."

            with open('possibilities.txt','w') as f:
                for passwordPossibility in possibilities:
                    f.write("{0}: {1}\n\n".format( passwordPossibility,possibilities[passwordPossibility] ) )
            print "Go to possibilities.txt, and find the correct decryption number.\n"
            password = int(raw_input("Enter the password number that makes the message legible..."))

            with open('decrypted.txt','w') as f:
                for line in encrypted:
                    f.write( decryptLine(line,password) )
            print 'You can read the file in "decrypted.txt"'
