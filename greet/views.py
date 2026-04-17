import json
import os
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash') 


def index(request):
    return render(request, 'greet/index.html')


@csrf_exempt
def generate_greeting(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()

            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)

            prompt = f"""
            Write a short, warm and friendly greeting message for {name}.
            Maximum 15-20 words. Add 1-2 relevant emojis.
            Only return the greeting message, nothing else.
            """

            response = model.generate_content(prompt)
            greeting = response.text.strip()

            return JsonResponse({'greeting': greeting})

        except Exception as e:
            print("=== GEMINI ERROR ===")
            print(type(e).__name__, ":", str(e))
            
            fallback = f"Hello {name}! Welcome! Have a wonderful day! ✨"
            return JsonResponse({'greeting': fallback})

    return JsonResponse({'error': 'Invalid method'}, status=405)