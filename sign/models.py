from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, email, password, username, nickname, gender, birth_date, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            password=password,
            username=username,
            nickname=nickname,
            gender=gender,
            birth_date=birth_date,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성'),
        ('N', '미지정')
    )
    USER_TYPE_CHOICES = (
        ('Sun', '태양형'),
        ('Jupiter', '목성형'),
        ('Comet', '혜성형'),
        ('Earth', '지구형'),
        ('Moon', '달형'),
        ('Saturn', '토성형'),
        ('White', '화이트홀형'),
        ('Black', '블랙홀형'),
    )

    user_id = models.CharField(max_length=32, unique=True, verbose_name='아이디', default='default')
    user_pw = models.CharField(max_length=128, verbose_name='비밀번호')
    username = models.CharField(max_length=32, unique=True, verbose_name='이름')
    user_register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='계정 생성시간')
    nickname = models.CharField(max_length=50, unique=True, verbose_name='닉네임')
    birth_date = models.DateField(verbose_name='생년월일', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name='프로필 사진')

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email']
    
    bio = models.TextField(max_length=500, blank=True) # 자기소개
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    def __str__(self):
        return self.username
    
    class Meta:
     	#DB 테이블명
         db_table='sign_customuser'
