from __future__ import unicode_literals

from django.db import models
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

class SearchManager(models.Manager):
    def search_validator(self, postData):
        errors = {}
        if len(postData['search']) == 0:
            errors["search"] = "Please enter a search query."
            return errors


class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        get_email = User.objects.filter(email=postData['email'])


        if len(postData['email']) == 0:
            errors["no_email"] = "Please enter your email"
        if (len(get_email) == 0):
            errors["email_does_not_exist"] = "Email does not exist."
            return errors
        else:
            get_stored_pw = get_email.first().hash_pw

            if len(postData['password']) == 0:
                errors["no_password"] = "Please enter your password."
            if bcrypt.checkpw(postData['password'].encode(), get_stored_pw.encode()) == False:
                errors["wrong_password"] = "Incorrect password."
            return errors

    def reg_validator(self, postData):
        errors = {}
        get_email = User.objects.filter(email=postData['email'])

        #email exists:
        if len(get_email) > 0:
            errors["email_exists"] = "Email already exists."

        #LENGTHS
        if len(postData['first']) < 2:
            errors["first_length"] = "First name must be longer than 2 characters"
        if len(postData['last']) < 4:
            errors["last_length"] = "Last must be longer than 4 characters"
        if len(postData['email']) == 0:
            errors["no_email"] = "Please enter your email"
        if len(postData['password']) < 8:
            errors["no_password"] = "Your password must be greater than 8 characters."
        if len(postData['confirm-password']) == 0 :
            errors["no_confirm"] = "Please confirm your password."

        #FORMAT
        if all(letter.isalpha() for letter in postData['first']) == False:
            errors["first_format"] = "Your first name must only contain letters."
        if all(letter.isalpha() for letter in postData['last']) == False:
            errors["last_format"] = "Your last must only contain letters."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email_format"] = "Please enter a valid email."
        if not PASSWORD_REGEX.match(postData['password']):
            errors["password_format"] = "Your password must contain at least 1 uppercase letter and 1 lowercase letter, and 1 special character."
        #Password
        if (postData['password'] != postData['confirm-password']):
            errors['password_confirm'] = "Your password confirmation does not match."

        return errors

class User(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hash_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "first: " + self.first + ", last: " + self.last +  ", Email: " + self.email + ", Date Added: "\
        + str(self.created_at) + ", saved images: " + str(self.saved_images)

    objects = UserManager()


class Collection(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="collections")

    def __unicode__(self):
        return "ID: " + str(self.id) + ", name: " + self.name +  ", creator: " + str(self.creator) + ", saved images: " + str(self.images)


class SavedImage(models.Model):
    unsplash_data = models.TextField()
    saved_by = models.ForeignKey(User, related_name="saved_images")
    collection = models.ForeignKey(Collection, related_name="images")
    def __unicode__(self):
        return ", saved_by: " + str(self.saved_by) +  ", unsplash data: " + self.unsplash_data
