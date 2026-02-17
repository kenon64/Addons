"""
Модуль работы с голосом
Распознавание и синтез речи
"""

import speech_recognition as sr
import pyttsx3
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    def __init__(self, language: str = "ru_RU"):
        self.recognizer = sr.Recognizer()
        self.engine = None
        self.language = language
        self.is_available = False
        
        try:
            self.engine = pyttsx3.init()
            self._setup_tts()
            self.is_available = True
            logger.info("✓ Voice assistant инициализирован")
        except Exception as e:
            logger.warning(f"⚠️ Voice synthesis недоступен: {e}")
            logger.info("   (Текстовый UI будет использоваться вместо этого)")
            self.engine = None
            self.is_available = False

    def _setup_tts(self):
        """Настройка синтеза речи"""
        if self.engine:
            self.engine.setProperty('rate', 150)  # Скорость
            self.engine.setProperty('volume', 0.9)  # Громкость

    def listen(self, timeout: int = 10) -> Optional[str]:
        """
        Слушать микрофон и распознавать речь
        
        Args:
            timeout: Максимальное время прослушивания в секундах
            
        Returns:
            Распознанный текст или None
        """
        try:
            with sr.Microphone() as source:
                logger.info("🎤 Слушаю...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            logger.info(f"✓ Распознано: '{text}'")
            return text
        except sr.UnknownValueError:
            logger.warning("⚠️ Не удалось распознать речь")
            return None
        except sr.RequestError as e:
            logger.error(f"❌ Ошибка сервиса распознавания: {e}")
            return None
        except sr.Timeout:
            logger.warning("⏱️ Время ожидания истекло")
            return None

    def speak(self, text: str):
        """
        Произнести текст
        
        Args:
            text: Текст для озвучивания
        """
        if not self.is_available:
            logger.debug(f"Voice synthesis недоступен, игнорируем: '{text}'")
            return
        
        logger.info(f"🔊 Говорю: '{text}'")
        try:
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Ошибка при синтезе речи: {e}")

