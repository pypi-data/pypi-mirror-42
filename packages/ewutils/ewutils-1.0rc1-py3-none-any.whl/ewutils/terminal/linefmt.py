
## Printing with arrows ##
def arrowRight(*argv):
    '''
    Will print out to terminal using right arrows between each segment
    Example:
        arrowRight("hello", "world")
    
    Output:
        hello -> world
    '''
    line = ""
    for arg in argv:
        line += f"{arg} -> "
    line = line[:-4]
    print(line)

def arrowLeft(*argv):
    '''
    Will print out to terminal using left arrows between each segment
    Example:
        arrowLeft("hello", "world")
    
    Output:
        hello <- world
    '''
    line = ""
    for arg in argv:
        line += f"{arg} <- "
    line = line[:-4]
    print(line)

## Lines that stand out ##
class Urgency:
    Normal = 7
    Warning = 3
    Error = 1
    Success = 2

def inform(source:str, message:str, urgency=Urgency.Normal):
    '''
    Uses colour and square brackets to make messages stand out a bit more
    Example:
        inform("ewutils", "Foo", Urgency.Normal)
    Output:
        [ewutils] Foo
    '''
    print(f"[\u001b[3{urgency}m{source}\u001b[0m] {message}")