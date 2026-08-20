# Bank Statement Processing & Classification System

A production-ready system for processing bank statements (text-based and scanned PDFs), extracting transactions, classifying them using non-LLM methods, and exporting to Excel/CSV.

> 📄 **For detailed technical documentation, development journey, and problem-solving approaches, see [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)**

## Features

✅ **PDF Processing**: Text-based and scanned (OCR) PDFs  
✅ **Auto-detection**: Automatically detects PDF type  
✅ **Transaction Extraction**: Date, description, debit, credit, balance  
✅ **Account Details**: Name, account number, IFSC, branch  
✅ **Classification**: Rules + ML (non-LLM) with 21 categories  
✅ **LLM Extraction**: Optional GPT-4/Claude/Gemini for any bank format  
✅ **Export**: Excel (multi-sheet) and CSV  
✅ **Web Interface**: Drag & drop upload with real-time processing  
✅ **Security**: Input validation, PII masking, encryption support  

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For OCR support (optional)
# macOS: brew install tesseract
# Ubuntu: sudo apt-get install tesseract-ocr
```

### 2. Train ML Model

```bash
python scripts/generate_training_data.py
python scripts/train_classifier.py
```

### 3. Run

**CLI:**
```bash
python -m src.main sample_pdfs/sample_statement_text_based.pdf
```

**Web Interface:**
```bash
./start_web.sh  # On Windows: start_web.bat
# Open http://localhost:5000
```

## Configuration

Edit `config/config.yaml`:

### Extraction Method

```yaml
extraction:
  method: "traditional"  # Options: traditional, llm, hybrid
```

- **traditional**: Free, works for standard formats
- **llm**: GPT-4/Claude/Gemini for any format (~$0.01-0.05/statement)
- **hybrid**: Try traditional first, use LLM if needed

### LLM Setup (Optional)

```yaml
extraction:
  method: "llm"
  llm:
    provider: "google"  # Options: openai, anthropic, google
    model: "gemini-2.5-flash"
    api_key_env: "GOOGLE_API_KEY"
```

Get API keys:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google: https://aistudio.google.com/app/apikey (FREE tier!)

```bash
export GOOGLE_API_KEY='your-key-here'
```

## Project Structure

```
bank-statement-processor/
├── app.py                      # Web application
├── config/
│   ├── config.yaml            # System configuration
│   └── category_keywords.json # Classification rules
├── src/
│   ├── main.py                # CLI entry point
│   ├── pipeline.py            # Main orchestrator
│   ├── ingestion/             # PDF loading & detection
│   ├── extraction/            # Text/OCR/LLM extraction
│   ├── classification/        # Rules + ML classifier
│   ├── export/                # Excel/CSV export
│   ├── security/              # Validation, PII masking
│   └── utils/                 # Config, logging
├── models/                    # Trained ML models
├── sample_pdfs/               # Test files
├── outputs/                   # Processed results
└── templates/                 # Web UI templates
```

## Classification

**Non-LLM approach as per requirements:**

1. **Rule-based** (keyword matching) - 21 categories
2. **ML fallback** (TF-IDF + Logistic Regression)
3. **Fallback** to "Uncategorized"

Categories: Salary, Rent, Groceries, Food & Dining, Shopping, Transport, Entertainment, Investment, Loan/EMI, Utilities, Healthcare, Education, Insurance, Travel, Cash Withdrawal/Deposit, Transfer, Interest, Refund, Subscription, Tax, Credit Card Payment

## Web Interface

- **Upload**: Drag & drop or click to select PDF
- **Process**: Automatic extraction and classification
- **Download**: Excel and CSV exports
- **Mobile**: Responsive design

## Security

- File validation (PDF magic byte, size limits)
- Account number masking in logs
- Optional encryption for exports
- Secure filename handling
- No LLM usage for sensitive classification

## Testing

```bash
# CLI
python -m src.main sample_pdfs/sample_statement_text_based.pdf

# Tests
pytest tests/ -v
```

## Multi-Bank Support

### Traditional Method
- Uses header aliasing for different column names
- Supports ~40+ column name variations
- Works well for standard formats

### LLM Method (Recommended for production)
- Works with ANY bank format
- No template maintenance needed
- Cost: ~$0.01-0.05 per statement
- FREE with Google Gemini (1500 requests/day)

## Troubleshooting

**Issue**: Models not found  
**Solution**: Run `python scripts/train_classifier.py`

**Issue**: OCR not working  
**Solution**: Install Tesseract OCR

**Issue**: LLM extraction fails  
**Solution**: Check API key is set: `echo $GOOGLE_API_KEY`

**Issue**: Port 5000 in use  
**Solution**: Change port in `app.py` or kill existing process

## Production Deployment

```bash
# Install Gunicorn
pip install gunicorn

# Run
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Requirements

- Python 3.8+
- Tesseract OCR (for scanned PDFs)
- Poppler utils (for PDF to image conversion)

## License

MIT

## Assessment Compliance

✅ Accepts PDF bank statements (text & image)  
✅ Auto-detects PDF type  
✅ Extracts account details and transactions  
✅ **Non-LLM classification** (rules + traditional ML)  
✅ Exports to Excel and CSV  
✅ Handles edge cases and multiple formats  
✅ Security features implemented  

**Note**: LLM is used only for extraction (not prohibited), classification remains non-LLM as required.

