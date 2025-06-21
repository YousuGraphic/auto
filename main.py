import asyncio
import random
import os
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
from keep_alive import keep_alive

# تحميل المتغيرات من ملف .env
load_dotenv()

# بيانات الحساب
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
USER_ID = int(os.getenv('USER_ID'))
REPORT_CHANNEL = os.getenv('REPORT_CHANNEL')
MONITOR_CHANNEL = "https://t.me/xqrrp"  # القناة التي سيتم مراقبتها

# روابط القنوات
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
        self.report_channel = REPORT_CHANNEL
        self.last_activity = datetime.now()

    async def initialize(self):
        """تهيئة العميل"""
        self.client = TelegramClient('userbot_session', API_ID, API_HASH)
        await self.client.start()
        
        # إضافة معالج الأحداث لمراقبة القناة
        self.client.add_event_handler(self.handle_channel_message, events.NewMessage(chats=MONITOR_CHANNEL))
        
        await self.send_report("✅ تم تشغيل اليوزر بوت بنجاح!")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم تشغيل اليوزر بوت بنجاح!")
        
        # بدء مهمة الإرسال الدوري
        asyncio.create_task(self.periodic_status_update())
        asyncio.create_task(self.keep_alive_checker())

    async def keep_alive_checker(self):
        """مهمة للتأكد من استمرارية التشغيل"""
        while self.is_running:
            await asyncio.sleep(300)  # كل 5 دقائق
            if (datetime.now() - self.last_activity).total_seconds() > 600:
                await self.send_report("🔄 البوت يعيد التشغيل بسبب عدم النشاط")
                await self.restart_bot()

    async def restart_bot(self):
        """إعادة تشغيل البوت"""
        await self.send_report("🔄 جاري إعادة تشغيل البوت...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    async def periodic_status_update(self):
        """إرسال تحديث الحالة كل 10 دقائق"""
        while self.is_running:
            try:
                status_message = "🤖 البوت يعمل بشكل طبيعي وجميع الوظائف تعمل بكفاءة ✅"
                await self.client.send_message(self.report_channel, status_message)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم إرسال تحديث الحالة")
            except Exception as e:
                error_msg = f"خطأ في إرسال تحديث الحالة: {e}"
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            
            await asyncio.sleep(600)  # 10 دقائق = 600 ثانية

    async def send_report(self, message):
        """إرسال تقرير إلى القناة المحددة"""
        try:
            await self.client.send_message(self.report_channel, message)
            self.last_activity = datetime.now()
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - فشل في إرسال التقرير: {e}")

    async def get_all_groups(self):
        """الحصول على جميع المجموعات"""
        try:
            dialogs = await self.client.get_dialogs()
            groups = [dialog for dialog in dialogs if dialog.is_group]
            return groups
        except Exception as e:
            error_msg = f"خطأ في الحصول على المجموعات: {e}"
            await self.send_report(f"❌ {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
            return []

    async def publish_bio(self, index):
        """نشر صيغة البايو المحددة"""
        try:
            if index < 1 or index > 20:
                await self.send_report("❌ رقم صيغة البايو غير صحيح (يجب أن يكون بين 1 و 20)")
                return
            
            groups = await self.get_all_groups()
            if not groups:
                msg = "⚠️ لا توجد مجموعات متاحة للنشر"
                await self.send_report(msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
                return
            
            total_groups = len(groups)
            await self.send_report(f"🔍 تم جلب {total_groups} مجموعة متاحة للنشر")
            
            text = BIO_TEXTS[index-1]
            success_count = 0
            failed_count = 0
            no_permission_count = 0
            failed_groups = []
            
            for group in groups:
                try:
                    await self.client.send_message(group.id, text)
                    success_count += 1
                    report_msg = f"📢 تم النشر في {group.title} (بايو{index})"
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {report_msg}")
                    await asyncio.sleep(random.uniform(5, 15))
                except Exception as e:
                    if "Forbidden" in str(e):
                        no_permission_count += 1
                    else:
                        failed_count += 1
                        failed_groups.append(group.title)
                    error_msg = f"خطأ في النشر في {group.title}: {e}"
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                    await asyncio.sleep(5)
            
            summary = (
                f"📊 ملخص نشر البايو {index}:\n"
                f"✅ نجاح: {success_count}\n"
                f"❌ فشل: {failed_count}\n"
                f"🚫 بدون صلاحية: {no_permission_count}\n"
                f"📋 المجموعات الفاشلة: {', '.join(failed_groups[:5])}{'...' if len(failed_groups) > 5 else ''}"
            )
            await self.send_report(summary)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {summary}")
            
        except Exception as e:
            error_msg = f"خطأ في نشر البايو: {e}"
            await self.send_report(f"❌ {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")

    async def publish_hisryat(self, index):
        """نشر صيغة رابط الحصريات المحددة"""
        try:
            if index < 1 or index > 20:
                await self.send_report("❌ رقم صيغة الحصريات غير صحيح (يجب أن يكون بين 1 و 20)")
                return
            
            groups = await self.get_all_groups()
            if not groups:
                msg = "⚠️ لا توجد مجموعات متاحة لنشر الروابط"
                await self.send_report(msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
                return
            
            total_groups = len(groups)
            await self.send_report(f"🔍 تم جلب {total_groups} مجموعة متاحة للنشر")
            
            text = f"{LINK_TEXTS_1[index-1]}\n{LINKS[0]}"
            success_count = 0
            failed_count = 0
            no_permission_count = 0
            failed_groups = []
            
            for group in groups:
                try:
                    await self.client.send_message(group.id, text)
                    success_count += 1
                    report_msg = f"🔗 تم نشر رابط الحصريات في {group.title} (حصريات{index})"
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {report_msg}")
                    await asyncio.sleep(random.uniform(5, 15))
                except Exception as e:
                    if "Forbidden" in str(e):
                        no_permission_count += 1
                    else:
                        failed_count += 1
                        failed_groups.append(group.title)
                    error_msg = f"خطأ في نشر رابط الحصريات في {group.title}: {e}"
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                    await asyncio.sleep(5)
            
            summary = (
                f"📊 ملخص نشر رابط الحصريات {index}:\n"
                f"✅ نجاح: {success_count}\n"
                f"❌ فشل: {failed_count}\n"
                f"🚫 بدون صلاحية: {no_permission_count}\n"
                f"📋 المجموعات الفاشلة: {', '.join(failed_groups[:5])}{'...' if len(failed_groups) > 5 else ''}"
            )
            await self.send_report(summary)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {summary}")
            
        except Exception as e:
            error_msg = f"خطأ في نشر رابط الحصريات: {e}"
            await self.send_report(f"❌ {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")

    async def publish_magtae(self, index):
        """نشر صيغة رابط المقاطع المحددة"""
        try:
            if index < 1 or index > 20:
                await self.send_report("❌ رقم صيغة المقاطع غير صحيح (يجب أن يكون بين 1 و 20)")
                return
            
            groups = await self.get_all_groups()
            if not groups:
                msg = "⚠️ لا توجد مجموعات متاحة لنشر الروابط"
                await self.send_report(msg)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")
                return
            
            total_groups = len(groups)
            await self.send_report(f"🔍 تم جلب {total_groups} مجموعة متاحة للنشر")
            
            text = f"{LINK_TEXTS_2[index-1]}\n{LINKS[1]}"
            success_count = 0
            failed_count = 0
            no_permission_count = 0
            failed_groups = []
            
            for group in groups:
                try:
                    await self.client.send_message(group.id, text)
                    success_count += 1
                    report_msg = f"🔗 تم نشر رابط المقاطع في {group.title} (مقاطع{index})"
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {report_msg}")
                    await asyncio.sleep(random.uniform(5, 15))
                except Exception as e:
                    if "Forbidden" in str(e):
                        no_permission_count += 1
                    else:
                        failed_count += 1
                        failed_groups.append(group.title)
                    error_msg = f"خطأ في نشر رابط المقاطع في {group.title}: {e}"
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")
                    await asyncio.sleep(5)
            
            summary = (
                f"📊 ملخص نشر رابط المقاطع {index}:\n"
                f"✅ نجاح: {success_count}\n"
                f"❌ فشل: {failed_count}\n"
                f"🚫 بدون صلاحية: {no_permission_count}\n"
                f"📋 المجموعات الفاشلة: {', '.join(failed_groups[:5])}{'...' if len(failed_groups) > 5 else ''}"
            )
            await self.send_report(summary)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {summary}")
            
        except Exception as e:
            error_msg = f"خطأ في نشر رابط المقاطع: {e}"
            await self.send_report(f"❌ {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")

    async def handle_channel_message(self, event):
        """معالجة الرسائل الواردة في القناة"""
        try:
            message = event.message.message.lower().strip()
            
            # معالجة أوامر البايو
            if message.startswith("بايو"):
                num = message.replace("بايو", "").strip()
                if num.isdigit():
                    index = int(num)
                    await self.send_report(f"📢 تم استلام أمر نشر بايو{index}")
                    await self.publish_bio(index)
            
            # معالجة أوامر الحصريات
            elif message.startswith("حصريات"):
                num = message.replace("حصريات", "").strip()
                if num.isdigit():
                    index = int(num)
                    await self.send_report(f"🔗 تم استلام أمر نشر حصريات{index}")
                    await self.publish_hisryat(index)
            
            # معالجة أوامر المقاطع
            elif message.startswith("مقاطع"):
                num = message.replace("مقاطع", "").strip()
                if num.isdigit():
                    index = int(num)
                    await self.send_report(f"🎥 تم استلام أمر نشر مقاطع{index}")
                    await self.publish_magtae(index)
            
            # إرسال رسالة تأكيد الاستلام
            await event.message.mark_as_read()
            
        except Exception as e:
            error_msg = f"خطأ في معالجة الرسالة: {e}"
            await self.send_report(f"❌ {error_msg}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}")

    async def run(self):
        """تشغيل البوت"""
        await self.initialize()
        
        # استمرار التشغيل حتى يتم إيقافه
        while self.is_running:
            await asyncio.sleep(1)

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
    import sys
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - تم إيقاف البرنامج")
