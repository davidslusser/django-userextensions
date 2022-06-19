from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from userextensions.models import ServiceAccount


class Command(BaseCommand):
    help = 'Create service account'

    def __init__(self):
        self.opts = None
        super(Command, self).__init__()

    def add_arguments(self, parser):
        """ define command arguments """
        parser.add_argument('--username', type=str, help='name for new superuser')
        parser.add_argument('--group', type=str, help='group this service account will be a member of')
        parser.add_argument('--description', type=str, help='description of this service account')

    def handle(self, *args, **options):
        """ command entry point """
        self.opts = options

        if not self.opts['username']:
            print('Please provide a username.')
            return

        if not self.opts['group']:
            print('Please specify a group')
            return

        # first check if user exists
        if User.objects.filter(username=self.opts['username']):
            print(f"A users with the username {self.opts['username']} already exists; please specify a "
                  f"different username")
            return

        try:
            user, is_user_new = User.objects.get_or_create(username=self.opts['username'])
            group, is_group_new = Group.objects.get_or_create(name=self.opts['group'])
            group.user_set.add(user)
            srv_acct = ServiceAccount.objects.create(user=user, group=group, description=self.opts['description'])
            print(f'Successfully created service account {srv_acct}')
        except Exception as err:
            print(f'Failed to create service account {err} in group {group}')
