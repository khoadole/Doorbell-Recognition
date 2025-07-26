    // Open door main function fetch api opendoor
    function door() {
        const csrfToken = getCookie('csrftoken');
        fetch('/api/open-door', {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken,
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log("Door opened!");
            }
            else {
                console.error("Failed to open door: " + (data.message || "Unknown error"));
            }
        })
        .catch(error => {
            console.error("Request failed: " + error);
        });
    }

    // Open Door button
    function openDoor() {
    const button = document.getElementById("door-btn");
    button.style.background =
        "linear-gradient(135deg, #10b981 0%, #059669 100%)";
    button.textContent = "Opening door...";
    

    setTimeout(() => {
        button.textContent = "Door opened!";
        door()
        setTimeout(() => {
        button.style.background =
            "linear-gradient(135deg, #00b7ff 0%, #00a0e6 100%)";
        button.textContent = "Open Door";
        }, 2000);
    }, 1000);
    }

    // Noti popup
    let popupTemplate = null;

    document.addEventListener('DOMContentLoaded', function() {
    initPopupTemplate();
    });

    async function initPopupTemplate() {
    if (!popupTemplate) {
        try {
            const response = await fetch('/get-popup-template/'); // Django URL
            if (response.ok) {
                popupTemplate = await response.text();
            } else {
                throw new Error('Failed to load popup template');
            }
        } catch (error) {
            console.error('Error loading popup template:', error);
            popupTemplate = createFallbackTemplate();
        }
    }
    }

    function notiPopup(recognitionData = null) {
        // NEED TO GET DATA
        // const data = recognitionData || {
        //     name: "Nguyen Van C",
        //     confidence: 50,
        //     avatar: "👨‍💼",
        //     timestamp: new Date().toLocaleString()
        // };
        
        const body = document.body;
        body.insertAdjacentHTML('beforeend', popupTemplate);
        body.style.overflow = 'hidden';

        const update = (data) => {
            updatePopupData(data);
            setupPopupEventListeners();
        };

        if (recognitionData) {
            update(recognitionData);
        } else {
            fetch("api/latest-recognition")
                .then(response => response.json())
                .then(data => {
                    update(data);
                })
                .catch(error => {
                    console.error("Failed to fetch latest recognition data: ", error);
                    // fall back
                    update({
                        name: "Unknown",
                        confidence: 0,
                        avatar: "👨‍💼",
                        timestamp: new Date().toLocaleString()
                    });
                });
        }
        
        // setTimeout(() => {
        //     updatePopupData(data);
        //     setupPopupEventListeners();
        // }, 10);
    }

    function updatePopupData(data) {
        const nameElement = document.querySelector('.detail-value');
        const confidenceElement = document.querySelector('.confidence-container .detail-value');
        const confidenceFill = document.querySelector('.confidence-fill');
        const avatar = document.querySelector('.person-avatar');
        
        if (nameElement) nameElement.textContent = data.name;
        if (confidenceElement) confidenceElement.textContent = data.confidence + '%';
        if (confidenceFill) confidenceFill.style.width = data.confidence + '%';
        if (avatar) {
            if (data.avatar.startsWith("data:image")) {
                // If avatar is an image, assume it's an <img>
                if (avatar.tagName.toLowerCase() == 'img') {
                    avatar.src = data.avatar;
                } else {
                    // Replace emoji div/span with an <img> tag
                    const img = document.createElement('img');
                    img.src = data.avatar;
                    img.className = avatar.className;
                    avatar.replaceWith(img);
                }
            } else {
                // If avatar is emoji/text, show it directly
                avatar.textContent = data.avatar;
            }
            
        }
    }

    // ===== UTILITY FUNCTIONS =====

    function setupPopupEventListeners() {
        const overlay = document.getElementById('#popupOverlay .popupOverlay');
        const closeBtn = document.querySelector('#popupOverlay .popup-close');
        const openDoorBtn = document.querySelector('#popupOverlay .btn-primary');
        const dismissBtn = document.querySelector('#popupOverlay .btn-secondary');
        
        if (closeBtn) closeBtn.onclick = closePopup;
        if (dismissBtn) dismissBtn.onclick = closePopup;
        if (openDoorBtn) openDoorBtn.onclick = () => openDoorFromPopup();
        
        if (overlay) {
            overlay.onclick = (e) => {
                if (e.target === overlay) closePopup();
            };
        }
    }

    function closePopup() {
        const popup = document.getElementById('popupOverlay');
        if (popup) popup.remove();
    }

    function openDoorFromPopup(personName) {
        console.log(`Opening door for: ${personName}`);
        // Logic open door
        door();
        closePopup();
    }

    // Get CSRF token for Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // =========== STREAMing =============
    function startStream() {
    const video = document.getElementById('video-stream');
    video.src = "/api/view_feed";
    video.style.display = "block";
    }

    function stopStream() {
    const video = document.getElementById('video-stream');
    video.src = "";  // stops the stream
    video.style.display = "none";
    }

    // function handleRecognitionResult(apiResponse) {
    //     const recognitionData = {
    //         name: apiResponse.person_name,
    //         confidence: apiResponse.confidence_percentage,
    //         avatar: apiResponse.avatar || "👤",
    //         timestamp: apiResponse.timestamp,
    //         person_id: apiResponse.person_id
    //     };
        
    //     notiPopup(recognitionData);
    // }

    // function onWebSocketMessage(event) {
    //     const data = JSON.parse(event.data);
    //     if (data.type === 'face_recognition') {
    //         handleRecognitionResult(data.payload);
    //     }
    // }