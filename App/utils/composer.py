from django.shortcuts import render
from App.models import Composer, Recording

def render_composer_info(OriginalRequest, SelectedComposers) :

    Context                     = {}
    Context["AllComposers"]     = []
    for composer in SelectedComposers :
        OwnRecordings = Recording.objects.filter(Composer=composer)
        Context["AllComposers"].append({"composer": composer, "recordings": OwnRecordings})

    return render(OriginalRequest, "composer.html", Context)

def render_composer_change(
    OriginalRequest,
    SelectedComposer: Composer,
    ChangeFailed=False,
    MultipleNames=False) :

    Context                     = {}
    Context["Composer"]         = SelectedComposer
    Context["ChangeFailed"]     = ChangeFailed
    Context["MultipleNames"]    = MultipleNames

    return render(OriginalRequest, "composer_change.html", Context)

def process_composer_change(
    SelectedComposer: Composer,
    Name,
    Introduction
    ) :

    if Name != SelectedComposer.get_name() :
        SameName = Composer.objects.filter(Name=Name).all()
        if len(SameName) :
            return {"ChangeFailed": True, "MultipleNames": True}

    SelectedComposer.Name = Name
    SelectedComposer.Introduction = Introduction

    SelectedComposer.save()

    return {"ChangeFailed": False, "MultipleNames": False}