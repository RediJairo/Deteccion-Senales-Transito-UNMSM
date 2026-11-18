import pyttsx3

def ejecutar_voz(texto, candado):

    co_init = False

    try:
        import pythoncom

        pythoncom.CoInitialize()
        co_init = True

        motor = pyttsx3.init()

        motor.setProperty("rate",145)
        motor.setProperty("volume",1)

        motor.say(texto)
        motor.runAndWait()

        del motor

    except Exception as e:
        print(e)

    finally:

        if co_init:
            pythoncom.CoUninitialize()

        candado.release()