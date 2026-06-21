# 🛠️ Хэрэгслүүд

Энэ хавтаст Instagram/Facebook хөгжүүлэхэд туслах жижиг программууд байна.

## 📅 content_planner.py — Контент төлөвлөгч

Постын санаа, хуваарийг хадгалж удирдана. Мэдээлэл нь `content.json`-д хадгалагдана.

```bash
python3 tools/content_planner.py add "Постын санаа" 2026-06-25   # санаа нэмэх
python3 tools/content_planner.py list                            # хуваарь харах
python3 tools/content_planner.py done 1                          # дууссан гэж тэмдэглэх
python3 tools/content_planner.py remove 1                        # устгах
```

## 🎨 make_fb_images.py — Facebook зураг үүсгэгч

Нил ягаан дэвсгэр + лотос + "Өөрийгөө хайрлахуй" уран бичмэлтэй
cover болон профайл зураг үүсгэнэ. Үр дүн нь `images/` хавтаст хадгалагдана.

```bash
python3 tools/make_fb_images.py
```

> Тэмдэглэл: энэ нь Pacifico фонт ашигладаг (`.fonts/` хавтаст автоматаар татагдана).
