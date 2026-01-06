import RPi.GPIO as GPIO
import time

# إعدادات المنافذ بناءً على تقرير بتول الحايك
PIR_PIN = 17        # مستشعر الحركة
DOOR_PIN = 27       # مستشعر الباب
RELAY_PIN = 22      # وحدة الريلاي
BUZZER_PIN = 23     # الإنذار الصوتي

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(DOOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    print("نظام الأمان قيد التشغيل...")
    while True:
        # منطق التحكم الشرطي (OR Logic) من التقرير
        if GPIO.input(PIR_PIN) or GPIO.input(DOOR_PIN):
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
