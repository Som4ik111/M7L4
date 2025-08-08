import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

print("🎮 Игра: Переводчик с русского на английский 🎮")
print('Это игра которая будет проверять твой перевод слов с русского на английский.')
print("У тебя есть 3 жизни. Ошибиться можно 3 раза.\n")

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}


while True:
    diff = input('Какой уровень сложности ты выберешь? Уровни: easy, medium, hard: ').lower()
    if diff in words_by_level:
        break
    print("Пожалуйста, выберите один из предложенных уровней сложности!")

lives = 3
score = 0

while lives > 0:
    
    current_word = random.choice(words_by_level[diff])
    
    duration = 5  # секунды записи
    sample_rate = 44100

    print(f"\nПереведи слово: '{current_word}' на английский язык.")
    print("Записываю твой ответ...")
    
    try:
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait()  # ждём завершения записи

        wav.write("output.wav", sample_rate, recording)
        print("Запись завершена, теперь распознаём...")

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print("Ты сказал:", text)

            translator = Translator()
            translated = translator.translate(text, src='en', dest='ru')
            
            
            if translated.text.lower().strip() == current_word.lower().strip():
                print('✅ Правильно!')
                score += 1
            else:
                lives -= 1
                print(f'❌ Неправильно. Правильный перевод: {translator.translate(current_word, src="ru", dest="en").text}')
                print(f'Осталось жизней: {lives}')
                
        except sr.UnknownValueError:
            lives -= 1
            print("Не удалось распознать речь.")
            print(f'Осталось жизней: {lives}')
        except sr.RequestError as e:
            lives -= 1
            print(f"Ошибка сервиса: {e}")
            print(f'Осталось жизней: {lives}')

    except Exception as e:
        lives -= 1
        print(f"Произошла ошибка при записи: {e}")
        print(f'Осталось жизней: {lives}')

print(f"\nИгра окончена! Твой счет: {score}")