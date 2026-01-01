#!/usr/bin/env python3
#!/usr/bin/env python3
"""
=======================================================
MIGRANT56 V3.0 GLOCAL EDITION
이주민 선교를 위한 23개국 언어 성경 암송 오디오 생성기
=======================================================
"""

import asyncio
import os
import json

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts가 설치되지 않았습니다. (pip install edge-tts)")
    exit(1)

AUDIO_DIR = "audio"

# 🌍 23개국 언어 및 성우 설정 (글로컬 선교 풀 패키지)
VOICES = {
    # === 기본 언어 ===
    "ko": "ko-KR-SunHiNeural",       # 한국어
    "en": "en-US-JennyNeural",       # 영어 (미국)
    
    # === 고용허가제(EPS) 17개국 ===
    "zh": "zh-CN-XiaoxiaoNeural",    # 중국 (중국어)
    "vi": "vi-VN-HoaiMyNeural",      # 베트남
    "th": "th-TH-PremwadeeNeural",   # 태국
    "id": "id-ID-GadisNeural",       # 인도네시아
    "tl": "fil-PH-AngeloNeural",     # 필리핀 (따갈로그)
    "mn": "mn-MN-YesuiNeural",       # 몽골
    "si": "si-LK-ThiliniNeural",     # 스리랑카 (싱할라)
    "uz": "uz-UZ-MadinaNeural",      # 우즈베키스탄
    "ur": "ur-PK-UzmaNeural",        # 파키스탄 (우르두)
    "km": "km-KH-SreymomNeural",     # 캄보디아 (크메르)
    "bn": "bn-BD-NabanitaNeural",    # 방글라데시 (벵골)
    "ky": "ky-KG-GulnaraNeural",     # 키르기스스탄 (키르기스)
    "ne": "ne-NP-HemkalaNeural",     # 네팔
    "my": "my-MM-NilarNeural",       # 미얀마
    "lo": "lo-LA-KeomanyNeural",     # 라오스
    "tg": "tg-TJ-EnekonaNeural",     # 타지키스탄 (타지크)
    
    # === 글로벌 전략 언어 ===
    "ru": "ru-RU-DmitryNeural",      # 러시아어 (중앙아시아 공용)
    "ar": "ar-SA-HamedNeural",       # 아랍어 (이슬람권)
    "es": "es-ES-AlvaroNeural",      # 스페인어 (중남미)
    "pt": "pt-BR-AntonioNeural",     # 포르투갈어 (동티모르/브라질)
    "fr": "fr-FR-HenriNeural",       # 프랑스어 (아프리카)
}

# 📖 Day 1 (말씀으로 시작) - 23개 언어 전체 번역 데이터
VERSES = [
    {
        "day": 1, "meal": "B",
        "ko": "예수께서 대답하여 이르시되 기록되었으되 사람이 떡으로만 살 것이 아니요 하나님의 입으로부터 나오는 모든 말씀으로 살 것이라 하였느니라",
        "en": "Jesus answered, It is written: Man shall not live on bread alone, but on every word that comes from the mouth of God.",
        "zh": "耶稣却回答说：经上记着说：人活着，不是单靠食物，乃是靠神口里所出的一切话。",
        "vi": "Đức Chúa Jêsus đáp: Có lời chép rằng: Người ta sống chẳng phải chỉ nhờ bánh mà thôi, song nhờ mọi lời nói ra từ miệng Đức Chúa Trời.",
        "th": "มนุษย์จะดำรงชีวิตด้วยอาหารเพียงอย่างเดียวไม่ได้ แต่ต้องดำรงชีวิตด้วยพระวจนะทุกคำ ซึ่งออกมาจากพระโอษฐ์ของพระเจ้า",
        "id": "Tetapi Yesus menjawab: Ada tertulis: Manusia hidup bukan dari roti saja, tetapi dari setiap firman yang keluar dari mulut Allah.",
        "tl": "Sumagot si Jesus, Nasusulat, Hindi sa tinapay lamang mabubuhay ang tao, kundi sa bawat salitang namutawi sa bibig ng Diyos.",
        "mn": "Есүс: Хүн зөвхөн талхаар бус, харин Бурханы амнаас гарах үг бүрээр амьдарна гэж бичигдсэн байдаг гэв.",
        "si": "යේසුස්වහන්සේ උත්තරදෙමින්: මනුෂ්‍යයා රොටි පමණක් නොව දෙවියන්වහන්සේගේ මුඛයෙන් නිකුත් වන සියලු වචනවලින් ජීවත් වන්නේය කියා ලියා තිබේ යයි වදාළ සේක.",
        "uz": "Iso unga javob berib dedi: — Muqaddas Bitiklarda yozilgan: “Inson faqat non bilan emas, balki Xudoning og‘zidan chiqqan har bir so‘z bilan yashaydi.”",
        "ur": "یسوع نے جواب دیا، ”لکھا ہے کہ ’انسان صرف روٹی ہی سے جیتا نہیں رہے گا بلکہ ہر اُس بات سے جو اللہ کے منہ سے نکلتی ہے۔‘“",
        "km": "មនុស្ស​មិន​មែន​រស់​ដោយ​សារ​តែ​នំប៉័ង​ប៉ុណ្ណោះ​ទេ គឺ​រស់​ដោយ​សារ​គ្រប់​ទាំង​ព្រះ‌បន្ទូល ដែល​ចេញ​ពី​ព្រះ‌ឱស្ឋ​របស់​ព្រះ‌ជាម្ចាស់​វិញ។",
        "bn": "যীশু উত্তর দিলেন, শাস্ত্রে লেখা আছে: ‘মানুষ কেবল রুটিতেই বাঁচে না, কিন্তু ঈশ্বরের মুখের প্রতিটি কথাতেই বাঁচে৷’",
        "ky": "Ыйса ага: – Ыйык Жазууда: „Адам нан менен гана эмес, Кудайдын оозунан чыккан ар бир сөз менен да жашайт“, – деп жазылган, – деп жооп берди.",
        "ne": "येशूले जवाफ दिनुभयो, “लेखिएको छ: ‘मानिस रोटीले मात्र होइन, तर परमेश्वरको मुखबाट निस्केको हरेक वचनले बाँच्दछ।’”",
        "my": "ကိုယ်တော်က၊ လူသည် မုန့်အားဖြင့်သာ အသက်ကို မွေးရမည်မဟုတ်။ ဘုရားသခင်၏ မိန့်တော်မူသမျှသော စကားအားဖြင့် အသက်ကို မွေးရမည် ကျမ်းစာလာသည်ဟု ပြန်ပြောတော်မူ၏။",
        "lo": "ພຣະເຢຊູ​ຊົງ​ຕອບ​ວ່າ, “ມີ​ຄຳ​ຂຽນ​ໄວ້​ໃນ​ພຣະຄຳພີ​ວ່າ ‘ມະນຸດ​ຈະ​ບຳລຸງ​ຊີວິດ​ດ້ວຍ​ອາຫານ​ສິ່ງ​ດຽວ​ກໍ​ຫາ​ບໍ່​ໄດ້ ແຕ່​ບຳລຸງ​ດ້ວຍ​ພຣະທຳ​ທຸກ​ຂໍ້ ຊຶ່ງ​ອອກ​ມາ​ຈາກ​ພຣະໂອດ​ຂອງ​ພຣະເຈົ້າ.’”",
        "tg": "Исо дар ҷавоб гуфт: «Навишта шудааст, ки \"инсон на танҳо бо нон зист мекунад, балки бо ҳар калимае ки аз даҳони Худо содир мешавад\"».",
        "ru": "Иисус сказал ему в ответ: написано: не хлебом одним будет жить человек, но всяким словом, исходящим из уст Божиих.",
        "ar": "فَأَجَابَ وَقَالَ: «مَكْتُوبٌ: لَيْسَ بِالْخُبْزِ وَحْدَهُ يَحْيَا الإِنْسَانُ، بَلْ بِكُلِّ كَلِمَةٍ تَخْرُجُ مِنْ فَمِ اللَّهِ».",
        "es": "Jesús respondió y dijo: Escrito está: No sólo de pan vivirá el hombre, sino de toda palabra que sale de la boca de Dios.",
        "pt": "Jesus, porém, respondeu: Está escrito: Não só de pão viverá o homem, mas de toda palavra que sai da boca de Deus.",
        "fr": "Jésus répondit: Il est écrit: L'homme ne vivra pas de pain seulement, mais de toute parole qui sort de la bouche de Dieu."
    },
    {
        "day": 1, "meal": "L",
        "ko": "주의 말씀은 내 발에 등이요 내 길에 빛이니이다",
        "en": "Your word is a lamp for my feet, a light on my path.",
        "zh": "你的话是我脚前的灯，是我路上的光。",
        "vi": "Lời Chúa là ngọn đèn cho chân tôi, Ánh sáng cho đường lối tôi.",
        "th": "พระวจนะของพระองค์เป็นโคมสำหรับเท้าของข้าพระองค์ และเป็นความสว่างแก่มรรคาของข้าพระองค์",
        "id": "Firman-Mu itu pelita bagi kakiku dan terang bagi jalanku.",
        "tl": "Ang salita mo ay ilawan sa aking mga paa, at liwanag sa aking landas.",
        "mn": "Таны үг миний хөл дэх дэнлүү, миний зам дахь гэрэл юм.",
        "si": "ඔබගේ වචනය මාගේ පාදවලට පහනක්ය, මාගේ මාවතට එළියක්ය.",
        "uz": "Sening kaloming qadamlarim uchun chiroqdir, Yo‘limga tushgan nurdir.",
        "ur": "تیرا کلام میرے پاؤں کے لئے چراغ اور میری راہ کے لئے روشنی ہے۔",
        "km": "ព្រះ‌បន្ទូល​ទ្រង់​ជា​ចង្កៀង​បំភ្លឺ​ជើង​ទូលបង្គំ ហើយ​ជា​ពន្លឺ​នៅ​តាម​ផ្លូវ​ទូលបង្គំ។",
        "bn": "তোমার বাক্য আমার পায়ের প্রদীপ ও আমার পথের আলোক।",
        "ky": "Сөзүңүз – менин бутума чырак, жолума жарык.",
        "ne": "तपाईंको वचन मेरो खुट्टाको निम्ति बत्ती र मेरो बाटोको निम्ति उज्यालो हो।",
        "my": "နှုတ်ကပတ်တော်သည် အကျွန်ုပ်ခြေရှေ့မှာ မီးခွက်ဖြစ်၍၊ အကျွန်ုပ်လမ်းခရီးကို လင်းစေပါ၏။",
        "lo": "ພຣະທຳ​ຂອງ​ພຣະອົງ​ເປັນ​ໂຄມໄຟ​ແກ່​ຕີນ​ຂອງ​ຂ້າພະອົງ ແລະ​ເປັນ​ແສງສະຫວ່າງ​ແກ່​ທາງ​ຂອງ​ຂ້າພະອົງ.",
        "tg": "Каломи Ту чароғест барои пойҳои ман, ва нурест барои роҳи ман.",
        "ru": "Слово Твое — светильник ноге моей и свет стезе моей.",
        "ar": "سِرَاجٌ لِرِجْلِي كَلاَمُكَ وَنُورٌ لِسَبِيلِي.",
        "es": "Lámpara es a mis pies tu palabra, Y lumbrera a mi camino.",
        "pt": "Lâmpada para os meus pés é tua palavra, e luz para o meu caminho.",
        "fr": "Ta parole est une lampe à mes pieds, Et une lumière sur mon sentier."
    },
    {
        "day": 1, "meal": "D",
        "ko": "이 율법책을 네 입에서 떠나지 말게 하며 주야로 그것을 묵상하여 그 안에 기록된 대로 다 지켜 행하라 그리하면 네 길이 평탄하게 될 것이며 네가 형통하리라",
        "en": "Keep this Book of the Law always on your lips; meditate on it day and night, so that you may be careful to do everything written in it.",
        "zh": "这律法书不可离开你的口，总要昼夜思想，好使你谨守遵行这书上所写的一切话。如此，你的道路就可以亨通，凡事顺利。",
        "vi": "Quyển sách luật pháp này chớ xa miệng ngươi, hãy suy gẫm ngày và đêm.",
        "th": "อย่าให้หนังสือธรรมบัญญัตินี้ห่างเหินไปจากปากของเจ้า แต่เจ้าจงตรึกตรองตามนั้นทั้งกลางวันและกลางคืน",
        "id": "Janganlah engkau lupa memperkatakan kitab Taurat ini, tetapi renungkanlah itu siang dan malam.",
        "tl": "Ang aklat na ito ng kautusan ay huwag mahihiwalay sa iyong bibig, kundi iyong pagbulay-bulayan araw at gabi.",
        "mn": "Хуулийн энэ номыг амнаасаа бүү салга. Түүнд бичигдсэн бүхнийг сахин биелүүлэхийн тулд өдөр шөнөгүй бясалга.",
        "si": "මේ ව්‍යවස්ථා පොත තාගේ කටින් අහක් නොවේවා, එහි ලියා තිබෙන සියල්ල රක්ෂාකර පැවැත්වීමට බලාගන්න පිණිស රෑ දාවල් ඒක මෙනෙහි කරපන්න.",
        "uz": "Tavrot kitobidagi so‘zlar tilingdan tushmasin. Unda yozilganlarning hammasiga rioya qilish uchun tunu kun uni o‘qi.",
        "ur": "شریعت کی یہ کتاب تیرے منہ سے نہ ہٹے بلکہ تجھے دن رات اِسی کا دھیان ہو تاکہ جو کچھ اِس میں لکھا ہے اُس سب پر تُو احتیاط کر کے عمل کر سکے۔",
        "km": "កុំ​ឲ្យ​គម្ពីរ​ក្រឹត្យ‌វិន័យ​នេះ​ឃ្លាត​ចេញ​ពី​មាត់​អ្នក​ឡើយ ត្រូវ​រិះ‌គិត​ពី​សេចក្ដី​នៅ​ក្នុង​នោះ​ទាំង​យប់​ទាំង​ថ្ងៃ",
        "bn": "ব্যবস্থার এই পুস্তকটি তোমার মুখ থেকে বিচ্যুত না হোক, কিন্তু তুমি দিনে ও রাতে তা ধ্যান কর।",
        "ky": "Бул мыйзам китеби оозуңдан түшпөсүн. Анда жазылгандардын бардыгын аткарыш үчүн, күнү-түнү ойлон.",
        "ne": "व्यवस्थाको यो पुस्तक तिम्रो ओठबाट नहटोस्, तर दिन र रात यसमाथि ध्यान् देओ",
        "my": "ဤပညတ္တိကျမ်းစာကို မဖတ်မရွတ်ဘဲမနေရ။ ကျမ်းစာ၌ ရေးထားသမျှအတိုင်း ကျင့်ဆောင်မည်အကြောင်း၊ နေ့ညဉ့်မပြတ် ကြံစည်ဆင်ခြင်ရမည်။",
        "lo": "ຢ່າ​ໃຫ້​ໜັງສື​ທຳມະບັນຍັດ​ນີ້​ຫ່າງ​ເຫີນ​ໄປ​ຈາກ​ປາກ​ຂອງ​ເຈົ້າ ແຕ່​ຈົ່ງ​ຕຶກຕອງ​ຕາມ​ນັ້ນ​ທັງ​ກາງເວັນ​ແລະ​ກາງຄືນ.",
        "tg": "Ин китоби шариат аз даҳони ту дур нашавад, ва шабу рӯз дар бораи он тафаккур намой, то ки ҳар он чиро, ки дар он навишта шудааст, иҷро кунӣ.",
        "ru": "Да не отходит сия книга закона от уст твоих; но поучайся в ней день и ночь, дабы в точности исполнять все, что в ней написано.",
        "ar": "لاَ يَبْرَحْ سِفْرُ هَذِهِ الشَّرِيعَةِ مِنْ فَمِكَ، بَلْ تَلْهَجُ فِيهِ نَهَاراً وَلَيْلاً، لِكَيْ تَتَحَفَّظَ لِلْعَمَلِ حَسَبَ كُلِّ مَا هُوَ مَكْتُوبٌ فِيهِ.",
        "es": "Nunca se apartará de tu boca este libro de la ley, sino que de día y de noche meditarás en él.",
        "pt": "Não se aparte da tua boca o livro desta lei; antes medita nele dia e noite, para que tenhas cuidado de fazer conforme a tudo quanto nele está escrito.",
        "fr": "Que ce livre de la loi ne s'éloigne point de ta bouche; médite-le jour et nuit, pour agir fidèlement selon tout ce qui y est écrit."
    },
]

def ensure_dirs():
    """23개 언어별 폴더 생성"""
    for lang in VOICES.keys():
        os.makedirs(os.path.join(AUDIO_DIR, lang), exist_ok=True)
    print(f"✓ 디렉토리 생성 완료: {len(VOICES)}개 언어")

async def generate_audio(text: str, voice: str, filepath: str):
    try:
        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(filepath)
        return "ok"
    except Exception as e:
        return f"error: {e}"

async def main():
    print("\n" + "=" * 60)
    print("🌍 MIGRANT56 V3.0 GLOCAL EDITION")
    print("   23개국 언어 성경 암송 오디오 생성 시작")
    print("=" * 60 + "\n")
    
    ensure_dirs()
    
    jobs = []
    for v in VERSES:
        day = v["day"]
        meal = v["meal"]
        file_id = f"M56-D{day:02d}-{meal}"
        
        for lang, voice in VOICES.items():
            text = v.get(lang, "")
            if text:
                filepath = os.path.join(AUDIO_DIR, lang, f"{file_id}-{lang}.mp3")
                jobs.append((text, voice, filepath, f"{file_id}-{lang}"))
    
    print(f"📊 총 {len(jobs)}개 파일 생성 예정...")
    
    created = 0
    errors = 0
    
    for i in range(0, len(jobs), 5):
        batch = jobs[i:i+5]
        for text, voice, filepath, name in batch:
            result = await generate_audio(text, voice, filepath)
            if result == "ok":
                created += 1
                print(f"✓ {name}")
            else:
                errors += 1
                print(f"✗ {name}: {result}")
        print(f"  ...진행 중 ({min(i+5, len(jobs))}/{len(jobs)})")

    print("\n" + "=" * 60)
    print("✅ 생성 완료!")
    
    index = {
        "version": "3.0",
        "program": "MIGRANT56 GLOCAL",
        "total_languages": len(VOICES),
        "languages": list(VOICES.keys()),
        "files": []
    }
    
    for v in VERSES:
        day = v["day"]
        meal = v["meal"]
        file_id = f"M56-D{day:02d}-{meal}"
        entry = {"id": file_id, "day": day, "meal": meal, "texts": {}, "audio": {}}
        for lang in VOICES.keys():
            if v.get(lang):
                entry["texts"][lang] = v[lang]
                entry["audio"][lang] = f"{lang}/{file_id}-{lang}.mp3"
        index["files"].append(entry)
        
    with open(os.path.join(AUDIO_DIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())