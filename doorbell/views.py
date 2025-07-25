from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from users.decorators import login_required
from .models import DeviceLog
from .mqtt import publish_to_device
import time
import threading
import datetime

latest_frame = None
frame_lock = threading.Lock()

@csrf_exempt
def upload_frame(request):
    global latest_frame
    if request.method == "POST" and request.body:
        with frame_lock:
            latest_frame = request.body
        return HttpResponse("OK")
    return HttpResponse("Only POST accept", status=405)

def gen():
    try:
        global latest_frame
        while True:
            with frame_lock:
                frame = latest_frame
            if frame:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
            else:
                time.sleep(0.1)
    except GeneratorExit:
        print("Client disconnected.")
        
def video_feed(request):
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')

def latest_recognition(request):
    latest = DeviceLog.objects.order_by('-date_add').first()
    if latest:
        return JsonResponse({
            "name": latest.name,
            "confidence": round(latest.percent * 100),
            "avatar": f"data:image/jpeg;base64,{latest.image}",  # assumes base64 stored
            "timestamp": latest.date_add.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({"error": "No logs found"}, status=404)

# @csrf_exempt
def open_door(request):
    if request.method == "POST":
        try:
            publish_to_device(True)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def home(request):
    # publish_to_device("haha")
    # if request.method == "POST":
    #     publish_to_device(True)
    # print(datetime.datetime.now())
    return render(request, 'homepage.html')

def get_popup_template(request):
    return render(request, 'components/popup.html')

@login_required
def history(request):
    histories = []
    logs = DeviceLog.objects.order_by('-date_add')
    for log in logs:
        histories.append({
            'name': log.name,
            'percent': round(log.percent * 100),
            'status': log.status,
            'image': f"data:image/jpeg;base64,{log.image}",
            'date': log.date_add.strftime('%Y-%m-%d %H:%M:%S')
        })

    return render(request, 'components/history.html', {'logs' : histories})


