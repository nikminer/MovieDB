from django.forms import inlineformset_factory
from MyWatchList.models import UserList, UserListRecord

class UserListRecordForm(ModelForm):
    class Meta:
        model = UserListRecord
        exclude = ()

UserListFormSet = inlineformset_factory(
  UserList,
  UserListRecord,
  form=UserListRecordForm,
  extra=1,
)