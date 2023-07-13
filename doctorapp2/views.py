from django.shortcuts import render,redirect, HttpResponse
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from doctorapp.models import consultation,user_reg,states,department,hospitallist,                  doctor_availability
import datetime,time
from django.urls import reverse
from django.db.models import Q
from.import views
import json

from json import dumps
from django.http import JsonResponse
# Create your views here.
#def doctor(request):
    
   # return render(request,'doctorlogin.html')

def patientdetails(request):
    if request.method == 'POST':
        uname=request.POST['pname']
        patientpwd=request.POST['pwd']
        
        
        if(uname=="" or patientpwd==""):
            msg="Invalid Credentials"
            return render(request,'patientlogin.html',{'loginmsg':msg})
        if user_reg.objects.filter(Q(username=uname) & Q(usertype='P')):
            print("Valid User")
            patient=user_reg.objects.filter(username=uname)
            pid=patient[0].id
            pname=patient[0].fname
            #return render(request,'patient_details.html',{'patientdata':pid,'pname':pname})
            return render(request,'patient_details.html',{'pid':pid,'pname':pname})
        else:
            sec_msg= "Invalid Credentials"
            return render(request,'patientlogin.html',{'invalidmsg':sec_msg})
def doctordetails(request):
    
    if request.method == 'POST':
        dname=request.POST['dname']
        doctorpwd=request.POST['dpwd']
        if(dname=="" or doctorpwd==""):
            msg="Invalid Credentials"
            return render(request,'doctorlogin.html',{'loginmsg':msg})
        if user_reg.objects.filter(Q(username=dname) & Q(usertype='D')):
            print("Valid User")
            doctor=user_reg.objects.filter(username=dname)
            did=doctor[0].id
            
            return render(request,'doctor_details.html',{'docid':did})
        else:
            sec_msg= "Invalid Credentials"
            return render(request,'doctorlogin.html',{'invalidmsg':sec_msg})
        
    
    
def consulting(request):
    
    patientid = request.GET['patientid']
    #print("Patientid:",pid)
    #patientobj=doctor_availability.objects.all()
    
    hosptobj= hospitallist.objects.all()
    deptobj=department.objects.all()
    """for doctor in patientobj:
        val=hospitallist.objects.values_list('hosptname',flat=True).filter(id=doctor.hospitalid_id).distinct('hosptname')
        
        newval=val.values()[0]
        doctor.hospital=newval['hosptname']
        deptval=department.objects.filter(id=doctor.deptid_id).values()
        
        deptname=deptval.values()[0]
        doctor.deptname=deptname['deptname']
        docid=user_reg.objects.filter(id=doctor.doctorid_id).values()
        
        doctorname=docid.values()[0]
        doctor.doctorname=doctorname['fname']"""
      
    return render(request,'consultation.html',{'hosptdata':hosptobj,'deptdata':deptobj,'pid':patientid})
def doctoravail(request):
    doctorid=request.GET['doctorid']
    deptobjd= department.objects.all()
    hosptobjd = hospitallist.objects.all()
    return render(request,'doctor_availability.html',{'hosptdatad':hosptobjd,'deptdatad':deptobjd,'docid':doctorid})
def doctorschedule(request):
    if request.method=='GET':
        docid=request.GET['doctorid']
        scheduleobj=consultation.objects.filter(doctorid=docid)
        countval=len(scheduleobj)
        print("countval :", countval)
        for eachdoctor in scheduleobj:
            hosptval=hospitallist.objects.filter(id=eachdoctor.hospitalid_id).values()
            patientval=user_reg.objects.filter(id=eachdoctor.patientid).values()
            patientname=patientval.values()[0]
            eachdoctor.patient=patientname['fname']
            newval=hosptval.values()[0]
            eachdoctor.hospital=newval['hosptname']
        return render(request,'doctor_schedule.html',{'docid':docid,'schedule':scheduleobj})
        
    
    
    
    
def availsave(request):
    
    if request.method == 'POST':
        doctid=request.POST['docid']
        
        did=user_reg.objects.get(id=doctid)
        
        hosptname=request.POST['hospitals']
        deptname=request.POST['department']
        hostid=hospitallist.objects.get(id=hosptname)
        deptid=department.objects.get(id=deptname)
        now=datetime.datetime.now()
        days=request.POST.getlist('days[]')
        sep=','
        availdays=sep.join(days)
        deptobjd= department.objects.all()
        hosptobjd = hospitallist.objects.all()
        if doctor_availability.objects.filter(Q(doctorid=doctid) & Q(hospitalid=hostid)):
            usermsg="User Existed"
            return render(request,'doctor_availability.html',{'msg':usermsg,'docid':doctid,'hosptdatad':hosptobjd,'deptdatad':deptobjd})
        savedata=doctor_availability(doctorid=did,hospitalid=hostid,deptid=deptid,available_days=availdays,status='A',cdate=now,mdate=now)
        savedata.save()
        res=("Data Saved")
        
        return render(request,'doctor_availability.html',{'display':res,'docid':doctid,'hosptdatad':hosptobjd,'deptdatad':deptobjd})
def availupdate(request):
         if request.method == 'POST': 
            doctid=request.POST['docid']
            eachdoctorid=request.POST['eachid']
            did=user_reg.objects.get(id=doctid)
            hosptname=request.POST['hospitals']
            deptname=request.POST['department']
            hostid=hospitallist.objects.get(id=hosptname)
            deptid=department.objects.get(id=deptname)
            now=datetime.datetime.now()
            days=request.POST.getlist('days[]')
            sep=','
            availdays=sep.join(days)
            deptobjd= department.objects.all()
            hosptobjd = hospitallist.objects.all()
            
            member = doctor_availability.objects.get(id=eachdoctorid)
            member.doctorid = did
            member.hospitalid = hostid
            member.deptid=deptid
            member.available_days=availdays
            member.status='A'
            member.mdate=now
            member.save()
            
            
            
            res=("Data Updated")
            listobj=fetchfunction(doctid)
            return render(request,'list_hospital.html',{'listdata':listobj,'docid':doctid})
def hosplist(request):
    docid=request.GET['doctorid']
    
    listobj=fetchfunction(docid)
    """
    listobj=doctor_availability.objects.filter(doctorid=docid)
   
    for doctor in listobj:
        val=hospitallist.objects.filter(id=doctor.hospitalid_id).values()
        newval=val.values()[0]
        doctor.hospital=newval['hosptname']
        print ("Newvalue: ",newval['hosptname']) """
    
    return render(request,'list_hospital.html',{'listdata':listobj,'docid':docid})
def deletelist(request):
    docid=request.GET.get('doctorid')
    
    eachdoctorid=request.GET['eachid']
    eachdoctor=doctor_availability.objects.get(id=eachdoctorid)
    
    eachdoctor.delete()
    listobj=fetchfunction(docid)
    return render(request,'list_hospital.html',{'listdata':listobj,'docid':docid})
    
def updatelist(request):
    docid=request.GET.get('doctorid')
    eachdoctorid=request.GET['eachid']
    print("availid:", eachdoctorid)
    deptobjd= department.objects.all()
    hosptobjd = hospitallist.objects.all()
    listobj=doctor_availability.objects.get(id=eachdoctorid)
    day=listobj.available_days
    days=day.split(",")
    weekday=['Monday','Tuesday','Wednesday','Thursday','Friday']
    
    return render(request,'updatelist.html',{'fetchdata':listobj,'docid':docid,'deptdata':deptobjd,'hospdata':hosptobjd,'day':days,'week':weekday})
    
def fetchfunction(docid):
    listobj=doctor_availability.objects.filter(doctorid=docid)
    
    for doctor in listobj:
        val=hospitallist.objects.filter(id=doctor.hospitalid_id).values()
        newval=val.values()[0]
        doctor.hospital=newval['hosptname']
    return listobj
    
    
    
def patientnewdata(request):
    print("inside Function")
    if request.method == 'GET':
        deptname = request.GET.get('dept', None)
        hosptname= request.GET.get('hospt', None)
        appointdate= request.GET.get('appointdate', None)
        #hosptname=request.POST['hosptname']
        #deptname=request.POST['deptname']
        print("department : ",deptname)
        print("hospital : ",hosptname)
        print("Appointdate : ",appointdate)
        
        docobj=doctor_availability.objects.filter(Q(hospitalid=hosptname) & Q(deptid=deptname))
        mylist=list(docobj.values())
        #print("My number :",len(mylist))
        doclist=[]
        
        
        
        for eachdata in docobj:
            
            doctorval=user_reg.objects.filter(id=eachdata.doctorid_id).values()
            
            #doctorname=doctorval.values()[0]
            #eachdata.doctorname=doctorname['fname']+" "+doctorname['lname']
            #print("Doctor is:  ",eachdata.doctorname)
            #docobj.doctorname=eachdata.doctorname
            #dolist.append(eachdata.doctorname)
            
            dolist=list(doctorval)
            doclist.append(dolist)
            
            #hospital.append(eachdata.hospitalid)
            #dept.append(eachdata.deptid)
        #print("Days: ",avail_day)    
        
        
        return JsonResponse({'datas':doclist,'avail':mylist,
        'consultdate':appointdate})
        
       
    #else:
        
        #return JsonResponse({"error": ""}, status=400)
def booking(request):
    if request.method == 'GET':
        selectdate=request.GET['sdate']
        booking_date=request.GET['availday']
        hospital=request.GET['hospt']
        departid=request.GET['dept']
        patient=request.GET['pid']
        doctor=request.GET['docid']
        now=datetime.datetime.now()
        hostid=hospitallist.objects.get(id=hospital)
        deptid=department.objects.get(id=departid)
        
        if consultation.objects.filter(Q(doctorid=doctor) & Q(hospitalid=hospital) & Q(patientid=patient)& Q(status='A')):
            usermsg="Already taken the appointment"
            return render(request,'confirm.html',{'msg':usermsg,'pid':patient})
        
        else:
            savebooking=consultation(hospitalid=hostid,deptid=deptid,doctorid=doctor,patientid=patient,consult_day=selectdate,payment='100',status='A',cdate=now,mdate=now)
            savebooking.save()
            msg=("Thank you ! Your appointment is confirmed")
            return render(request,'confirm.html',{'msg':msg,'pid':patient})
def pbooklist(request):
        pid = request.GET['patientid']
        patientlist=patientfetch(pid)
        
        
        return render(request,'appointmentlist.html',{'pid':pid,'plist':patientlist})
        
def pstate(request):
    pid = request.GET['patientid']
    print("PID IS: ",pid)
    return render(request,'patient_details.html',{'pid':pid})
  
def cancelpatient(request):
    cancel_id=request.GET['cancelid']
    print("id is :" ,cancel_id)
    pid=request.GET.get('pid')
    print("PID is :",pid)
    canceldata=consultation.objects.get(id=cancel_id)
    canceldata.delete()
    patientobjs=patientfetch(pid)
    return render(request,'appointmentlist.html',{'plist':patientobjs,'pid':pid})
def patientfetch(patient):
    patientobj=consultation.objects.filter(patientid=patient)
    for eachpatient in patientobj:
        hospitalval=hospitallist.objects.filter(id=eachpatient.hospitalid_id).values()
        patientval=user_reg.objects.filter(id=eachpatient.patientid).values()
        doctorval=user_reg.objects.filter(id=eachpatient.doctorid).values()
        patientname=patientval.values()[0]
        hostname=hospitalval.values()[0]
        doctorname=doctorval.values()[0]
        eachpatient.hospital=hostname['hosptname']
        eachpatient.patient=patientname['fname']
        eachpatient.doctor=doctorname['fname']
    return patientobj  
def doctorhome(request):
    docid= request.GET['doctorid']
    return render(request,'doctor_details.html',{'docid':docid})