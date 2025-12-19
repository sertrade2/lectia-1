import requests
import schedule
import time
from datetime import datetime

# ========== НАСТРОЙКИ ==========
# Вставь сюда свой токен доступа
ACCESS_TOKEN = "EAAJqMz67FjwBQAHySZASJR0jX3ZCXQTt2T2azqZCZBPEM6KNJ5kVv1V24h6h0NWG7puZAZAJUfpswRJ8eBOsV4ECkGOENl4V4rkK8BMeK3DVNbRwSlZAIkI1iQOCiHhUY2PNWq7RgKE1aOiPZB5h3UyxebV3OhSD0UfNNSZBiPYrJuZCi2Y9P8YpUJsLHlC9oOZAIDzZBfIuSItBqZAyFafdicun2WV4PYx0y9ZCw5Qn9MeMpjhuaRE0ISqpnlZChlwHMDSIjT2w2FXLnjK32tVatFmhIdD"
# Вставь сюда ID своего Instagram аккаунта
INSTAGRAM_ACCOUNT_ID = "1202166554573591"

# URL фото которое будет постить бот (должно быть доступно по интернету)
PHOTO_URL = "https://picsum.photos/1080/1080"  # Пример: случайное фото

# Текст поста
CAPTION = "Автоматический пост от бота! 🤖 #bot #automated"

# Время постинга (формат: "ЧЧ:ММ")
POST_TIME = "23:53"  # Каждый день в 10:00
# ================================


def post_to_instagram(image_url, caption):
    """
    Функция для постинга фото в Instagram
    """
    try:
        print(f"[{datetime.now()}] Начинаю постинг...")
        
        # Шаг 1: Создаём контейнер медиа
        create_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
        create_params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }
        
        print("Создаю контейнер медиа...")
        response = requests.post(create_url, params=create_params)
        
        if response.status_code != 200:
            print(f"❌ Ошибка создания контейнера: {response.text}")
            return False
        
        creation_id = response.json()["id"]
        print(f"✅ Контейнер создан! ID: {creation_id}")
        
        # Шаг 2: Публикуем пост
        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_params = {
            "creation_id": creation_id,
            "access_token": ACCESS_TOKEN
        }
        
        print("Публикую пост...")
        response = requests.post(publish_url, params=publish_params)
        
        if response.status_code != 200:
            print(f"❌ Ошибка публикации: {response.text}")
            return False
        
        post_id = response.json()["id"]
        print(f"🎉 Пост успешно опубликован! ID поста: {post_id}")
        return True
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {str(e)}")
        return False


def main():
    """
    Главная функция бота
    """
    print("=" * 50)
    print("🤖 Instagram Auto Post Bot запущен!")
    print(f"⏰ Время постинга: {POST_TIME} каждый день")
    print("=" * 50)
    
    # Проверяем настройки
   
    
    # Планируем ежедневный пост
    schedule.every().day.at(POST_TIME).do(
        post_to_instagram,
        image_url=PHOTO_URL,
        caption=CAPTION
    )
    
    print(f"\n✅ Бот настроен! Жду времени постинга ({POST_TIME})...")
    print("Для остановки нажми Ctrl+C\n")
    
    # Бесконечный цикл проверки расписания
    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем каждую минуту


if __name__ == "__main__":
    main()