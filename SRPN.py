# declare global variables for the operands
operand1, operand2 = 0, 0

# declare main stack for calculator
stack = []

#define the list of 'random' numbers and the position in this list
randCounter = 0
randNums = [1804289383,846930886,1681692777,1714636915,1957747793,424238335,719885386,1649760492,596516649,1189641421,1025202362,1350490027,783368690,1102520059,2044897763,1967513926,1365180540,1540383426,304089172,1303455736,35005211,521595368]

#declare global variable to determine if the the calculator is in comment mode
commentMode = False

#declare global variable used for one line operations 
ongoingOperand = ""

#function that returns boolean stating if the stack is full or not
def isStackFull():
    #assume stack is not full
    isFull = False
    #stack is full if length is maximum 
    if len(stack) == 23:
        isFull = True
    #return boolean
    return isFull


#function that assigns the value of the last two elements on the stack to the operand variables
def popOps():
    #allow access to global operand variables
    global operand1
    global operand2
    #pop first operand from stack
    try:
        operand2 = stack.pop()
    except:
        #if stack is empty and operand cannot be popped off, return message to user and return false
        print("Stack underflow.")
        return False
    else:
        #if operand can be popped off of stack, try to pop second operand off stack 
        try:
            operand1 = stack.pop()
        except:
            #if stack is empty and operand cannot be popped off, return message to user, return first operand to stack and return false 
            print("Stack underflow.")
            stack.append(operand2)
            return False
        else:
            #if both operands can be popped off return true
            return True

#function that determines whether an input is an accepted operator 
def isOperator(test):
    #if inputted parameter matches one of the operators, return true value, otherwise, return false
    if test == "+":
        return True
    elif test == "-":
        return True
    elif test == "=":
        return True
    elif test == "/":
        return True
    elif test == "%":
        return True
    elif test == "*":
        return True
    elif test == "^":
        return True
    else:
        return False


#function that returns the value of a calculation accounting for saturation
def saturation(number):
    result = number
    #adjusts number if it is larger than saturation
    if result > 2147483647:
        result = 2147483647
    #adjusts number if it is smaller than saturation
    if result < -2147483648:
        result = -2147483648
    #returns adjusted value
    return result


#function that handles denary decimal inputs 
def numberInput(number):
    #tests if stack is full by calling previous function
    if isStackFull() == True:
        #tells user number cannot be added to stack
        print("Stack overflow.")
    else:
        #otherwise adds number as float variable type (converted from string) to stack
        stack.append(float(number))


#function that handles single letter alphabetic inputs
def charInput(char):
    #allows access to global variable that holds current position in list of random numbers
    global randCounter

    if char == "d":    
        #handles input to print stack
        if len(stack) == 0:
            #if stack is empty, print negative saturation
            print(-2147483648)
        else:
            #if stack is not empty, print each element on a new line
            for elements in stack:
                print(int(elements))
    elif char == "r":
        #handles input to add random number
        #add number from random list at position as determined by how many other random numbers have been called 
        numberInput(randNums[randCounter])
        #loops random list once all numbers have been used
        if randCounter < 21:
            randCounter += 1
        else:
            randCounter = 0


#function that handles operations using one or two operands and an operator
def operatorInput(operator):
    #allows access to global operand variables
    global operand1
    global operand2

    #resets variable to null
    result = None

    #performs calculation using given operator if a sufficient number of operands can be popped
    if operator == "+" and popOps():
        result = operand1 + operand2       
    elif operator == "-" and popOps():
        result = operand1 - operand2
    elif operator == "=":
        #tests if one operand can be popped from stack
        try:
            result = stack.pop()
        except:
            #if it cannot, inform user
            print("Stack empty.")
        else:
            #if it can, print integer version of result
            print(int(result))
    elif operator == "/" and popOps():
        if not operand2 == 0:
            result = operand1 / operand2
        else:
            print("Divide by 0.")
            stack.append(operand1)
            stack.append(operand2)
    elif operator == "%" and popOps():
        result = operand1 % operand2
    elif operator == "*" and popOps():
        result = operand1 * operand2
    elif operator == "^" and popOps():
        result = operand1 ^ operand2
    
    #if operation has been performed and result is not null, apply saturation function to result to ensure it is within bounds and add the result to the stack
    if not result == None:
        result = saturation(result)
        stack.append(result)


#function that handles numbers with a single line input
def resetOngoingOperand():
    #allows access to global variable
    global ongoingOperand
    if ongoingOperand != "":
        #if variable is not empty, pass it to main sorting function to be added to stack     
        sort(ongoingOperand)
    #reset value to nothing
    ongoingOperand = ""


#function that handles one line inputs
def oneLineInput(line):
    #allows access to necessary global variables
    global commentMode
    global ongoingOperand
  
    #declares count as negative one
    count = -1
    for character in line:
        #increase count to arrive at starting position of line and increase on each loop
        count +=1
        #determines what to do with input, only processes if comment mode is disabled
        if character == "d" and not commentMode:
            #adds any previously typed numbers to the stack as a finished operand
            resetOngoingOperand()
            #passes the single input to the the main sorting function
            sort(character)
        elif character == " " and not commentMode:
            #ignores spaces
            resetOngoingOperand()
        elif character == "r" and not commentMode:
            resetOngoingOperand()
            sort(character)        
        elif character == "#":
            resetOngoingOperand()
            sort(character)
        elif character.isdigit() or (character == "-" and line(count+1).isdigit()) and not commentMode:
            #handles both positive and negative numbers
            ongoingOperand += character
        elif isOperator(character) and not commentMode:
            resetOngoingOperand()
            operatorInput(character)
        elif not commentMode:
            #handles unrecognised inputs while not in comment mode
            resetOngoingOperand()
            print("Unrecognised operator or operand \"", character, "\".")
        else:
            commentMode = commentMode
    resetOngoingOperand()

            #if input is unrecognised but calculator is in comment mode, it will be ignored.
   

#function that allows for octal conversion to denary
def octalInput(octal):
    #attempt octal conversion 
    try:
        decimal = int(octal,8)
    except:
        #if fails, number is not a valid octal and it is not added to the stack 
        invalidOctal = True
    else:
        #if passes, number is a valid octal and denary conversion is done, passes denary number to be added to the stack
        numberInput(decimal)
        

#function to determine the type of input inputted by the user
def sort(userIn):
    #allow access to global variable
    global commentMode

    #determines if the input is a positive or a negative octal and calls function if comment mode not enabled
    if (userIn.startswith('0') or userIn.startswith('-0')) and len(userIn) > 2 and not commentMode and not "." in userIn:
        octalInput(userIn)
    #determines if the input is a single character and calls appropriate function if comment mode is not enabled
    elif (len(userIn) == 1) and (userIn.isalpha()) and not commentMode:
        charInput(userIn)
    #determines if the input is a operator by calling a function and then calls another function if comment mode is not enabled
    elif (len(userIn) == 1) and isOperator(userIn) and not commentMode:
        operatorInput(userIn)
    #determines if the input is a positive or negative integer
    elif (userIn.isdigit() or (userIn*-1).isdigit()) and not commentMode and not "." in userIn:
        numberInput(userIn)
    #determines if the input is indicating a comment, toggle comment mode
    elif userIn == "#":
        commentMode = not commentMode
    #if unrecognised, is passed to function to run through each item in line separately
    else:
        oneLineInput(userIn)
    
#the inital starting function
def main():
    # ongoing program loop continuously takes user input
    while True:
        userIn = input()
        #passes input to function to determine type of input
        sort(userIn)

#user prompt            
print("You can now start interacting with the SRPN calculator")
#call initial function
main()
