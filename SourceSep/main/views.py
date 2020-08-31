import os, time
from . import process

from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    if request.method == 'POST':
        f = request.FILES['input_file']
        fs = FileSystemStorage()
        filename = fs.get_available_name(f.name, max_length=None)
        filepath = os.path.join(BASE_DIR,"media", filename)
        with open(filepath, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return redirect('/file/'+ filename)
    else:
        return render(request, 'main/home.html')

def file(request, filename):
    args = {}
    args['audio'] = filename
    return render(request, 'main/file.html', args)

def sep(request, filename):
    args = {}
    print("SEPERATE")
    modelname = "C:\Projects\Year4\FYP\SourceSep\main\Music2SpeechLargeDB.h5"
    fileIn = os.path.join(BASE_DIR,"media", filename)
    fileOut = os.path.join(BASE_DIR,"media", "SEP" + filename)
    process.separate(fileIn, fileOut, modelname)

    args['mixture'] = filename
    args['speech'] = "SEP" + filename
    return render(request, 'main/split.html', args)

def soon(request):
    return render(request, 'main/soon.html')

def samples(request):
    return render(request, 'main/samples.html')
