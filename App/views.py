from django.shortcuts import render, redirect
from django import forms
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _

import datetime
from App import models
from App.models import Recording, User, Composer

from App.utils.index import render_index
from App.utils.login import render_login, process_login_form, process_register_form
from App.utils.upload import process_upload
from App.utils.user import render_user_change, render_user_info, process_user_change_form, process_user_delete, process_verification, verification_required, send_verification_email
from App.utils.recording import render_recording_info, render_recording_change, process_recording_change, process_recording_delete
from App.utils.composer import render_composer_info, render_composer_change, process_composer_change
from django.utils.html import escape
 # Index page
def hello(Request, **kwargs):

    if "tag" not in kwargs:
        return redirect('index/timeline/0')
    
    if "page" in kwargs:
        return render_index(Request, kwargs["tag"], kwargs["page"])
    else :
        return render_index(Request, kwargs["tag"])

# User is accesing upload page
# This page needs auth
@login_required
@verification_required
def upload(Request):
    RecordingName = Request.POST.get('RecordingName')
    ComposerName = Request.POST.get('ComposerName')
    Description = Request.POST.get('Description')
    UploadTime = datetime.datetime.now()
    MyFile = Request.FILES.get('File')

    if Request.method == 'POST' and MyFile:
        process_upload(MyFile,
            RecordingName=RecordingName,
            ComposerName=ComposerName,
            Description=Description,
            UploadTime=UploadTime,
            UploadUser=Request.user
        )
        return render_index(Request)

    return render_index(Request)

# User is accessing "login" page,
def login(Request):

    if Request.user.is_authenticated:

        return redirect('/user/'+Request.user.username+'/')

    return render_login(Request)

# When user submitted a login form in the "login" page,
# process that form and redirect to main page if successed
def login_form(Request):

    UserName = Request.POST.get('UserName')
    Password = Request.POST.get('Password')

    res = process_login_form(Request, UserName, Password)

    if res == True :    # success
        return redirect('/')
    else : # failure
        return render_login(Request, login_failed=True)

# When user submitted a registration form in the "login" page,
# process that from and auto-login if successed
def register_form(Request):

    UserName = Request.POST.get('UserName')
    Email = Request.POST.get('Email')
    Password = Request.POST.get('Password')
    Password2 = Request.POST.get('Password2')

    res = process_register_form(Request, UserName, Email, Password, Password2)

    if "register_failed" in res and res["register_failed"] == True: # failed registration
        return render_login(Request,
                            login_failed=False,
                            register_failed=res["register_failed"],
                            register_nonconsistency=res["register_nonconsistency"],
                            register_used_name=res["register_used_name"],
                            register_non_pku=res["register_non_pku"])
    else :
        return redirect('/')

# Logout a user
def logout(Request) :

    logout_user(Request)

    return render_index(Request)

# Accesing user info page
def user_info(Request, **kwargs) :

    SelectedUsers = User.objects.filter(username=kwargs["username"])

    return render_user_info(Request, Users=SelectedUsers)

# Accesing change page
def user_info_change(Request, **kwards) :

    return render_user_change(Request)

# Comminting a change form
def user_info_change_commit(Request, **kwards) :

    Avatar = Request.FILES.get('Avatar')
    UserName = Request.POST.get('UserName')
    Email = Request.POST.get('Email')
    Password = Request.POST.get('Password')
    Password2 = Request.POST.get('Password2')
    Introduction = Request.POST.get('Introduction')

    print(Request.POST)

    Delete = False
    if 'delete_button' in Request.POST :
        Delete = True
    
    if not Delete :

        res = process_user_change_form(Request, Avatar, UserName, Email, Password, Password2, Introduction)

        if res["change_failed"] == False :    # the user info changed successfully

            print("changed successfully, refreshing...")

            if Password and Password2 :     # if refreshed password, need to reload user
                logout_user(Request)
                res = process_login_form(Request, UserName, Password)
                if res == True :    # success
                    return redirect('/user/'+Request.user.username+'/')
                else : # failure
                    return render_login(Request, login_failed=True)
            
            else :
                return render_user_info(Request, [Request.user])

        else :  # failed, error info are presented in a dict

            print("change failed")
            if "inconsistent_password" in res :
                return render_user_change(Request, ChangeFailed=True, Inconsistency=True)
            elif "conflict_username" in res :
                return render_user_change(Request, ChangeFailed=True, UsedName=True)
            else :
                raise NotImplementedError("Error not handled in views.change")
    
    else :

        process_user_delete(Request)
        return redirect('/')
    
    return render_user_info(Request)

# Showing recording info page
def recording_info(Request, **kwargs) :

    SelectedRecordings = Recording.objects.filter(Id=kwargs["id"])

    return render_recording_info(Request, SelectedRecordings)

# Showing recording editing page
def recording_change(Request, **kwargs) :

    SelectedRecordings = Recording.objects.filter(Id=kwargs["id"])

    return render_recording_change(Request, SelectedRecordings)

# Handling recording change forms
def recording_change_commit(Request, **kwargs) :

    RecordingName = Request.POST.get('RecordingName')
    ComposerName = Request.POST.get('ComposerName')
    Description = Request.POST.get('Description')
    UploadTime = datetime.datetime.now()
    if 'File' in Request.FILES :
        MyFile = Request.FILES.get('File')
    else :
        MyFile = None
    Delete = False

    if 'delete_button' in Request.POST :
        Delete = True

    SelectedRecordings = Recording.objects.filter(Id=kwargs["id"])

    assert(SelectedRecordings.count() == 1)

    SelectedRecording = SelectedRecordings[0]

    if not Delete :
        res = process_recording_change(
            SelectedRecording,
            MyFile,
            RecordingName,
            ComposerName,
            Description,
            UploadTime,
            Request.user)
        return redirect('/recording/' + str(SelectedRecording.get_id()) + '/')
    else :
        res = process_recording_delete(SelectedRecording)
        return redirect('/')
    
# The link to send a verification email
def verify_email(Request, **kwargs) :

    email = Request.user.get_email()

    context = {"Reason": ""}

    if email[-15:] != "@stu.pku.edu.cn" and email[-11:] != "@pku.edu.cn" :
        context["Reason"] = _("Email is not a PKU email address.")
        return render(Request, "verification_fail.html", context)
    else :
        context["Reason"] = _("We have send you a verification email, please check your inbox.")
        send_verification_email(Request.user)
        return render(Request, "verification_pending.html", context)

# If the user is accessing the verification page
# Process the verification information
def verify_email_process(Request, **kwargs):

    UserName = kwargs["username"]
    Code = kwargs["code"]

    res = process_verification(Request, UserName, Code)

    context = {"Reason": res["reason"]}

    if res["verification_failed"] == True :
        return render(Request, "verification_fail.html", context)
    else :
        return render(Request, "verification_success.html", context)

# Error page of not verified email
def error_email_not_verified(Request) :

    return render(Request, "verification_needed.html", {})

def composer_info(Request, **kwargs) :

    SelectedComposer = Composer.objects.filter(Id=kwargs["id"]).all()

    return render_composer_info(Request, SelectedComposer)

def composer_change(Request, **kwargs) :

    SelectedComposer = Composer.objects.filter(Id=kwargs["id"]).get()

    return render_composer_change(Request, SelectedComposer)

def composer_change_commit(Request, **kwargs) :

    SelectedComposer = Composer.objects.filter(Id=kwargs["id"]).get()
    Name = Request.POST.get('Name')
    Introduction = Request.POST.get('Introduction')

    Res = process_composer_change(SelectedComposer, Name, Introduction)

    if Res["ChangeFailed"] == True :
        return render_composer_change(Request, SelectedComposer, **Res)
    else :
        return render_composer_info(Request, SelectedComposer)