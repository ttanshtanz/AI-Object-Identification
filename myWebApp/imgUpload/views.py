from django.shortcuts import render
from .forms import ImageUploadForm

import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions


# Create your views here.
#The function opens a new file called img.jpg in write-binary mode ('wb+') using a context manager (with open(...) as destination). It then iterates over the file chunks using the chunks() method of the file object and writes each chunk to the destination file using the write() method.
def handle_uploaded_file(f):
    with open('img.jpg','wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def home(request):
    return render(request, 'home.html')

#instantiates an ImageUploadForm object with the request's POST data and FILES data. Then, it checks if the form is valid using the is_valid() method.
#If the form is valid, it calls the handle_uploaded_file function, passing request.FILES['image'] to save the uploaded image. 
def imageprocess(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
            handle_uploaded_file(request.FILES['image'])
            model = ResNet50(weights='imagenet')
            img_path = 'img.jpg'
            import numpy as np
            from tensorflow.keras.preprocessing import image
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preds = model.predict(x)
            print('Predicted:', decode_predictions(preds, top=3)[0])
            
            html = decode_predictions(preds, top=3)[0]
            res = []
            for e in html:
                res.append((e[1],np.round(e[2]*100,2))) #name & %
            return render(request, 'result.html',{'res':res})

    return render(request, 'home.html')