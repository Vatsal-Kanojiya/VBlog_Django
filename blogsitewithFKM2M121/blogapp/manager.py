from django.contrib.auth.base_user import BaseUserManager


'''
class UserManager(BaseUserManager):
    def create_user(self,user_name,password=None,**extra_fields):
        if not user_name:
            raise ValueError("Username is required")
        #extra_fields['email']=self.normalize_email(extra_fields['email'])
        user=self.model(user_name=user_name,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self,user_name,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if not user_name:
            raise ValueError("Username is required")
        
        user=self.model(user_name=user_name,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
'''


from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        email=self.normalize_email('email')
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if not email:
            raise ValueError("Email is required")
        
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return self.create_user(email,password,**extra_fields)