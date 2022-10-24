from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('qa_website', views.web_site, name='web_site'),
    path('qa', views.qa_web, name='qa_web'),
    path('mood', views.mood_web, name='mood_web'),
    path('score', views.score_web, name='score_web'),
    path('mood_website', views.sentiment_analysis_website, name='sentiment_analysis_website'),
    path('test', views.test, name='test'),
    path('get_request', views.get_request, name='get_request'),
    path('get_Mood', views.get_Mood, name='get_Mood'),
    path('get_score', views.get_score, name='get_score'),
    path('run_server_model', views.run_server_model, name='run_server_model'),
]