
from .shared_ngspice import *

class NgspiceSimulator():
    def __init__(self) -> None:
        self.netlist_filename = ""
        self.raw_filename = ""
        self.init()

    def set_netlist_filename(self,filename):
        self.netlist_filename = filename

    def set_raw_file_name(self,filename):
        self.raw_filename = filename

    def init(self):
        """To initialize ngspice """
        initialize_ngspice()

    def circ(self,file_name):
        circ(file_name)

    def simulate(self,file_name,commande = ""):

        initialize_ngspice()
        result = {}
        if commande:
            cmd("source '{}'".format(file_name))
            cmd("{}".format(commande))
            #print("\n\n\n",file_name,"\n\n\n")
        else:
            cmd("source '{}'".format(file_name))
            #print("\n\n\n",file_name,"\n\n\n")

        # Contain ["tran1","const"]
        plot = plots()
        #print(plot)
        #print(vector_names("tran1"))

        for i in plot:
            if "tran" in i:
                vec_names = vector_names(i)
                p = {}
                for k in vec_names:
                    p[k] = vector(k)

                result[i] = p

        #result["time"] = vector("time")

        return result
    

if __name__ == "__main__":
    sim = NgspiceSimulator()
    print(sim.simulate("sim2.cir"))



