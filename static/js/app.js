// File input handling
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadForm = document.getElementById('uploadForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoader = submitBtn.querySelector('.btn-loader');

fileInput.addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        fileName.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
    } else {
        fileName.textContent = '';
    }
});

// Form submission
uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        showError('Please select a PDF file');
        return;
    }

    // Get selected formats
    const formatCheckboxes = document.querySelectorAll('input[name="formats"]:checked');
    if (formatCheckboxes.length === 0) {
        showError('Please select at least one export format');
        return;
    }

    // Disable form and show loader
    setLoading(true);
    hideResults();

    // Prepare form data
    const formData = new FormData();
    formData.append('file', file);
    formatCheckboxes.forEach(checkbox => {
        formData.append('formats[]', checkbox.value);
    });

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showResults(data);
        } else {
            showError(data.error || 'Processing failed. Please try again.');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        setLoading(false);
    }
});

// Show results
function showResults(data) {
    document.getElementById('resultSection').style.display = 'block';
    document.getElementById('errorSection').style.display = 'none';
    document.querySelector('.upload-section').style.display = 'none';

    // Populate results
    document.getElementById('transactionCount').textContent = data.transaction_count;
    
    // Handle account holder name - show N/A if null or empty
    const accountHolderName = data.account_details.account_holder_name;
    document.getElementById('accountHolder').textContent = accountHolderName && accountHolderName.trim() !== '' 
        ? accountHolderName.trim() 
        : 'N/A';
    
    // Handle account number
    const accountNumber = data.account_details.account_number;
    document.getElementById('accountNumber').textContent = accountNumber && accountNumber.trim() !== ''
        ? maskAccountNumber(accountNumber)
        : 'N/A';

    // Create download links
    const downloadLinks = document.getElementById('downloadLinks');
    downloadLinks.innerHTML = '';

    for (const [format, fileInfo] of Object.entries(data.output_files)) {
        const link = document.createElement('a');
        link.href = fileInfo.download_url;
        link.className = 'download-btn';
        link.innerHTML = `
            <span>📥</span>
            <span>Download ${format.toUpperCase()}</span>
        `;
        downloadLinks.appendChild(link);
    }

    // Scroll to results
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
}

// Show error
function showError(message) {
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorMessage').textContent = message;
    
    // Scroll to error
    document.getElementById('errorSection').scrollIntoView({ behavior: 'smooth' });
}

// Hide results
function hideResults() {
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
}

// Reset form
function resetForm() {
    uploadForm.reset();
    fileName.textContent = '';
    document.querySelector('.upload-section').style.display = 'block';
    hideResults();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Set loading state
function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    fileInput.disabled = isLoading;
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function maskAccountNumber(accountNumber) {
    if (!accountNumber || accountNumber === 'N/A') return 'N/A';
    const digits = accountNumber.replace(/\D/g, '');
    if (digits.length <= 4) return '*'.repeat(digits.length);
    return '*'.repeat(digits.length - 4) + digits.slice(-4);
}

// Drag and drop support
const uploadCard = document.querySelector('.upload-card');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadCard.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadCard.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadCard.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    uploadCard.style.border = '2px dashed var(--primary-color)';
    uploadCard.style.backgroundColor = 'rgba(31, 78, 120, 0.05)';
}

function unhighlight(e) {
    uploadCard.style.border = '';
    uploadCard.style.backgroundColor = '';
}

uploadCard.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        fileInput.files = files;
        const event = new Event('change');
        fileInput.dispatchEvent(event);
    }
}
