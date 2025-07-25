from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .embedder import extract_text_from_pdf, chunk_text, embed_and_store
from .rag_engine import stream_llm_response
from .pdf_reader import get_context_from_vectorstore

import os
from django.conf import settings

#Main UI View for handles PDF upload
def chatbot_ui(request):
    context = {}
    if request.method == "POST" and request.FILES.get("pdf_file"):
        pdf_file = request.FILES["pdf_file"]

        # Ensure upload directory exists
        upload_dir = os.path.join(settings.BASE_DIR, "uploaded_pdfs")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, pdf_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        # Process the uploaded PDF
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        collection_name = pdf_file.name.replace(".pdf", "")
        embed_and_store(chunks, collection_name=collection_name)

        context["msg"] = f"✅ PDF uploaded and indexed: {pdf_file.name}"
        context["collection_name"] = collection_name

    return render(request, "chatbot/index.html", context)

#Streaming Chat Response View
def stream_chat_response(request):
    query = request.GET.get("q", "")
    context = get_context_from_vectorstore(query)

    def event_stream():
        for token in stream_llm_response(query, context):
            yield f"data: {token}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


#API for uploading via JS (JSON response)
@csrf_exempt
def handle_pdf_upload(request):
    if request.method == "POST" and request.FILES.get("pdf_file"):
        uploaded_file = request.FILES["pdf_file"]

        upload_dir = os.path.join(settings.BASE_DIR, "uploaded_pdfs")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            text = extract_text_from_pdf(file_path)
            chunks = chunk_text(text)
            collection_name = uploaded_file.name.replace(".pdf", "")
            embed_and_store(chunks, collection_name=collection_name)

            return JsonResponse({
                "status": "success",
                "message": "PDF uploaded and indexed.",
                "collection": collection_name
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "No PDF uploaded."})
