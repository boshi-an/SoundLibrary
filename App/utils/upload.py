import os
from django import forms
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from App.models import Recording, Composer

# Save a uploaded file to disk and maintain databases
def process_upload(
    MyFile, 
    RecordingName,
    ComposerName,
    Description,
    UploadTime,
    UploadUser
    ) :

    # FileStorage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "Uploaded"))
    # Filename = FileStorage.save(MyFile.name, MyFile)
    # UploadedFileUrl = FileStorage.url(Filename)

    CurComposer, _created = Composer.objects.get_or_create(Name=ComposerName, defaults={"Introduction": "Empty"})

    if _created :

        print("Created New Composer: ", CurComposer.Name)

    CurRecording = Recording(
        Name=RecordingName,
        File=MyFile,
        Composer=CurComposer,
        UploadUser=UploadUser,
        UploadUserName=UploadUser.username,
        Description=Description,
        UploadTime=UploadTime
        )
    
    CurRecording.save()

    return