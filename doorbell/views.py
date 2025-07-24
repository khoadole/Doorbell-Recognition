from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, HttpResponse
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from users.decorators import login_required
from .mqtt import publish_to_device
import time

latest_frame = None

@csrf_exempt
def upload_frame(request):
    global latest_frame
    if request.method == "POST" and request.body:
        latest_frame = request.body
        return HttpResponse("OK")
    return HttpResponse("Only POST accept", status=405)

def gen():
    try:
        global latest_frame
        while True:
            if latest_frame:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
            else:
                time.sleep(0.1)
    except GeneratorExit:
        print("Client disconnected.")
        
def video_feed(request):
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    # publish_to_device("haha")
    if request.method == "POST":
        publish_to_device(True)
        
    return render(request, 'homepage.html')

def get_popup_template(request):
    return render(request, 'components/popup.html')

@login_required
def history(request):
    return render(request, 'components/history.html')


