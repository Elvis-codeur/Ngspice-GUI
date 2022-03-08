
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

    def simulate_netlist(self,netlist,commande):
        initialize_ngspice()
        circ(netlist)
        if(issubclass(type(commande),str)):
            cmd("{}".format(commande))
        elif issubclass(type(commande),list):
            for i in commande:
                cmd("{}".format(i))

        return self.get_simulation_datas()


    def simulate_file(self,file_name,commande):

        initialize_ngspice()
        if commande:
            cmd("source '{}'".format(file_name))

            if(issubclass(type(commande),str)):
                cmd("{}".format(commande))
            elif issubclass(type(commande),list):
                for i in commande:
                    cmd("{}".format(i))

            #print("\n\n\n",file_name,"\n\n\n")
        else:
            cmd("source '{}'".format(file_name))
            #print("\n\n\n",file_name,"\n\n\n")

        return self.get_simulation_datas()

    def get_simulation_datas(self):
        result = {}
        # Contain ["tran1","const"]
        plot = plots()
        #print("plots = ",plot)
        #print(vector_names("dc1"))

        compteur = False
        for i in plot:
            if "const" not in i:
                vec_names = vector_names(i)
            
                p = {}
                for k in vec_names:
                    p[k] = vector(k)

                result[i] = p
                """
                if("time" in vec_names and not compteur):
                    result["time"] = vector("time")
                    compteur = True
                elif "v-sweep" in vec_names and not compteur:
                    result["v-sweep"] = vector("v-sweep")
                """
        #print("\n\n\n",result,"\n\n\n")
        return result
    

if __name__ == "__main__":
    sim = NgspiceSimulator()
    print(sim.simulate("sim2.cir"))



