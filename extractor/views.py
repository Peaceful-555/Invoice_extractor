import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key='AIzaSyAWJDgqrgtDyc1Ie7anYiYvl4KFkAgGp40')
model = genai.GenerativeModel('gemini-1.5-flash')

def home(request):
  return render(request, 'extractor/home.html')

def extract_text_from_pdf(file):
  document = fitz.open(stream=file.read(), filetype="pdf")
  text = ""
  for page in document:
      text += page.get_text()
  return text

def extract_text_from_image(file):
  image = Image.open(file)
  text = pytesseract.image_to_string(image)
  return text

def extract_details_from_text(text):
  # Generate content using the Gemini API
  prompt = f"""
  Extract the following details from the invoice text:
  1. Customer Details (Name, Billing Address, Shipping Address)
  2. Products (Description, HSN/SAC, Rate, Quantity, Amount, IGST, Total Amount)
  3. Total Amount (Final amount payable)
  
  Here is the invoice text:
  {text}
  """

  response = model.generate_content(prompt)
  return response.text

def extract(request):
  if request.method == 'POST' and request.FILES['file']:
      file = request.FILES['file']
      if file.name.endswith('.pdf'):
          text = extract_text_from_pdf(file)
      elif file.name.endswith(('.png', '.jpg', '.jpeg')):
          text = extract_text_from_image(file)
      else:
          return JsonResponse({'error': 'Unsupported file type'}, status=400)

      # Get the raw response from the Gemini API
      details = extract_details_from_text(text)

      # Render the raw response directly in the result template
      return render(request, 'extractor/result.html', {'details': details})

  return JsonResponse({'error': 'No file uploaded'}, status=400)