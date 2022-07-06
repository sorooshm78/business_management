from django.urls import path

from record import views

urlpatterns = [
    path('del-record/<record_id>', views.del_record, name='del_record'),
    path('add-record/<repo_id>', views.CreateRecordView.as_view(), name='add_record'),
    path('update-record/<record_id>', views.UpdateRecordView.as_view(), name='update_record'),
    path('detail-record/<pk>', views.DetailRecordView.as_view(), name='detail_record'),
]
