import os
import pwd
import grp
import crypt
import pam

from rest_framework import serializers

from models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)
    last_login = serializers.CharField(read_only=True)
    date_joined = serializers.CharField(read_only=True)

    files = serializers.HyperlinkedRelatedField(many=True, view_name='file-detail', read_only=True)

    def create_user_dir(self, username):
        print 'Creating user directory...'
        uid = pwd.getpwnam(username).pw_uid
        gid = grp.getgrnam(username).gr_gid
        print uid
        path = 'media/storage/' + username + '/'
        print "Path: ", path
        if not os.path.exists(path):
            print "Path: ", path, " doesn\'t exists!"
            os.makedirs(path)
            print "Path created!!"
            print "Giving user permissions to path..."
            os.chown(path, uid, gid)
            print "User permissions ok!"
        print 'User directory created!'

    def validate(self, validated_data):
        """
        0. If 'password' in validated_data, it is a sign up request, differently user must provide a bearer token in headers
        1. User has already account in OS -- Register user in app db
        2. Username exists in OS but password is wrong -- Raise Validation error
        3. User has not account in OS and username doesn't exist in OS -- Register user in OS and in app db
            OS user account has its password encrypted with crypt.crypt(password, "22")
            App user account has its password encrypted by django
        """
        if 'password' in validated_data:
            print "Validate user registration in OS"
            p = pam.pam()
            print validated_data['password']
            has_os_account = p.authenticate(validated_data['username'], validated_data['password'])
            print "has_os_account: " + str(has_os_account)
            if not has_os_account:
                username_in_os = False
                for username in pwd.getpwall():
                    if username[0] == str(validated_data['username']):
                        username_in_os = True
                        break
                if username_in_os:
                    raise serializers.ValidationError("Username in OS -- wrong password")
                print "username_in_os: " + str(username_in_os)
                enc_pass = crypt.crypt(validated_data['password'], "22")
                try:
                    if os.system("useradd -p " + enc_pass + " " + validated_data['username']) == 0:
                        print "User created in OS"
                        # If user OS account created
                        # -- application user account will be created
                        # -- user directory under his/her permissions will be created at: media/storage/<username>
                        self.create_user_dir(validated_data['username'])
                    else:
                        print "OS user account cannot be created"
                except:
                    print "Internal server error -- User account creation"
            else:
                # If user has OS account but not in application database
                # -- application user account will be created
                # -- user directory under his/her permissions will be created at: media/storage/<username>
                self.create_user_dir(validated_data['username'])
        return validated_data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('id','last_login', 'date_joined', 'username', 'password', 'email', 'files')
        #exclude = ('is_staff', 'is_superuser')