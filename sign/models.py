from django.db import models

class User(models.Model):
    user_id=models.CharField(max_length=32, unique=True, verbose_name='아이디', default='default')
    user_pw=models.CharField(max_length=128, verbose_name='비밀번호')
    user_name=models.CharField(max_length=32, unique=True, verbose_name='이름')
    user_register_dttm=models.DateTimeField(auto_now_add=True, verbose_name='계정 생성시간')
    
    #생성된 객체의 이름을 지정하는 메서드
    def __str__(self):
        return self.user_name
    
    class Meta:
    	#DB 테이블명
        db_table='user'
        #테이블 닉네임
        verbose_name='유저'
        verbose_name_plural='유저'