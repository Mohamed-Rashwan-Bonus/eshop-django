# عضو 2 — الحسابات والدخول (Authentication) — الشروط 1 ل 9

## 1. مهمتك ايه بالظبط
نظام اليوزرز كامل: تسجيل + دخول بالايميل + خروج + بروفايل + حماية الصفحات الخاصة. كل ملفاتك جوه فولدر accounts.

## 2. من الصفر خالص: يعني ايه اللي انت عملته
- Django جاي بيوزر جاهز بيدخل بـ username، لكن المطلوب دخول بالايميل + رقم موبايل مصري. فعملنا يوزر على مقاسنا اسمه CustomUser.
- USERNAME_FIELD يعني الحقل اللي Django بيدور بيه لما حد يدخل — خليناه email بدل username.
- الـ validator يعني شرط مكتوب على الحقل: لو متحققش الفورم تترفض. استخدمناه للموبايل المصري.
- الـ regex يعني pattern بيوصف شكل النص المقبول. بتاعنا `^01[0125][0-9]{8}$` معناه: يبدأ بـ 01 وبعدين رقم من (0 او 1 او 2 او 5) وبعدين 8 أرقام. يعني 010 و 011 و 012 و 015 بس.
- `@login_required` يعني حارس على باب الصفحة: مش مسجل دخول؟ اتحول لصفحة الدخول.

## 3. قاموس المصطلحات بتاعتك
- AbstractUser: اليوزر الجاهز اللي ورثنا منه كل حاجة وعدلنا عليه.
- unique=True: ممنوع التكرار على مستوى الداتابيز نفسها.
- ModelForm: فورم مبنية على موديل فبتورث شروطه تلقائيا.
- clean_email: دالة انت كتبتها بتتنادى لوحدها لما الفورم تتفحص.
- set_password: بتشفر الباسورد قبل الحفظ (عمره ما يتخزن نص صريح).
- IntegrityError: غلطة الداتابيز لما تحاول تدخل قيمة مكررة في حقل وحيد.
- 302: كود تحويل (redirect) لمكان تاني.

## 4. الكود سطر بسطر
### accounts/models.py
```
class CustomUser(AbstractUser):
```
- بنرث كل حاجة من يوزر Django (باسورد مشفر ودخول وخروج) ونعدل اللي محتاجينه.
```
    username = None
```
- لغينا حقل username خالص عشان المطلوب دخول بالايميل (شرط 6).
```
    email = models.EmailField(unique=True)
```
- الايميل وحيد على مستوى الداتابيز (شرط 3). حتى لو الفورم عدت حاجة، الداتابيز هتمنع التكرار.
```
    phone = models.CharField(max_length=16, validators=[validate_egyptian_phone])
```
- الموبايل بيتخزن 11 رقم بعد التنضيف (شرط 5). والـ 16 عشان المستخدم يقدر يكتب +20 أو مسافات.
- الفالديشن على 3 مستويات: الشكل (010/011/012/015 + 8 أرقام)، رفض الأرقام المكررة (00000000)، ورفض المتسلسلة (12345678). و+20 والمسافات بيتنضفوا تلقائيا ويتخزنوا 01.
- نفس القاعدة مطبقة على موبايل الشحن في الـ checkout (موبايل فيك = الأوردر مرفوض).
```
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
```
- الدخول بالايميل. والحقول المطلوبة عند إنشاء سوبر يوزر من التيرمنال (شرط 2).

### accounts/forms.py
```
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(...)
```
- الباسورد بيظهر كنقط مش حروف، وأقل طول 8.
```
    def clean_email(self):
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered...')
```
- لو الايميل متسجل (حتى باختلاف كابيتال وسمول) الفورم تترفض برسالة لطيفة بدل صفحة خطأ (شرط 3).
```
    def clean(self):
        if data.get('password') != data.get('confirm_password'):
            raise forms.ValidationError('Password confirmation does not match.')
```
- الباسورد لازم يطابق التأكيد (شرط 4).

### accounts/views.py
```
    if request.user.is_authenticated:
        return redirect('catalog:product_list')
```
- اللي مسجل دخول ميدخلش على صفحة التسجيل تاني.
```
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
```
- commit=False يعني جهز اليوزر من غير حفظ عشان نشفر الباسورد الأول.
```
        try:
            user.save()
        except IntegrityError:
            form.add_error('email', 'This email was just registered...')
```
- حماية السباق: لو اتنين داسوا تسجيل بنفس الايميل في نفس الثانية، التاني يشوف رسالة مش صفحة 500. دي كانت bug حقيقية واتصلحت واتجربت.
```
@login_required
def profile_view(request):
```
- صفحة البروفايل للأعضاء بس (شرط 8). وcheckout وتاريخ الأوردرات عليهم نفس الحارس (شرط 9): الزائر بيتحول للدخول بكود 302.

## 5. مربوط بمين
- عضو 1: فعل AUTH_USER_MODEL بتاعك.
- عضو 6: بياخد request.user عشان يعرف صاحب الأوردر.
- عضو 8: جرب كل حالاتك.

## 6. فيديوهات تذاكر منها
- Corey Schafer: حلقة Login/Logout (رقم 7) وحلقة Profile (رقم 8) من نفس السلسلة:
- https://www.youtube.com/playlist?list=PLLtIxaRk6P3JRiiW1SAV2BLhuuSSCULRn
- كورس Django كامل بالعربي (Programming Secrets) — فيه المصادقة والفورم:
- https://www.youtube.com/playlist?list=PLp2eAGIFKMEVnAAJWhGzLc1Nn-tFP1UHP
- شرح Custom User Model مكتوب بالعربي:
- https://thecodefix.net/learn/django/00-intro

## 7. أسئلة مناقشة متوقعة
- س: الباسورد متخزن ازاي؟ ج: مشفر بـ PBKDF2 عن طريق set_password ومستحيل يظهر حتى للأدمن.
- س: ليه لغيتوا username؟ ج: المطلوب دخول بالايميل، وحقل زيادة ملوش لازمة.
- س: اتنين سجلوا بنفس الايميل مع بعض؟ ج: الأولى تعدي والتانية تتمسك في clean_email، ولو عدت الـ IntegrityError بيتمسك في الـ view.
- س: 019 مقبول؟ ج: لا، الـ pattern بيقبل 010 و011 و012 و015 بس.

## 8. العرض اللايف بتاعك
1. سجل بموبايل غلط وورّي رسالة الخطأ.
2. سجل بنفس الايميل مرتين وورّي رسالة التكرار.
3. افتح checkout من غير دخول وورّي التحويل لصفحة Login.
