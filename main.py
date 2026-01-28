from gpiozero import PWMLED
from gpiozero.tones import Tone
from gpiozero import LED, MotionSensor, Buzzer, TonalBuzzer
from time import sleep, time

# تعريف القطع - تأكد من توصيل الأسلاك بالأرقام الصحيحة
led = PWMLED(18)
pir = MotionSensor(17)
buzzer = TonalBuzzer(22)
buzzer.stop()

def smooth_on():
    """دالة لزيادة شدة الضوء تدريجياً"""
    print("light smoothly - تدرج الضوء للعمل")
    for i in range(0, 101, 5):
        led.value = i / 100
        sleep(0.05)

def smooth_off():
    """دالة لإطفاء الضوء تدريجياً"""
    print("light smoothly - تدرج الضوء للإطفاء")
    for i in range(100, -1, -5):
        led.value = i / 100
        sleep(0.05)

def panic_mode():
    """دالة الإنذار عند بقاء الشخص لفترة"""
    print("panic mode - تشغيل الإنذار")
    led.value = 0
    try:
        for _ in range(5):
            buzzer.play(Tone(880.0))
            led.value = 1       # تم التعديل: الضوء سيعمل الآن بقوة 100%
            sleep(0.2)
            
            buzzer.stop()       # تم التعديل: كتابة stop بشكل صحيح
            led.value = 0       # إطفاء الضوء لخلق تأثير الوميض
            sleep(0.2)
            
    except ValueError:
        print("freq to high")
        buzzer.stop()

print("system is on waiting for motion")
sleep(3)
print("active")

try:
    while True:
        if pir.motion_detected:
            # الانتظار لمدة ثانيتين للتأكد من استمرار وجود الشخص
            sleep(2) 
            
            if pir.motion_detected:
                # إذا استمر الشخص بالوقوف (حالة ذعر)
                panic_mode()
                # ننتظر حتى يغادر الشخص المنطقة تماماً قبل العودة للمراقبة
                while pir.motion_detected:
                    sleep(1)
            else:
                # إذا كانت حركة عابرة (تدرج الضوء)
                smooth_on()
                sleep(3)
                smooth_off()
                
        sleep(0.1)

except KeyboardInterrupt:
    print("user stopped")

finally:
    # تنظيف المداخل وإطفاء كل شيء عند الإغلاق
    buzzer.stop()
    led.off()
    print("clean up")