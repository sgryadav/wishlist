from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

NAME_REGEX = re.compile(r"(^[A-Z][-a-zA-Z]+$)")
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')


class usersManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}

        name = postData['reg_name']
        username = postData['reg_username']
        pass1 = postData['reg_pass1']
        pass2 = postData['reg_pass2']
        unidatehired = postData['reg_datehired']
        datehired = datetime.strptime(unidatehired,"%Y-%m-%d")
        current = datetime.now()
        limit = datetime(1900, 1, 1)


        if not NAME_REGEX.match(name):
            errors['name'] = "Name is invalid"

        if Users.objects.filter(username=username):
            errors['username_exist'] = "Username has been used"

        if not PASS_REGEX.match(pass1):
            errors['pass1'] = "Password is invalid"

        if pass1 != pass2:
            errors['pass2'] = "Password does not match"
        
        if limit >= datehired or datehired >= current:
            errors['datehired'] = "Datehired is not valid"

        return errors

    def log_validator(self, postData):
        errors = {}

        login_username = postData['login_username']
        login_pass = postData['login_pass']

        try:
            Users.objects.get(username=login_username)
            db_pass = Users.objects.get(username=login_username).password
            if not bcrypt.checkpw(login_pass.encode(), db_pass.encode()):
                errors['not_match'] = "Invalid password"
        except:
            errors['not_email'] = "Invalid username"

        return errors
    
class itemsManager(models.Manager):
    def item_validator(self, postData):
        errors = {}
        item_added = postData['itemtoadd']

        if len(item_added) < 4:
            errors['item name is less than 4 characters']
        
        return errors
    

class Users(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=35)
    password = models.CharField(max_length=30)
    datehired = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = usersManager()

class Items(models.Model):

    name = models.CharField(max_length=35)
    users = models.ManyToManyField(Users,related_name="items")
    added_by = models.ForeignKey(Users, related_name="item")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = itemsManager()


