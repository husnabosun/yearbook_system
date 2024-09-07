import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Import users from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help=r'C:\Users\bosun.HšSNABOSUN\OneDrive\Belgeler\yearbook_excell.xlsx')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            user, created = User.objects.get_or_create(
                student_number=(int(row['student_number'])),
                defaults={
                    'username': row['username'],
                    'student_number': row['student_number'],
                    'password': str(row['password']),
                    'is_staff': row.get('is_staff', False),
                    'is_superuser': row.get('is_superuser', False),
                }
            )
            if created:
                user.set_password(str(row['password']))
                user.save()

        self.stdout.write(self.style.SUCCESS('Users have been successfully imported'))