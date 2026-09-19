# عضو 2 — الحسابات والدخول (Authentication) — الشروط 1 ل 9

## 1. مهمتك ايه بالظبط
نظام اليوزرز كامل: تسجيل + دخول بالايميل + خروج + بروفايل + حماية الصفحات الخاصة. ملفاتك كلها جوه فولدر `accounts`.

## 2. المفاهيم اللي لازم تعرف تشرحها
- Django فيه يوزر جاهز (username + password) لكن احنا محتاجين دخول بالايميل + موبايل، فعملنا CustomUser.
- USERNAME_FIELD يعني الحقل اللي Django بيدور بيه عند الدخول — خليناه email.
- الـ validator يعني شرط بيترفض لو متحققش، واستخدمناه للموبايل المصري بالـ regex.
- الـ decorator زي `@login_required` يعني حارس على باب الـ view: مش مسجل؟ روح سجل الأول.

## 3. الملفات بتاعتك سطر بسطر
### accounts/models.py — اليوزر المخصص
```
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, validators=[egyptian_phone])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
```
- لغينا username خالص (شرط 6: الدخول بالايميل).
- email وحيد على مستوى الداتابيز (شرط 3).
- الموبايل لازم يطابق `^01[0125][0-9]{8}$` يعني 010 او 011 او 012 او 015 وبعده 8 أرقام (شرط 5).

### accounts/forms.py — فورم التسجيل
```
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(...)
    def clean_email(self):
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered...')
```
- شرط 2: كل الحقول موجودة في الفورم.
- شرط 4: `clean` بتقارن الباسورد بالتأكيد.
- شرط 3 (طبقة تانية): `clean_email` بتمنع التكرار برسالة لطيفة بدل صفحة خطأ.

### accounts/views.py — المنطق
```
def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:product_list')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        try:
            user.save()
        except IntegrityError:
            form.add_error('email', 'This email was just registered...')
```
- `set_password` بتشفر الباسورد (عمره ما يتخزن نص صريح).
- الـ try/except دي حماية من السباق: لو اتنين داسوا تسجيل بنفس الايميل في نفس الثانية، التاني يشوف رسالة مش صفحة 500 (دي كانت bug حقيقية واتصلحت).
- `login_view` بتدخل بالايميل، و`logout_view` بتخرج، و`profile_view` عليها `@login_required` (شرط 8).
- شرط 9: صفحات checkout و order history عليهم login_required فالزائر بيتحول لصفحة الدخول (302).

## 4. انت مربوط بمين
- عضو 1: فعل لك AUTH_USER_MODEL في settings.
- عضو 6 (Checkout): اعتمد عليك في `request.user` ومعرفة مين صاحب الأوردر.
- عضو 8: جرب كل حالاتك (موبايل غلط، ايميل مكرر، دخول غلط).

## 5. أسئلة مناقشة متوقعة
- س: الباسورد متخزن ازاي؟ ج: مشفر بـ PBKDF2 عن طريق set_password، ومستحيل يظهر حتى للأدمن.
- س: ليه لغيتوا username؟ ج: عشان المطلوب دخول بالايميل، ووجود username كان هيعمل حقل زيادة ملوش لازمة.
- س: لو حد سجل بنفس الايميل مرتين بسرعة؟ ج: الأولى بتعدي والتانية بتتمسك في clean_email، ولو عدت (سباق) الـ IntegrityError بيتمسك في الـ view.
- س: الـ 019 مقبول؟ ج: لا، الـ regex بيقبل 010 و011 و012 و015 بس زي شبكات مصر.

## 6. العرض اللايف بتاعك (دقيقتين)
1. سجل يوزر جديد بموبايل غلط وورّي رسالة الخطأ.
2. سجل بنفس الايميل مرتين وورّي رسالة التكرار.
3. جرب تفتح checkout من غير دخول وورّي التحويل لصفحة Login.
