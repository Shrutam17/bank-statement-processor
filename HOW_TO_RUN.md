# 🚀 How to Run the Bank Statement Processor Web App

## ⚡ Quick Start (Recommended)

### macOS/Linux:
```bash
./start_web.sh
```

### Windows:
```cmd
start_web.bat
```

That's it! The script handles everything automatically.

---

## 📋 What the Script Does

1. ✅ Checks virtual environment exists
2. ✅ Activates the virtual environment
3. ✅ Trains ML models if not present
4. ✅ Creates necessary directories
5. ✅ Starts the Flask web server
6. ✅ Shows you the access URL

---

## 🌐 Access the Application

Once the server starts, you'll see:
```
🚀 Starting web server...

Access the application at: http://localhost:5000
Press Ctrl+C to stop the server
```

Open your browser and go to: **http://localhost:5000**

---

## 📝 Step-by-Step Manual Run (Alternative)

If you prefer to run manually:

### 1. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### 2. Check Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train Models (First Time Only)
```bash
python scripts/generate_training_data.py
python scripts/train_classifier.py
```

### 4. Start the Server
```bash
python app.py
```

### 5. Open Browser
Navigate to: http://localhost:5000

---

## 🎯 Using the Application

### Upload PDF
1. Click **"Choose PDF File"** or drag & drop a PDF
2. Select export formats: **Excel**, **CSV**, or both
3. Click **"Process Statement"**

### View Results
After processing completes, you'll see:
- **Transactions Found**: Number of transactions extracted
- **Account Holder**: Name from the statement
- **Account Number**: Masked for security (****1234)

### Download Files
Click the download buttons to get:
- **Excel (.xlsx)**: With summary sheet and transaction details
- **CSV (.csv)**: Flat file with all data

### Process More
Click **"Process Another Statement"** to upload a new file

---

## 🧪 Test with Sample PDFs

Sample PDFs are located in `sample_pdfs/`:
- `sample_statement_text_based.pdf` - Regular PDF with text
- `sample_statement_scanned.pdf` - Scanned image PDF (OCR)

Upload these to test the application!

---

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## ⚠️ Troubleshooting

### Port 5000 Already in Use

**Problem**: Error about port 5000 being in use

**Solution 1** - Kill the existing process:
```bash
# Find the process
lsof -i :5000

# Kill it
kill -9 <PID>
```

**Solution 2** - Change the port in `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)  # Use 5001 instead
```

### Models Not Found

**Problem**: "Trained model not found" error

**Solution**: Train the models:
```bash
python scripts/generate_training_data.py
python scripts/train_classifier.py
```

### Tesseract Not Found (OCR Error)

**Problem**: OCR fails on scanned PDFs

**Solution**: Install Tesseract OCR:

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Virtual Environment Not Found

**Problem**: venv directory doesn't exist

**Solution**: Create it:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Flask Not Installed

**Problem**: "Flask not found" error

**Solution**: Install Flask:
```bash
pip install Flask==3.0.0
```

---

## 📊 What Happens Behind the Scenes

When you upload a PDF:

1. **File Validation** - Checks file type, size, and format
2. **PDF Type Detection** - Determines if text-based or scanned
3. **Data Extraction** - Uses pdfplumber (text) or Tesseract (OCR)
4. **Account Details** - Extracts name, account number, IFSC, branch
5. **Transaction Parsing** - Finds dates, amounts, descriptions
6. **Classification** - Categorizes using rules + ML (non-LLM)
7. **Export** - Generates Excel and CSV files
8. **Download Links** - Provides secure download URLs

---

## 🔒 Security Features

- ✅ Only PDF files accepted
- ✅ File size limits (50MB max)
- ✅ Magic byte validation
- ✅ Secure filename handling
- ✅ Account number masking in UI
- ✅ Automatic file cleanup
- ✅ Path traversal prevention

---

## 📱 Browser Compatibility

Works on:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

---

## 💡 Tips

- **Drag & Drop**: You can drag PDFs directly onto the upload area
- **Multiple Formats**: Select both Excel and CSV for maximum flexibility
- **Mobile**: The interface is mobile-friendly
- **Results**: Processed files are saved in `outputs/` folder

---

## 📚 More Information

- **Full Documentation**: See `README_WEB_APP.md`
- **Architecture**: See `docs/architecture_diagram.md`
- **Web Flow**: See `docs/web_app_flow.md`
- **System Details**: See main `README.md`

---

## 🎉 You're Ready!

Just run `./start_web.sh` (or `start_web.bat` on Windows) and start processing bank statements!

**Need Help?** Check the logs in `logs/app.log`
