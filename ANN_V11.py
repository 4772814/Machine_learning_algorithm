import csv
import datetime
import pickle
import math
import copy
import random
from operator import itemgetter, attrgetter, methodcaller

def read2lst(fname):
    lineN=0
    readlst=[]
      
    fopen=open(fname,"r")

    while(True):
        tmpline=fopen.readline()
        tmpline=tmpline.replace("\n","")
        tmpline=tmpline.replace("\r","")
        if not tmpline:break
        
        lineN=lineN+1
        if lineN==1:continue
        #print(tmpline)
        tmplinelst=tmpline.split(",")
        readlst.append(tmplinelst)
        

    print("Var:********,Target,DlpTest,Weight")
    print("Totline:",lineN)
    #print("readlst[0:10]:",readlst[0:10])

    return(copy.deepcopy(readlst))


Rawlst=read2lst("D:/download/Doc/Python_A/MFILE.TXT")

Rawlstdic=[{"TranID":x[0] 
       ,"ACT_0_1" :float(x[1]) ,"ACT_0_2":float(x[2])  ,"ACT_0_3":float(x[3])  ,"ACT_0_4":float(x[4])  ,"ACT_0_5":float(x[5]) 
       ,"ACT_0_6" :float(x[6]) ,"ACT_0_7":float(x[7])  ,"ACT_0_8":float(x[8])  ,"ACT_0_9":float(x[9])  ,"ACT_0_10":float(x[10]) 
       ,"ACT_0_11":float(x[11]),"ACT_0_12":float(x[12]),"ACT_0_13":float(x[13]),"ACT_0_14":float(x[14]),"ACT_0_15":float(x[15]) 
       ,"ACT_0_16":float(x[16]),"ACT_0_17":float(x[17]),"ACT_0_18":float(x[18]),"ACT_0_19":float(x[19]),"ACT_0_20":float(x[20]) 
       ,"ACT_0_21":float(x[21]),"ACT_0_22":float(x[22]),"ACT_0_23":float(x[23]),"ACT_0_24":float(x[24]),"ACT_0_25":float(x[25]) 
       ,"ACT_0_26":float(x[26]),"ACT_0_27":float(x[27]),"ACT_0_28":float(x[28]),"ACT_0_29":float(x[29]),"ACT_0_30":float(x[30]) 
       ,"ACT_0_31":float(x[31]),"ACT_0_32":float(x[32]),"ACT_0_33":float(x[33]),"ACT_0_34":float(x[34]),"ACT_0_35":float(x[35]) 
            
       ,"TARGET_1":float(x[36]),"TARGET_2":float(x[37])
       ,"DlpTest":x[38],"FREQ_WGT":float(x[39])}
        for x in Rawlst]

print("Rawlstdic#################################################")
print("Length of Rawlstdic:",len(Rawlstdic))
print(Rawlstdic[:10])



##################################################################
def Srange(x):
    trange=list(range(x+1))[1:]
    return(trange[:])

def ACTSLT(VAR,FUNC,D):
    if D=="N":
        if FUNC=="LOGSIG":FRLT=(1/(1+math.exp(min(-VAR,100))))
        elif FUNC=="TANSIG":FRLT=(2/(1+math.exp(min(-2*VAR,100)))-1)

    elif D=="Y":
        if FUNC=="LOGSIG":FRLT=(1)*(math.exp(min(-VAR,100))/((1+math.exp(min(-VAR,100)))**2))
        elif FUNC=="TANSIG":FRLT=(1)*(4*math.exp(min(-2*VAR,100))/((1+math.exp(min(-2*VAR,100)))**2))       
    return(FRLT)


class NNode(object):
    def __init__(self):
        self.Father=[]
        self.WGT={}
        self.NodeOrder=-100
        self.Child=[]
        self.COMB=0
        self.ACTFUNC="TANSIG"
        self.ACT=0
        self.D=0
        

class Network(object):

    def __init__(self):
        self.NetNode={}
        self.InputMap={}

        self.OutputMap={}
     

    def addNode(self,NodeOrder,NumNode,Father=None):       
        for ti in Srange(NumNode):
            self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)]=NNode()
            self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].NodeOrder=NodeOrder

           
            if NodeOrder>0:
                tmpFather=list(Father)
                tmpFather.append("ACT_" +str(NodeOrder)+"_"+str(ti)+"_Intercept")
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].Father=copy.deepcopy(tmpFather)
                
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)+"_Intercept"]=NNode()
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)+"_Intercept"].ACT=1
                
                
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].WGT           =dict.fromkeys(self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].Father)
                
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].PARTIAL_P0_WGT=dict.fromkeys(self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].Father,0)
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].DETAX_WGT     =dict.fromkeys(self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].Father,0)
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].CUM_RO        =0
                self.NetNode["ACT_" +str(NodeOrder)+"_"+str(ti)].COMB          =0

                

    def addTargetNode(self,NumNode,HNodeToTargetNodeMap):
        for ti in Srange(NumNode):
            self.NetNode["TARGET_"+str(ti)]=NNode()
            self.NetNode["TARGET_"+str(ti)].NodeOrder=-1

        self.HNodeToTargetNodeMap=copy.deepcopy(HNodeToTargetNodeMap)

        
    def collChildNode(self):

        HNodeName=[x for x in self.NetNode if self.NetNode[x].NodeOrder>0]

        for tmpnodekey in HNodeName:
            tmpnodevalue=self.NetNode[tmpnodekey]
            tmpnodevalue.Child=[x for x in HNodeName if  tmpnodekey in self.NetNode[x].Father]
            

        self.HNodeName=copy.deepcopy(HNodeName)
        self.HNodeNameOrderLst=sorted(set([self.NetNode[x].NodeOrder for x in self.HNodeName]))

        self.HNodeNameOrderLst_R=sorted(self.HNodeNameOrderLst,reverse=True)

        self.InputNodes=[x for x in self.NetNode if self.NetNode[x].NodeOrder==0 ]

        self.OrderList={}
        for tmporder in self.HNodeNameOrderLst:
            self.OrderList[tmporder]=copy.deepcopy([x for x in self.NetNode if self.NetNode[x].NodeOrder==tmporder])

        self.TargetNodes=[x for x in self.NetNode if x in self.HNodeToTargetNodeMap]

                
    def initWeight(self):
        for tmpnodekey in self.HNodeName:            
            for tmpwgt in self.NetNode[tmpnodekey].Father:
                self.NetNode[tmpnodekey].WGT[tmpwgt]           =random.uniform(-1,1)
                self.NetNode[tmpnodekey].PARTIAL_P0_WGT[tmpwgt]=0
                self.NetNode[tmpnodekey].DETAX_WGT[tmpwgt]     =0

            self.NetNode[tmpnodekey].CUM_RO=0
            
        
    def NNTraining(self,DlplstDic,TMAXLOOPN=30):
        
        WGTSEED=12
        MINERROR=0.001
        ETA=0.001
        MAXLOOPN=TMAXLOOPN
        LAM=0
        BETA=0
        SPARM=0.5
        ALPHA=0.7

        random.seed(WGTSEED)
        NWDATA_MODEL=[]
        
        for tmpvi in DlplstDic:
            tmpvix=copy.deepcopy(tmpvi)
            if tmpvix["DlpTest"]=="D":
                trandom=random.random()
                tmpvix["DT"]="DA"
                tmpvix["TMPRANUNI"]=trandom
                NWDATA_MODEL.append(copy.deepcopy(tmpvix))
                
                tmpvix["DT"]="DP"
                tmpvix["TMPRANUNI"]=trandom
                NWDATA_MODEL.append(copy.deepcopy(tmpvix))
                
                tmpvix["DT"]="DV"
                tmpvix["TMPRANUNI"]=trandom
                NWDATA_MODEL.append(copy.deepcopy(tmpvix))
            else:
                tmpvix["DT"]="TV"
                trandom=random.random()
                tmpvix["TMPRANUNI"]=trandom
                NWDATA_MODEL.append(copy.deepcopy(tmpvix))
    
        NWDATA_MODEL=sorted(copy.deepcopy(NWDATA_MODEL), key=itemgetter("DT","TMPRANUNI"), reverse=False)
        len_NWDATA_MODEL=len(NWDATA_MODEL)

        
        
    
        print("NWDATA_MODEL##########################")            
        
    
        print("Number of DA :",len([x for x in NWDATA_MODEL if x["DT"]=="DA"]))
        print("Number of DP :",len([x for x in NWDATA_MODEL if x["DT"]=="DP"]))
        print("Number of DV :",len([x for x in NWDATA_MODEL if x["DT"]=="DV"]))
        print("Number of TV :",len([x for x in NWDATA_MODEL if x["DT"]=="TV"]))
        
        #End Prepare the data,add DT,TMPRANUNI and random sort

        #Start Training
        Data_NWDATA_MODEL=copy.deepcopy(NWDATA_MODEL)
    
        DLP_ALLERROR     =9999999999     ;DLP_AVGERROR =9999999999
        TEST_ALLERROR    =9999999999     ;TEST_AVGERROR=9999999999
        LAST_DLP_AVGERROR=9999999999
        
        DOBS=0;    TOBS=0
    
        L_T_AE=[9999999999]*9


            
        LOOPN=0
        ALLWGT=[]

        while( not (DLP_AVGERROR<MINERROR or LOOPN>=MAXLOOPN   )):
        
            LOOPN=LOOPN+1
            
            DLP_ALLERROR =0;TEST_ALLERROR=0
            DOBS=0         ;TOBS=0
            

            N_DA=0

            for tmpnodekey in self.HNodeName:
                self.NetNode[tmpnodekey].CUM_RO=0

            #Read record one by one START
            for Dataloop in Data_NWDATA_MODEL:
                
                #Set Inputnode act 
                for tmpnodekey in self.InputNodes:
                    self.NetNode[tmpnodekey].ACT=Dataloop[tmpnodekey]
                    
                    
                #Set Onputnode act 
                for tmpnodekey in self.HNodeToTargetNodeMap.values():
                    self.NetNode[tmpnodekey].ACT=Dataloop[tmpnodekey]

                

                for tmporder in self.HNodeNameOrderLst:
                    for tmpnodekey in self.OrderList[tmporder]:
                        tmpnode=self.NetNode[tmpnodekey]

                        tmpnode.COMB=sum([tmpnode.WGT[x]*self.NetNode[x].ACT for x in tmpnode.Father])
                        tmpnode.ACT=ACTSLT(tmpnode.COMB,tmpnode.ACTFUNC,"N")

                if Dataloop["DT"]=="DA":
                    
                    N_DA=N_DA+1*Dataloop["FREQ_WGT"]

                    for tmporder in self.HNodeNameOrderLst:
                        for tmpnodekey in self.OrderList[tmporder]:
                            self.NetNode[tmpnodekey].CUM_RO=self.NetNode[tmpnodekey].CUM_RO+self.NetNode[tmpnodekey].ACT
                    
                    DA=0
                    
                #Start DP
                elif Dataloop["DT"]=="DP":
                    if DA==0:#Calc Avg of Ro at  first time of DP
                        DA=1
                        
                        for tmporder in self.HNodeNameOrderLst:
                            for tmpnodekey in self.OrderList[tmporder]:

                                self.NetNode[tmpnodekey].AVG_RO=self.NetNode[tmpnodekey].CUM_RO/N_DA
                                
                                if    -0.000001<=self.NetNode[tmpnodekey].AVG_RO<=0.000001 \
                                   or -0.000001<=(1-self.NetNode[tmpnodekey].AVG_RO)<=0.000001:self.NetNode[tmpnodekey].STERM=0;
                                else:self.NetNode[tmpnodekey].STERM=BETA*sum([-SPARM/self.NetNode[tmpnodekey].AVG_RO,(1-SPARM)/(1-self.NetNode[tmpnodekey].AVG_RO)])
                        


                    
                    for tmporder in self.HNodeNameOrderLst_R:
                        for tmpnodekey in self.OrderList[tmporder]:
                            tmpnode=self.NetNode[tmpnodekey]
                            
                            if tmpnodekey in [x for x in self.HNodeToTargetNodeMap]:    
                                tmp_SUM=-(self.NetNode[self.HNodeToTargetNodeMap[tmpnodekey]].ACT-tmpnode.ACT)
                            else:
                                tmp_SUM=sum([self.NetNode[x].D*self.NetNode[x].WGT[tmpnodekey]  for x in tmpnode.Child])

                                
                                tmp_SUM=tmp_SUM+tmpnode.STERM
                                
                                
                            tmpnode.D=ACTSLT(tmpnode.COMB,tmpnode.ACTFUNC,"Y")*tmp_SUM

                            for tmpw in tmpnode.Father:
                                tmpnode.PARTIAL_P0_WGT[tmpw]=tmpnode.D*self.NetNode[tmpw].ACT



                    for tmporder in self.HNodeNameOrderLst_R:
                        for tmpnodekey in self.OrderList[tmporder]:
                            tmpnode=self.NetNode[tmpnodekey]

                            for tmpw in tmpnode.Father:
                                tmpnode.WGT[tmpw]=tmpnode.WGT[tmpw] \
                                                       +(-ETA*(tmpnode.PARTIAL_P0_WGT[tmpw]+LAM*tmpnode.WGT[tmpw]) +ALPHA*tmpnode.DETAX_WGT[tmpw])*Dataloop["FREQ_WGT"]

                                tmpnode.DETAX_WGT[tmpw]=(-ETA*(tmpnode.PARTIAL_P0_WGT[tmpw]+LAM*tmpnode.WGT[tmpw]) +ALPHA*tmpnode.DETAX_WGT[tmpw])

                                
                #End DP

                elif Dataloop["DT"]=="DV":
                    DOBS=DOBS+1*Dataloop["FREQ_WGT"];

                    TMPERR=0
                    for tmpoutnodekey in self.TargetNodes: 
                        TMPERR=TMPERR+(self.NetNode[tmpoutnodekey].ACT- self.NetNode[self.HNodeToTargetNodeMap[tmpoutnodekey]].ACT)**2
                        
                    DLP_ALLERROR=DLP_ALLERROR+TMPERR*Dataloop["FREQ_WGT"];
                        

                elif Dataloop["DT"]=="TV":
                    TOBS=TOBS+1*Dataloop["FREQ_WGT"];

                    TMPERR=0
                    for tmpoutnodekey in self.TargetNodes: 
                        TMPERR=TMPERR+(self.NetNode[tmpoutnodekey].ACT- self.NetNode[self.HNodeToTargetNodeMap[tmpoutnodekey]].ACT)**2
                        
                    TEST_ALLERROR=TEST_ALLERROR+TMPERR*Dataloop["FREQ_WGT"];

            DLP_AVGERROR = (DLP_ALLERROR /DOBS)/ len(self.HNodeToTargetNodeMap)
            TEST_AVGERROR= (TEST_ALLERROR/TOBS)/ len(self.HNodeToTargetNodeMap)

            print("LOOPN:",LOOPN,"======>DLP_AVGERROR:",DLP_AVGERROR,"TEST_AVGERROR:",TEST_AVGERROR,">>ETA:",ETA)
            if   DLP_AVGERROR<LAST_DLP_AVGERROR :   ETA=min(ETA*1.2,0.1);
            elif DLP_AVGERROR>LAST_DLP_AVGERROR :   ETA=max(ETA*0.8,0.00001);
            LAST_DLP_AVGERROR=DLP_AVGERROR;
            

            for _TPI in range(len(L_T_AE)-1,0,-1):                                                   
                L_T_AE[_TPI]=L_T_AE[_TPI-1]                                                          
            L_T_AE[0]=TEST_AVGERROR;                                                                 
                                                                                                     
            ALLWGT.append(copy.deepcopy([self.NetNode,TEST_AVGERROR,LOOPN]))
                                                                                                     
            if min(L_T_AE[0:6])>L_T_AE[6]:break
            
        _WGT_RLT=sorted(ALLWGT,key=itemgetter(1))
        
        self.WGT_RLT=_WGT_RLT[0]


    def NNScoring(self,scoredata):
        tmpscoredata=copy.deepcopy(scoredata)
        tmprltNetNode=self.WGT_RLT[0]

        for Dataloop in tmpscoredata:
            for tmpnodekey in self.InputNodes:
                self.NetNode[tmpnodekey].ACT=Dataloop[tmpnodekey]

            
            for tmporder in self.HNodeNameOrderLst:
                for tmpnodekey in self.OrderList[tmporder]:
                    tmpnode=self.NetNode[tmpnodekey]

                    tmpnode.COMB=sum([tmprltNetNode[tmpnodekey].WGT[x]*self.NetNode[x].ACT for x in tmpnode.Father])
                    tmpnode.ACT=ACTSLT(tmpnode.COMB,tmpnode.ACTFUNC,"N")

            for tmpnodekey in self.HNodeToTargetNodeMap:
                Dataloop.update({"P"+self.HNodeToTargetNodeMap[tmpnodekey]:self.NetNode[tmpnodekey].ACT})


        return(copy.deepcopy(tmpscoredata))


          
        
print("#Start Debug Network###########################################")
tmpNetwork=Network()

tmpNetwork.addNode(0,35)
                                     
tmpNetwork.addNode(1,17,Father=["ACT_0_"+str(x) for x in Srange(35)])
tmpNetwork.addNode(2,10,Father=["ACT_1_"+str(x) for x in Srange(17)])
tmpNetwork.addNode(3,2 ,Father=["ACT_2_"+str(x) for x in Srange(10)])
tmpNetwork.NetNode["ACT_3_1"].ACTFUNC="LOGSIG"
tmpNetwork.NetNode["ACT_3_2"].ACTFUNC="LOGSIG"

tmpNetwork.addTargetNode(2,HNodeToTargetNodeMap={"ACT_3_1":"TARGET_1","ACT_3_2":"TARGET_2"})
tmpNetwork.collChildNode()
tmpNetwork.initWeight()

if __name__=="__main__":
    tmpNetwork.NNTraining(Rawlstdic)

    tmpNetwork.NNScoring(Rawlstdic)

    
print("#End Debug Network###########################################")
