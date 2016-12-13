from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def register(self, request, fields):
        is_valid = True

        if len(fields["email"]) == 0:
            messages.error(request, "Email is required");
            is_valid = False

        # OTHER VALIDATIONS HERE

        users = User.objects.filter(email=fields["email"])

        if len(users) != 0:
            messages.error(request, "That user exists");
            is_valid = False

        if not is_valid:
            return False

        ####
        #### the form is valid
        ####

        hashpw = bcrypt.hashpw(fields["password"].encode("utf-8"), bcrypt.gensalt())

        user = User.objects.create(
            email = fields["email"],
            hashpw = hashpw
        );

        request.session["logged_in_as"] = user.id

        return True




    def login(self, request, fields):
        # no validation required

        users = User.objects.filter(email=fields["email"])

        if len(users) == 0:
            messages.error(request, "That user does not exist");
            return False;

        user = users[0]

        guesshash = bcrypt.hashpw(fields["password"].encode("utf-8"), user.hashpw.encode("utf-8"))

        if guesshash != user.hashpw:
            messages.error(request, "That is the incorrect password");
            return False

        request.session["logged_in_as"] = user.id

        return True;


class User(models.Model):
    email = models.CharField(max_length=100)
    hashpw = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
