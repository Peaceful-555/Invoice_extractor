## Getting Started

To run the Invoice extractor application locally, follow these steps:
1. Create a folder and open terminal from this folder

### Clone the Repository
2. Run this command to clone the repository - git clone https://github.com/Peaceful-555/invoicedetailsextractor.git

3. Create a virtual environment and activate it:

python -m venv venv

cd venv

-On Windows, use Scripts\activate to activate the venv

cd ..
cd invoicedetailsextractor

4. Install the required packages:

pip install -r requirements.txt

5. Run database migrations:

python manage.py makemigrations

python manage.py migrate

6. Start the development server:

python manage.py runserver

Now you can upload the image or pdf files to extract the details from the Invoice, this application uses Gemini-1.5 API to perforn data extraction.
