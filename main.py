import asyncio
import random
import os
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv
from keep_alive import keep_alive

# تحميل المتغيرات من ملف .env
load_dotenv()

# بيانات الحساب
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
USER_ID = int(os.getenv('USER_ID'))
REPORT_CHANNEL = os.getenv('REPORT_CHANNEL')

# إعدادات النشر
PUBLISH_INTERVAL = 3600  # كل ساعة (بالثواني)
LINKS_PUBLISH_INTERVAL = 10800  # كل 3 ساعات (بالثواني)
LINKS = [
    "https://t.me/+V84P28GntXswYzk0",  # قناة الحصريات
    "https://t.me/+hygcUTDegyAxMTc0"   # قناة المقاطع الحصرية
]

# 20 صيغة جذابة لنشر البايو
BIO_TEXTS = [
    "🔥 اكتشف المحتوى الحصري في القناة! رابط الانضمام في البايو 👆",
    "🎬 مقاطع لن تجدها إلا عندنا! تفضل بالانضمام عبر الرابط في البايو",
    "🚀 انضم إلى قناتنا الحصرية للوصول إلى محتوى مميز! الرابط في البايو",
    "💎 محتوى حصري ينتظرك! اضغط على الرابط في البايو للانضمام الآن",
    "🌟 قناة خاصة بمحتوى لن تراه في أي مكان آخر! الرابط في البايو",
    "📽️ استمتع بأفضل المقاطع الحصرية! انضم إلينا عبر الرابط في البايو",
    "🎉 احصل على محتوى مميز يوميًا! الرابط في البايو للانضمام",
    "🛍️ عروض حصرية للمشتركين! انضم الآن عبر الرابط في البايو",
    "👑 قناة VIP للحصول على أفضل المحتويات! الرابط في البايو",
    "💣 مقاطع حصرية مميزة! اضغط على الرابط في البايو للانضمام",
    "🎁 هدايا وعروض خاصة للمشتركين! الرابط في البايو",
    "🔥🔥 محتوى حصري ينتظرك! انضم الآن عبر الرابط في البايو",
    "👀 لا تفوت الفرصة! محتوى حصري في انتظارك، الرابط في البايو",
    "💃 استمتع بأفضل المقاطع! انضم إلى قناتنا عبر الرابط في البايو",
    "🛑 توقف! لدينا ما تبحث عنه، انضم عبر الرابط في البايو",
    "⚡ شحنات يومية من المحتوى المميز! الرابط في البايو",
    "🤩 مفاجآت تنتظرك! انضم إلى قناتنا الحصرية عبر الرابط في البايو",
    "🚨 إنذار أخير! الفرصة تنتهي قريبًا، انضم الآن عبر الرابط في البايو",
    "🎯 محتوى يستحق المشاهدة! الرابط في البايو",
    "🌈 تجربة مشاهدة فريدة تنتظرك! الرابط في البايو"
]

# 20 صيغة جذابة مصاحبة لرابط قناة الحصريات (محتوى عام)
LINK_TEXTS_1 = [
    "🚀 انضم إلى قناتنا الحصرية لمشاهدة أفضل المحتويات!",
    "💎 قناة VIP للحصول على محتوى لن تجده في أي مكان آخر!",
    "🔥 محتوى حصري ينتظرك! انضم الآن ولا تفوت الفرصة",
    "🎬 أفضل المقاطع الحصرية تجدها هنا! اضغط للانضمام",
    "🌟 قناة خاصة بمحتوى مميز يومي! انضم إلينا الآن",
    "💣 مقاطع حصرية مميزة! اضغط للانضمام إلى القناة",
    "🎁 هدايا وعروض خاصة للمشتركين فقط! انضم الآن",
    "👑 محتوى VIP بانتظارك! اضغط على الرابط للانضمام",
    "🛍️ عروض حصرية لا تعوض! اضغط للانضمام الآن",
    "👀 لا تفوت الفرصة! محتوى لن تراه إلا هنا",
    "⚡ شحنات يومية من المحتوى المميز! انضم إلينا",
    "🤩 مفاجآت تنتظرك في قناتنا الحصرية! انضم الآن",
    "🚨 إنذار أخير! الفرصة تنتهي قريبًا، انضم الآن",
    "🎉 احتفل معنا بأفضل المحتويات! اضغط للانضمام",
    "💃 استمتع بأفضل المقاطع الحصرية! انضم إلى القناة",
    "🛑 توقف! لدينا ما تبحث عنه، انضم الآن",
    "📽️ محتوى حصري بانتظارك! انضم إلينا",
    "🎯 محتوى يستحق المشاهدة! انضم الآن",
    "🌈 تجربة مشاهدة فريدة تنتظرك!",
    "🚀 انطلق في رحلة المحتوى الحصري! انضم الآن"
]

# 20 صيغة جذابة مصاحبة لرابط قناة المقاطع الحصرية (تركيز على المقاطع)
LINK_TEXTS_2 = [
    "🎥 قناة المقاطع الحصرية تفتح أبوابها لك! انضم الآن",
    "💫 اكتشف عالمًا من المقاطع التي لن تراها إلا هنا!",
    "🔥 مقاطع حصرية تنتظرك! اضغط للانضمام إلى القناة",
    "🌟 قناة خاصة بأجمل المقاطع الحصرية! انضم إلينا",
    "🎬 أفضل المقاطع المجمعة في مكان واحد! انضم الآن",
    "💣 مقاطع حصرية مميزة! لا تفوت الفرصة، انضم",
    "🎁 هدايا وعروض خاصة لمشتركي القناة فقط! انضم",
    "👑 محتوى VIP من المقاطع الحصرية! اضغط للانضمام",
    "🛍️ عروض حصرية على المقاطع! اضغط للانضمام الآن",
    "👀 مقاطع لن تراها في أي مكان آخر! انضم إلينا",
    "⚡ شحنات يومية من المقاطع المميزة! انضم الآن",
    "🤩 مفاجآت مقاطع تنتظرك! انضم إلى قناتنا الحصرية",
    "🚨 الفرصة الأخيرة للانضمام! لا تفوت المقاطع الحصرية",
    "🎉 احتفل معنا بأفضل المقاطع! اضغط للانضمام",
    "💃 استمتع بمقاطع لن تنساها! انضم إلى القناة",
    "🛑 توقف! لدينا المقاطع التي تبحث عنها، انضم الآن",
    "📽️ مكتبة ضخمة من المقاطع الحصرية! انضم إلينا",
    "🎯 أفضل المقاطع المختارة تنتظرك! انضم الآن",
    "🌈 تجربة مشاهدة لا تُنسى! اضغط للانضمام",
    "🚀 انطلق في رحلة المقاطع الحصرية! انضم الآن"
]

class AutoPoster:
    def __init__(self):
        self.client = None
        self.is_running = True
        self.publish_interval = PUBLISH_INTERVAL
        self.links_publish_interval = LINKS_PUBLISH_INTERVAL
        self.report_channel = REPORT_CHANNEL

    async def initialize(self):
        """تهيئة العميل"""
        self.client = TelegramClient('userbot_session', API_ID, API_HASH)
        await self.client.start()
        await self.send_report("✅ تم تشغيل اليوزر بوت بنجاح!")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم تشغيل اليوزر بوت بنجاح!")

    async def send_report(self, message):
        """إرسال تقرير إلى القناة المحددة"""
        try:
            await self.client.send_message(self.report_channel, message)
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - فشل في إرسال التقرير: {e}")

    async def get_all_groups(self):
        """الحصول على جميع المجموعات"""
        try:
            dialogs = await self.client.get_dialogs()
            groups = [dialog for dialog in dialogs if dialog.is_group]
            await self.send_report(f"🔍 تم جلب {len(groups)} مجموعة متاحة للنشر")
            return groups
        except Exception as e:
            error_msg = f"خطأ في الحصول على المجموعات: {e}"
            await self.send_report(f"❌ {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            return []

    async def publish_message(self):
        """نشر رسالة في جميع المجموعات"""
        groups = await self.get_all_groups()
        if not groups:
            msg = "⚠️ لا توجد مجموعات متاحة للنشر"
            await self.send_report(msg)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
            return

        text = random.choice(BIO_TEXTS)
        success_count = 0
        
        for group in groups:
            try:
                await self.client.send_message(group.id, text)
                success_count += 1
                report_msg = f"📢 تم النشر في {group.title}"
                await self.send_report(report_msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {report_msg}")
                await asyncio.sleep(random.uniform(5, 15))
            except Exception as e:
                error_msg = f"خطأ في النشر في {group.title}: {e}"
                await self.send_report(f"❌ {error_msg}")
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                await asyncio.sleep(30)
        
        summary = f"📊 ملخص نشر البايو: {success_count}/{len(groups)} مجموعة"
        await self.send_report(summary)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {summary}")

    async def publish_links(self):
        """نشر الروابط في جميع المجموعات"""
        groups = await self.get_all_groups()
        if not groups:
            msg = "⚠️ لا توجد مجموعات متاحة لنشر الروابط"
            await self.send_report(msg)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
            return

        success_count = 0
        
        for group in groups:
            try:
                # نشر الرابط الأول مع نص عشوائي
                link = LINKS[0]
                text = random.choice(LINK_TEXTS_1)
                await self.client.send_message(group.id, f"{text}\n{link}")
                report_msg = f"🔗 تم نشر رابط الحصريات في {group.title}"
                await self.send_report(report_msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {report_msg}")
                await asyncio.sleep(random.uniform(5, 15))
                
                # نشر الرابط الثاني مع نص عشوائي
                link = LINKS[1]
                text = random.choice(LINK_TEXTS_2)
                await self.client.send_message(group.id, f"{text}\n{link}")
                report_msg = f"🔗 تم نشر رابط المقاطع في {group.title}"
                await self.send_report(report_msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {report_msg}")
                await asyncio.sleep(random.uniform(5, 15))
                
                success_count += 1
            except Exception as e:
                error_msg = f"خطأ في نشر الروابط في {group.title}: {e}"
                await self.send_report(f"❌ {error_msg}")
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                await asyncio.sleep(30)
        
        summary = f"📊 ملخص نشر الروابط: {success_count}/{len(groups)} مجموعة"
        await self.send_report(summary)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {summary}")

    async def schedule_publishing(self):
        """جدولة النشر التلقائي"""
        while self.is_running:
            try:
                await self.publish_message()
                msg = f"⏳ انتظار {self.publish_interval//3600} ساعة للنشر التالي"
                await self.send_report(msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
                await asyncio.sleep(self.publish_interval)
            except Exception as e:
                error_msg = f"خطأ في جدولة النشر: {e}"
                await self.send_report(f"❌ {error_msg}")
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                await asyncio.sleep(60)

    async def schedule_links_publishing(self):
        """جدولة نشر الروابط"""
        while self.is_running:
            try:
                await self.publish_links()
                msg = f"⏳ انتظار {self.links_publish_interval//3600} ساعة لنشر الروابط التالي"
                await self.send_report(msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
                await asyncio.sleep(self.links_publish_interval)
            except Exception as e:
                error_msg = f"خطأ في جدولة نشر الروابط: {e}"
                await self.send_report(f"❌ {error_msg}")
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                await asyncio.sleep(60)

    async def run(self):
        """تشغيل البوت"""
        await self.initialize()
        
        # بدء المهام في الخلفية
        asyncio.create_task(self.schedule_publishing())
        asyncio.create_task(self.schedule_links_publishing())
        
        # استمرار التشغيل حتى يتم إيقافه
        while self.is_running:
            await asyncio.sleep(3600)

async def main():
    # تشغيل خادم keep_alive
    keep_alive()
    
    poster = AutoPoster()
    while True:
        try:
            await poster.run()
        except Exception as e:
            error_msg = f"حدث خطأ جسيم: {e}"
            await poster.send_report(f"❌ {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - إعادة تشغيل البوت بعد 60 ثانية...")
            await asyncio.sleep(60)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم إيقاف البرنامج")
