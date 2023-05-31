import cv2

# Načtení Haar kaskádového klasifikátoru pro detekci obličeje
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Načtení Haar kaskádového klasifikátoru pro detekci očí
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Načtení Haar kaskádového klasifikátoru pro detekci úst
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Získání přístupu ke kameře
cap = cv2.VideoCapture(0)

while True:
    # Čtení snímku z kamery
    _, frame = cap.read()

    # Převod snímku na šedé odstíny pro zjednodušení detekce
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detekce obličeje v snímku
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Kreslení obdélníka kolem detekovaného obličeje
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detekce očí v detekovaném obličeji
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # Kreslení obdélníka kolem detekovaných očí
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Detekce úst v detekovaném obličeji
        mouth = mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.5)
        for (mx, my, mw, mh) in mouth:
            # Kreslení obdélníka kolem detekovaných úst
            cv2.rectangle(roi_color, (mx, my), (mx+mw, my+mh), (0, 0, 255), 2)

    # Zobrazení upraveného snímku s detekovanými obličeji, očima a ústy
    cv2.imshow('img', frame)

    # Ukončení smyčky, pokud je stisknuta klávesa 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()