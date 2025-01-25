from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from users.models import ClientUserModel
import helpers
# from polls.models import Question as Poll


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--user_id", default=-1, type=int)

    def handle(self, *args, **options):
        user_id = options['user_id']
        
        if user_id == -1:
            self.stdout.write("Creating client_user_model for all admin accounts\n")
            # get all user superuser
            for u in User.objects.filter(is_superuser=True):
                if not hasattr(u, "client_user"):
                    self.stdout.write("\tCreating client_user_model instance for superuser %s\n" % u.username)
                    if len(u.email) == 0:
                        self.stdout.write("\t\tUnable to create client_user_model instance for superuser %s -> Email not found\n" % u.username)
                        continue
                    client_user = ClientUserModel.objects.create(user_id=helpers.create_variable_hash(u.email), auth_user=u)
                    self.stdout.write("\t\tCreated client_user_model instance for superuser %s\n" % u.username)
        else:
            self.stdout.write("Creating client_user_model for given user_id accounts\n")