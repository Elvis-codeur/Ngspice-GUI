import re
import numpy 
class ProcessRaw():
    def __init__(self,file_name=""):
        self.file_name = file_name
        self.args = {}
        self.datas = []
        self.info = {}
        
        #Reading the file
        f = open(self.file_name,"r")
        self.text = f.read()

        # Splitting the text
        self.info_text,self.data_text = self.text.split("Values:")
        
        a,k = self.info_text.split("Variables:\n\t")

        a = a.split("\n")

        # Getting the simulation informations
        for i in a:
            ml = i.split(":")
            if(len(ml)>1):
                self.info[ml[0]] = ml[1][1:]

        # Getting the labels of the results
        k = k.split("\n")
        self.labels = []
        for i in k:
            u = i.split("\t")
            if(len(u)> 1):
                self.labels.append(u[1:])

        self.nb_variable = len(self.labels)

        # Preparing the datas
        if(self.info["Plotname"] == "Transient Analysis"):
            self.tran_process()
            self.create_args()
        elif(self.info["Plotname"] == "AC Analysis"):
            self.ac_process()

    

    def create_args(self):
        for i in range(len(self.labels)):
            self.args[self.labels[i][1]] = self.datas[i]
            
    def ac_process(self):
        # Use of a regex to find the numbers that begin a new set of datas
        result = list(re.finditer("([ ]){1}[0-9]*([	]){1}",self.data_text))
        self.datas = [[[],[]] for i in range(self.nb_variable)]

        for i in range(1,len(result)):
            a = result[i].span() 
            b = result[i-1].span()
            values = self.data_text[b[1]:a[0]].split("\n")
   
            for u in range(len(values)):
                if(values[u]):
                    k = values[u].split(",")
                    self.datas[u][0].append(float(k[0]))
                    self.datas[u][1].append(float(k[1]))



    def tran_process(self):
        # Use of a regex to find the numbers that begin a new set of datas
        result = list(re.finditer("([ ]){1}[0-9]*([	]){1}",self.data_text))
        self.datas = [[] for i in range(self.nb_variable)]

        for i in range(1,len(result)):
            a = result[i].span() 
            b = result[i-1].span() 
            # Get the different values
            values = self.data_text[b[1]:a[0]].split("\n")

            # Adding each value to the correspondent list
            for u in range(len(values)):
                if(values[u]):
                    self.datas[u].append(float(values[u]))


def plot(all = False,**kwarg):
    if(all):
        a = ProcessRaw("ca.raw")
        jkl = a.args
        print(jkl.keys())
        import matplotlib.pyplot as plt 
    
        for i in jkl.keys():
            plt.plot(jkl["time"],jkl[i],label = i)

        plt.legend()
        plt.show() 

    else:
        a = ProcessRaw("cc.raw")
        jkl = a.args
        print(jkl.keys())
        import matplotlib.pyplot as plt 
    
        #plt.plot(jkl["time"],jkl["v(1)"],label = "v(1)")
        #plt.plot(jkl["time"],jkl["v(3)"],label = "v(3)")
        plt.plot(jkl["time"],jkl["i(l1)"],label = "i(l1)")

        plt.legend()
        plt.show() 
if __name__ == "__main__":
     plot(True)  
