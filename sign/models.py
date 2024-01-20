from django.db import models

# Create your models here.
class User(models.Model):
    user_email=models.CharField(max_length=32, unique=True, verbose_name='이메일')
    user_pw=models.CharField(max_length=128, verbose_name='비밀번호')
    user_name=models.CharField(max_length=32, unique=True, verbose_name='이름')
    user_register_dttm=models.DateTimeField(auto_now_add=True, verbose_name='계정 생성시간')
    
    #생성된 객체의 이름을 지정하는 메서드
    def __str__(self):
        return self.user_name
    
    class Meta:
    	#DB 테이블명
        db_table='user'
        #테이블 
        verbose_name='유저'
        verbose_name_plural='유저'
