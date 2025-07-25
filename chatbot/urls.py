from django.urls import path
from .views import chatbot_ui, stream_chat_response, handle_pdf_upload
from .api_views import ask_question

urlpatterns = [
    path("", chatbot_ui, name="chat_ui"),
    path("api/ask/", ask_question, name="api_ask"),
    path("api/upload/", handle_pdf_upload, name="api_pdf_upload"),
    path("stream/", stream_chat_response, name="stream_chat"),
]

