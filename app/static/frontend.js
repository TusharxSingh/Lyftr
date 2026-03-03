// Frontend JavaScript for AI Web Scraper

document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const scrapeBtn = document.getElementById('scrapeBtn');
    const loading = document.getElementById('loading');
    const errorMsg = document.getElementById('errorMsg');
    const sectionsDiv = document.getElementById('sections');
    const jsonViewer = document.getElementById('jsonViewer');
    const jsonContent = document.getElementById('jsonContent');
    const downloadBtn = document.getElementById('downloadBtn');
    
    let currentData = null;
    
    scrapeBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        
        if (!url) {
            showError('Please enter a URL');
            return;
        }
        
        // Validate URL
        try {
            new URL(url);
        } catch (e) {
            showError('Invalid URL format');
            return;
        }
        
        // Reset UI
        hideError();
        sectionsDiv.innerHTML = '';
        jsonViewer.style.display = 'none';
        setLoading(true);
        
        try {
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Scraping failed');
            }
            
            const data = await response.json();
            currentData = data;
            
            displaySections(data.sections);
            displayJSON(data);
            
        } catch (error) {
            showError(error.message || 'An error occurred while scraping');
        } finally {
            setLoading(false);
        }
    });
    
    function setLoading(isLoading) {
        if (isLoading) {
            loading.classList.add('active');
            scrapeBtn.disabled = true;
        } else {
            loading.classList.remove('active');
            scrapeBtn.disabled = false;
        }
    }
    
    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.classList.add('active');
    }
    
    function hideError() {
        errorMsg.classList.remove('active');
    }
    
    function displaySections(sections) {
        sectionsDiv.innerHTML = '';
        
        if (sections.length === 0) {
            sectionsDiv.innerHTML = '<p>No sections found</p>';
            return;
        }
        
        sections.forEach((section, index) => {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = 'section';
            
            const header = document.createElement('div');
            header.className = 'section-header';
            header.innerHTML = `
                <span class="section-label">${section.label || `Section ${index + 1}`}</span>
                <span class="section-type">${section.type}</span>
            `;
            
            const content = document.createElement('div');
            content.className = 'section-content';
            content.innerHTML = `
                <p><strong>Content:</strong></p>
                <p>${section.content.substring(0, 500)}${section.truncated ? '...' : ''}</p>
                ${section.block.lists.length > 0 ? `<p><strong>Lists:</strong> ${section.block.lists.length}</p>` : ''}
                ${section.block.tables.length > 0 ? `<p><strong>Tables:</strong> ${section.block.tables.length}</p>` : ''}
                ${section.block.images > 0 ? `<p><strong>Images:</strong> ${section.block.images}</p>` : ''}
                ${section.block.links > 0 ? `<p><strong>Links:</strong> ${section.block.links}</p>` : ''}
            `;
            
            header.addEventListener('click', () => {
                content.classList.toggle('active');
            });
            
            sectionDiv.appendChild(header);
            sectionDiv.appendChild(content);
            sectionsDiv.appendChild(sectionDiv);
        });
    }
    
    function displayJSON(data) {
        jsonContent.textContent = JSON.stringify(data, null, 2);
        jsonViewer.style.display = 'block';
    }
    
    downloadBtn.addEventListener('click', () => {
        if (!currentData) return;
        
        const blob = new Blob([JSON.stringify(currentData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'scraped-data.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
    
    // Allow Enter key to trigger scrape
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            scrapeBtn.click();
        }
    });
});

