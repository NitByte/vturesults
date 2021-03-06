from django.shortcuts import HttpResponse,render
import json
import random

def index(request):
    return render(request,"index.html")

def api(request):
    return render(request,"apipage.html")

def stats(request):
    return render(request,"statspage.html")

def search(request):
    return render(request,"search.html")

def home(request):
    return render(request,"home.html")

def class_results(request,branch):
    year=request.GET["year"]
    print(year)
    with open("templates/new20"+year+"batch.json","r") as fp:
        res=json.load(fp)
    if branch=='all':
        return render(request,'table.html',{'results':res,'all':'True'})
    else:
        return render(request,'table.html',{'results':res[branch],'all':'False'})

def result(request,usn):
    year=usn[3:5]
    try:
        with open("templates/new20"+year+"batch.json","r") as fp:
            res=json.load(fp)
        
        branch=usn[5:7]
        usn_dict=res[branch][usn]
        sub_dict={}
        for sub in res[branch][usn]["Subjects"]:
            sub_dict[sub]={}
            for key,value in res[branch][usn]["Subjects"][sub].items():
                key=key.replace(" ","")
                sub_dict[sub][key]=value
        usn_dict["Subjects"]=sub_dict
        return render(request,'result.html',{'results':usn_dict})
    except:
        return render(request,'error.html')

def hello_world(request):
    return HttpResponse("Hello World")

def root_page(request):
    return HttpResponse("Welcome")


def random_number(request,max_rand=100):
    random_num=random.randrange(0,int(max_rand))
    msg="Random number between 0 and "+max_rand+" is "+str(random_num)
    return HttpResponse(msg)

def json_display(request):
    year=request.GET["year"]
    return render(request,"new20"+year+"batch.json")

def display_reval(request,usn):
    year=usn[3:5]
    with open("templates/reval20"+year+"batch.json","r") as fp:
        reval=json.load(fp)
    try:
        branch=usn[5:7]
        usn_dict=reval[branch][usn]
        sub_dict={}
        for sub in reval[branch][usn]["Subjects"]:
            sub_dict[sub]={}
            for key,value in reval[branch][usn]["Subjects"][sub].items():
                key=key.replace(" ","")
                sub_dict[sub][key]=value
                try:
                    sub_dict[sub]["Oldresult"]=res[branch][usn]["Subjects"][sub]["Result"]
                except:
                    sub_dict[sub]["Oldresult"]="-"
        usn_dict["Subjects"]=sub_dict
        return render(request,'revalresult.html',{'results':usn_dict,'usn':str(usn)})
    except:
        return render(request,'error.html')

def display_allreval(request,branch):
    year=request.GET["year"]
    with open("templates/new20"+year+"batch.json","r") as fp:
        response=json.load(fp)
    with open("templates/reval20"+year+"batch.json","r") as fp:
        reval=json.load(fp)
    usns=[] 
    for b in response:
        for usn in reval[b]:
            response[b][usn]["IncrementCGPA"]='%.2f'%(float(response[b][usn]['CGPA'])-float(response[b][usn]['OldSGPA']))
    if branch=='all':
        for b in reval:
            for usn in reval[b]:
                usns.append(usn)
        return render(request,'allreval.html',{'results':response,'all':'True','usnlist':usns})
    else:
        for usn in reval[branch]:
            usns.append(usn)
        return render(request,'allreval.html',{'results':response[branch],'all':'False','usnlist':usns})

def after_reval(request,usn):
    year=usn[3:5]
    try:
        with open("templates/new20"+year+"batch.json","r") as fp:
            res=json.load(fp)
        branch=usn[5:7]
        usn_dict=res[branch][usn]
        sub_dict={}
        for sub in res[branch][usn]["Subjects"]:
            sub_dict[sub]={}
            for key,value in res[branch][usn]["Subjects"][sub].items():
                key=key.replace(" ","")
                sub_dict[sub][key]=value
        usn_dict["Subjects"]=sub_dict
        return render(request,'afterreval.html',{'results':usn_dict})
    except:
        return render(request,'error.html')




