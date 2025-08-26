import main


class Keyword:
    def __init__(self, name, description, alternatives,function):
        self.name = name
        self.description = description
        self.alternatives = alternatives
        self.function = function
    
    def compare(self,value):
        return value.lower() == self.name or value.lower() in self.alternatives
    
    def __str__(self):
        return f"{self.name} : {self.description} - Alternatives : [{", ".join(self.alternatives)}]"

    def run(self):
        self.function()
    
def help_cmd():
    print("Commands : ")
    print("")
    for i in keywords:
        print(i)



keywords = [
    Keyword("help","Provides A List Of All Commands",["?"],help_cmd),
    Keyword("end","Ends the Engine",["close"],lambda:exit(0)),
    Keyword("run","Runs The Code",["start","begin"],main.run)
]


def check(inputted):
    for keyword in keywords:
        if keyword.compare(inputted):
            keyword.run()

