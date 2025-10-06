import os 
import django 
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crudEx.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User 

def setup_roles():

    group_names = ["Client" , "Employee"]

    for name in group_names:
        group , created = Group.objects.get_or_create(name=name)

        if created:
            print(f"Group '{name}' created.")
        else:
            print(f"Group '{name}' already exists.")

    
    try:
        user = User.objects.get(username="rafael")
        #user = User.objects.get(username=os.getenv("DJANGO_SUPERUSER_USERNAME"))
        employee_group = Group.objects.get(name="Employee")

        user.groups.add(employee_group)

        print(f"User '{user.username}' added to 'Employee' group.")

    except Exception as e:
        print(f"Error occurred: {e}")
    except User.DoesNotExist:
        print("Superuser does not exist. Please create a superuser first.")
    except Group.DoesNotExist:
        print("Employee group does not exist.")

    
if __name__ == "__main__":
    setup_roles()