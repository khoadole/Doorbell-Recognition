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
from users.models import User
from .models import DeviceLog, EnrolledFace
import base64

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

@login_required
def enroll_face(request):
    if request.method == 'POST':
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Handle delete request
                if 'face_id' in request.POST:
                    face_id = request.POST.get('face_id')
                    try:
                        # Get current user
                        current_user = User.objects.get(username=request.session.get('username'))
                        
                        # Find and delete the face (only if it belongs to current user)
                        face = EnrolledFace.objects.get(id=face_id, owner=current_user)
                        face.delete()
                        
                        return JsonResponse({
                            'success': True,
                            'message': 'Face deleted successfully'
                        })
                    except EnrolledFace.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'message': 'Face not found or you do not have permission to delete it'
                        })
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'message': f'Error deleting face: {str(e)}'
                        })
                
                # Handle upload request
                else:
                    name = request.POST.get('name', '').strip()
                    image_file = request.FILES.get('image')
                    
                    if not name:
                        return JsonResponse({
                            'success': False,
                            'message': 'Name is required'
                        })
                    
                    if not image_file:
                        return JsonResponse({
                            'success': False,
                            'message': 'Image is required'
                        })
                    
                    # Validate image size (5MB limit)
                    if image_file.size > 5 * 1024 * 1024:
                        return JsonResponse({
                            'success': False,
                            'message': 'Image size must be less than 5MB'
                        })
                    
                    # Validate image type
                    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
                    if image_file.content_type not in allowed_types:
                        return JsonResponse({
                            'success': False,
                            'message': 'Only JPG, PNG, and GIF images are allowed'
                        })
                    
                    try:
                        # Convert image to base64
                        image_data = image_file.read()
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                        
                        # Get current user
                        current_user = User.objects.get(username=request.session.get('username'))
                        
                        # Create new enrolled face
                        enrolled_face = EnrolledFace(
                            name=name,
                            image=image_base64,
                            owner=current_user,
                            type="enrolled_face"
                        )
                        enrolled_face.save()
                        
                        return JsonResponse({
                            'success': True,
                            'message': 'Face uploaded successfully'
                        })
                        
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'message': f'Error saving face: {str(e)}'
                        })
            
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Unexpected error: {str(e)}'
                })
        
        # If not AJAX, redirect to avoid form resubmission
        return redirect('enroll_face')
    
    # GET request - display enrolled faces
    try:
        # Get current user
        current_user = User.objects.get(username=request.session.get('username'))
        
        # Get enrolled faces for current user
        enrolled_faces_data = []
        enrolled_faces = EnrolledFace.objects.filter(owner=current_user).order_by('-create_at')
        
        for face in enrolled_faces:
            enrolled_faces_data.append({
                'id': str(face.id),
                'name': face.name,
                'image': f"data:image/jpeg;base64,{face.image}",
                'date': face.create_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return render(request, 'components/enroll_face.html', {
            'enrolled_faces': enrolled_faces_data
        })
        
    except User.DoesNotExist:
        return redirect('user:signin')
    except Exception as e:
        # Log error and show empty page
        print(f"Error loading enrolled faces: {str(e)}")
        return render(request, 'components/enroll_face.html', {
            'enrolled_faces': []
        })
