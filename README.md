# Mənzillərin Qiymət Proqnozlaşdırılması Layihəsi

!['asdasd'](https://www.investopedia.com/thmb/rkx-DcijTK4xDkm6DX45854cS6o=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/TipsforUsingAIToBuyaHome-v1-c5ca80ec76b841ddaa0e436c8bd4bc26.png)

Bu layihə, Bakı şəhərindəki mənzillərin qiymətlərini proqnozlaşdırmağa yönəlmiş bir maşın öyrənməsi modelinin inkişafını əhatə edir. Layihə, müxtəlif xüsusiyyətlərə əsaslanaraq mənzilin satış qiymətini dəqiq təxmin etməyə imkan verir. 

## **Layihənin Təsviri**

**Məqsəd:** Bu layihə, daşınmaz əmlak bazarındakı qiymət dəyişkənliyini anlamaq və müəyyən xüsusiyyətlərdən istifadə edərək mənzilin satış qiymətini proqnozlaşdırmaq üçün yüksək performanslı bir maşın öyrənməsi modeli qurmağı hədəfləyir.

**Əsas Xüsusiyyətlər:**
- Mənzilin sahəsi
- Otaq sayı
- Mərtəbə
- Tikili yaşı
- Təmir vəziyyəti və digər əhəmiyyətli məlumatlar

## **Layihədə istifadə olunan məlumatlar**

Layihə, aşağıdakı sütunları ehtiva edən bir məlumat dəstəsi istifadə edir:

- **price**: Mənzilin satış qiyməti (hədəf dəyişən).
- **location**: Mənzilin yerləşdiyi ərazi.
- **rooms**: Mənzildəki otaq sayı.
- **square**: Mənzilin ümumi sahəsi (m²).
- **floor**: Mənzilin yerləşdiyi mərtəbə.
- **new_building**: Mənzilin yeni tikili olub-olmaması (Bəli/Xeyr).
- **has_repair**: Mənzildə təmirin olub-olmaması (Bəli/Xeyr).
- **has_bill_of_sale**: Satış sənədinin olub-olmaması (Bəli/Xeyr).
- **has_mortgage**: İpoteka imkanının olub-olmaması (Bəli/Xeyr).

## **İstifadəçi Qeydləri**

1. **Məlumat Dəstəsi**: Layihədə istifadə olunan məlumatlar CSV formatında təqdim olunub və Streamlit tətbiqinin sağ tərəf menyusundan yüklənə bilər.
   
2. **Streamlit İnteqrasiyası**: Bu layihə, istifadəçilərə mənzil qiymətləri haqqında məlumat verən və analizlər edən bir veb tətbiqi təqdim edir. Streamlit tətbiqi ilə vizualizasiyalar və məlumatlar asanlıqla təqdim edilir.

3. **Proqnozlaşdırma Modeli**: Bu layihə proqnozlaşdırma modelinin qurulması məqsədini güdür və mənzil qiymətlərini dəqiq təxmin etmək üçün daha da inkişaf etdirilə bilər.

## **İstifadə və Quraşdırma**

1. **Asılılıqlar**:
   - Streamlit
   - Plotly
   - Pandas

2. **Quraşdırma**:
   - Python 3.12.0 versiyası ilə işləyir.
   - `requirements.txt` faylından istifadə edərək asılılıqları quraşdırın:
     ```
     pip install -r requirements.txt
     ```

## **Tətbiqin Faydaları**

- **Alıcılar üçün üstünlüklər**: Mənzil alarkən müxtəlif xüsusiyyətlər əsasında qiymətləri müqayisə etməyə kömək edir.
- **Satıcılar üçün üstünlüklər**: Mənzilin bazar dəyərini daha yaxşı anlamağa dəstək olur.
- **Sektor üçün üstünlüklər**: Daşınmaz əmlak bazarında daha məlumatlı qərarlar qəbul edilməsini təmin edir.
