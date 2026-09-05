import os
import base64
import subprocess
import fitz  # PyMuPDF

WORK_DIR = r"c:\Users\mohdh\Desktop\Job Hunt\biodata"
ASSETS_DIR = os.path.join(WORK_DIR, "assets")

def to_base64(filepath):
    with open(filepath, "rb") as f:
        ext = os.path.splitext(filepath)[1].lower().replace(".", "")
        if ext == "jpg": ext = "jpeg"
        encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/{ext};base64,{encoded}"

# Load images
img_kurta = to_base64(os.path.join(ASSETS_DIR, "portrait_kurta.jpg"))
img_sherwani = to_base64(os.path.join(ASSETS_DIR, "traditional_sherwani.jpg"))
img_docu = to_base64(os.path.join(ASSETS_DIR, "documentary_iit_bombay.jpg"))

# ==============================================================================
# 1. SINGLE-PAGE EDITION (Airy, Spacious, Human Voice, Zero Em-Dashes)
# ==============================================================================
single_page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Marriage Biodata: Mohd Hayaat Ali</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@500;600;700&family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,500&display=swap" rel="stylesheet">

<style>
  @page {{
    size: A4 portrait;
    margin: 0;
  }}
  
  *, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Outfit', sans-serif;
    color: #2D3748;
    background-color: #E2E8F0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page {{
    width: 210mm;
    height: 297mm;
    position: relative;
    background: #FCFAF7;
    margin: 0 auto;
    overflow: hidden;
    page-break-inside: avoid;
    display: flex;
    flex-direction: column;
    padding: 12mm 15mm;
  }}

  /* Refined Gold Border */
  .page-border {{
    position: absolute;
    top: 5mm;
    left: 5mm;
    right: 5mm;
    bottom: 5mm;
    border: 1.2px solid #C8B38E;
    pointer-events: none;
    z-index: 10;
  }}

  .page-border-inner {{
    position: absolute;
    top: 7mm;
    left: 7mm;
    right: 7mm;
    bottom: 7mm;
    border: 0.6px solid rgba(200, 179, 142, 0.4);
    pointer-events: none;
    z-index: 10;
  }}

  .corner-ornament {{
    position: absolute;
    width: 20px;
    height: 20px;
    border: 2px solid #B8934A;
    pointer-events: none;
    z-index: 11;
  }}
  .corner-tl {{ top: 5.5mm; left: 5.5mm; border-right: none; border-bottom: none; }}
  .corner-tr {{ top: 5.5mm; right: 5.5mm; border-left: none; border-bottom: none; }}
  .corner-bl {{ bottom: 5.5mm; left: 5.5mm; border-right: none; border-top: none; }}
  .corner-br {{ bottom: 5.5mm; right: 5.5mm; border-left: none; border-top: none; }}

  /* Header */
  .header {{
    text-align: center;
    margin-bottom: 12px;
  }}

  .bismillah {{
    font-family: 'Amiri', serif;
    font-size: 20pt;
    color: #142E25;
    line-height: 1.2;
    margin-bottom: 2px;
  }}

  .bismillah-sub {{
    font-family: 'Cinzel', serif;
    font-size: 6.8pt;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    color: #8C734B;
    margin-bottom: 5px;
  }}

  .divider-motif {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 5px;
  }}

  .divider-line {{
    width: 65px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C5A059, transparent);
  }}

  .divider-symbol {{
    color: #B8934A;
    font-size: 8.5pt;
  }}

  .document-title {{
    font-family: 'Cinzel', serif;
    font-size: 13pt;
    letter-spacing: 4px;
    font-weight: 700;
    color: #142E25;
    text-transform: uppercase;
  }}

  /* Hero Profile Card */
  .hero-card {{
    background: #FFFFFF;
    border: 1px solid #E6DDCF;
    border-radius: 9px;
    padding: 13px 18px;
    display: flex;
    gap: 18px;
    align-items: center;
    box-shadow: 0 4px 14px rgba(20, 46, 37, 0.03);
    margin-bottom: 12px;
  }}

  .hero-photo-wrap {{
    position: relative;
    flex-shrink: 0;
  }}

  .hero-photo {{
    width: 112px;
    height: 142px;
    object-fit: cover;
    object-position: center 20%;
    border-radius: 7px;
    border: 2px solid #D6C29E;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    display: block;
  }}

  .hero-info {{
    flex-grow: 1;
  }}

  .hero-name {{
    font-family: 'Playfair Display', serif;
    font-size: 21pt;
    font-weight: 700;
    color: #112820;
    line-height: 1.15;
    margin-bottom: 3px;
  }}

  .hero-designation {{
    font-family: 'Cinzel', serif;
    font-size: 8.8pt;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #94723C;
    margin-bottom: 10px;
  }}

  .badges-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 6.5px;
    margin-bottom: 11px;
  }}

  .badge {{
    background: #F4EFE6;
    border: 1px solid #DFD5C3;
    padding: 3px 11px;
    border-radius: 16px;
    font-size: 7.8pt;
    font-weight: 600;
    color: #1B3F32;
    letter-spacing: 0.3px;
  }}

  .hero-quick-meta {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5.5px 16px;
    font-size: 8.3pt;
  }}

  .meta-item {{
    display: flex;
    align-items: baseline;
    gap: 6px;
  }}

  .meta-label {{
    color: #718096;
    font-weight: 500;
    min-width: 90px;
  }}

  .meta-value {{
    color: #1A202C;
    font-weight: 600;
  }}

  /* Grid 2 Columns */
  .grid-2col {{
    display: grid;
    grid-template-columns: 1fr 1.05fr;
    gap: 12px;
    margin-bottom: 11px;
  }}

  /* Section Card */
  .section-card {{
    background: #FFFFFF;
    border: 1px solid #E6DDCF;
    border-radius: 8px;
    padding: 12px 15px;
    box-shadow: 0 2px 8px rgba(20, 46, 37, 0.02);
    display: flex;
    flex-direction: column;
  }}

  .card-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #EFE6DA;
    padding-bottom: 6px;
    margin-bottom: 9px;
  }}

  .card-icon {{
    width: 14px;
    height: 14px;
    fill: #B8934A;
    flex-shrink: 0;
  }}

  .card-title {{
    font-family: 'Cinzel', serif;
    font-size: 8.8pt;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #142E25;
  }}

  .data-list {{
    display: flex;
    flex-direction: column;
    gap: 7px;
    font-size: 8.3pt;
  }}

  .data-row {{
    display: flex;
    line-height: 1.38;
  }}

  .data-label {{
    width: 82px;
    flex-shrink: 0;
    color: #718096;
    font-weight: 500;
  }}

  .data-value {{
    flex-grow: 1;
    color: #1A202C;
    font-weight: 600;
  }}

  .data-sub {{
    display: block;
    font-size: 7.4pt;
    font-weight: 400;
    color: #556977;
    margin-top: 2px;
    line-height: 1.32;
  }}

  /* Prose Text (Human Voice) */
  .prose-text {{
    font-size: 8.2pt;
    line-height: 1.54;
    color: #374151;
    text-align: justify;
  }}

  .prose-text p + p {{
    margin-top: 6px;
  }}

  /* Subtle In-Card Footnote / Metadata */
  .meta-sub-row {{
    margin-top: 8px;
    padding-top: 6px;
    border-top: 1px dashed #EFE6DA;
    font-size: 7.6pt;
    color: #556977;
    display: flex;
    gap: 12px;
  }}

  .meta-sub-item {{
    display: flex;
    gap: 4px;
  }}

  .meta-sub-item strong {{
    color: #142E25;
    font-weight: 600;
  }}

  /* Seamless Open Du'a Banner (No heavy box, airy & spiritual) */
  .dua-section {{
    text-align: center;
    padding: 10px 18px;
    margin-top: 2px;
    margin-bottom: 12px;
    border-top: 1px solid rgba(200, 179, 142, 0.35);
    border-bottom: 1px solid rgba(200, 179, 142, 0.35);
    background: rgba(255, 255, 255, 0.4);
    border-radius: 6px;
  }}

  .dua-arabic {{
    font-family: 'Amiri', serif;
    font-size: 15pt;
    color: #142E25;
    line-height: 1.4;
    margin-bottom: 3px;
    direction: rtl;
  }}

  .dua-english {{
    font-family: 'Outfit', sans-serif;
    font-size: 7.6pt;
    font-style: italic;
    color: #4A5568;
    line-height: 1.35;
    max-width: 90%;
    margin: 0 auto 3px auto;
  }}

  .dua-ref {{
    font-family: 'Cinzel', serif;
    font-size: 6.4pt;
    letter-spacing: 1.5px;
    color: #94723C;
    text-transform: uppercase;
    font-weight: 600;
  }}

  /* Contact Strip */
  .contact-strip {{
    background: #112820;
    color: #F7FAFC;
    border-radius: 7px;
    padding: 11px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1.2px solid #B8934A;
    margin-top: auto;
  }}

  .contact-col {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .contact-col-title {{
    font-family: 'Cinzel', serif;
    font-size: 6.8pt;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #D6C29E;
  }}

  .contact-col-val {{
    font-size: 9.5pt;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 0.4px;
  }}
</style>
</head>
<body>

  <div class="page">
    <div class="page-border"></div>
    <div class="page-border-inner"></div>
    <div class="corner-ornament corner-tl"></div>
    <div class="corner-ornament corner-tr"></div>
    <div class="corner-ornament corner-bl"></div>
    <div class="corner-ornament corner-br"></div>

    <!-- Header -->
    <header class="header">
      <div class="bismillah">بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>
      <div class="bismillah-sub">In the Name of Allah, the Most Gracious, the Most Merciful</div>
      <div class="divider-motif">
        <div class="divider-line"></div>
        <span class="divider-symbol">✦ ❖ ✦</span>
        <div class="divider-line"></div>
      </div>
      <h1 class="document-title">Marriage Biodata</h1>
    </header>

    <!-- Hero Card -->
    <section class="hero-card">
      <div class="hero-photo-wrap">
        <img class="hero-photo" src="{img_kurta}" alt="Mohd Hayaat Ali">
      </div>
      <div class="hero-info">
        <h2 class="hero-name">Mohd Hayaat Ali</h2>
        <div class="hero-designation">Creative Director • Crevia Media</div>
        <div class="badges-row">
          <span class="badge">Age: 28 Yrs</span>
          <span class="badge">Height: 6' 3" (190 cm)</span>
          <span class="badge">Sunni Muslim (Khan)</span>
          <span class="badge">Never Married</span>
        </div>
        <div class="hero-quick-meta">
          <div class="meta-item">
            <span class="meta-label">Date of Birth:</span>
            <span class="meta-value">8th June 1998</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Native Roots:</span>
            <span class="meta-value">Mirzapur, Uttar Pradesh</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Current Work Base:</span>
            <span class="meta-value">Delhi NCR</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Current Hometown:</span>
            <span class="meta-value">Allahabad / Prayagraj, UP</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Row 1: Education & Career | Family Details -->
    <div class="grid-2col">
      <!-- Education & Career -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3z M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/></svg>
          <span class="card-title">Education & Career</span>
        </div>
        <div class="data-list">
          <div class="data-row">
            <span class="data-label">Education:</span>
            <div class="data-value">
              Bachelor of Business Administration (BBA)
              <span class="data-sub">Sam Higginbottom University of Agriculture, Technology and Sciences (SHUATS), Naini, Prayagraj</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Profession:</span>
            <span class="data-value">Creative Director</span>
          </div>
          <div class="data-row">
            <span class="data-label">Company:</span>
            <span class="data-value">Crevia Media</span>
          </div>
          <div class="data-row">
            <span class="data-label">Work Base:</span>
            <span class="data-value">Delhi NCR</span>
          </div>
        </div>
        <div class="meta-sub-row">
          <div class="meta-sub-item"><strong>Languages:</strong> English, Urdu, Hindi</div>
          <div class="meta-sub-item"><strong>Diet:</strong> Halal</div>
        </div>
      </div>

      <!-- Family Details -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
          <span class="card-title">Family Details</span>
        </div>
        <div class="data-list">
          <div class="data-row">
            <span class="data-label">Father:</span>
            <div class="data-value">
              Late Naushad Ahmad Khan
              <span class="data-sub">B.Sc, LL.B. (Allahabad University) • Carpet Manufacturing & Export</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Mother:</span>
            <div class="data-value">
              Mrs. Farah Deeba Khan
              <span class="data-sub">M.A., LL.B. (Shibli National College, Azamgarh) • Advocate & Homemaker</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Sister:</span>
            <div class="data-value">
              Namrah Ali
              <span class="data-sub">Businesswoman / Entrepreneur</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Hometown:</span>
            <span class="data-value" style="font-size:7.6pt; font-weight:500;">18B/3M/1A, Karamat Chowki, Kareli, Allahabad (Prayagraj)</span>
          </div>
        </div>
        <div class="meta-sub-row">
          <div class="meta-sub-item"><strong>Family Roots:</strong> Mirzapur, UP</div>
        </div>
      </div>
    </div>

    <!-- Row 2: About Me | Partner Expectations (Human Voice, No AI Cliches) -->
    <div class="grid-2col">
      <!-- About Me -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
          <span class="card-title">About Me</span>
        </div>
        <div class="prose-text">
          <p>
            I work as a Creative Director in Delhi. Most of my work involves leading creative teams and designing digital products, while outside of work, I document human stories through photography and filmmaking.
          </p>
          <p>
            Faith and family are central to how I live. I take my work and personal growth seriously, but I try to keep my priorities straight, believing that barakah, peace of mind, and honest effort matter much more than speed or noise.
          </p>
        </div>
      </div>

      <!-- Partner Expectations -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
          <span class="card-title">Partner Vision & Values</span>
        </div>
        <div class="prose-text">
          <p>
            I am looking for a partner who values mutual respect, emotional maturity, and shared Islamic values. Someone who communicates with adab, has a kind nature, and values the sincere commitment of marriage.
          </p>
          <p>
            I appreciate someone who is ambitious yet grounded in faith, looking forward to building a calm, supportive home together with patience and understanding.
          </p>
        </div>
      </div>
    </div>

    <!-- Open, Spiritual Du'a Banner -->
    <div class="dua-section">
      <div class="dua-arabic">رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا</div>
      <p class="dua-english">"Our Lord, grant us from among our spouses and offspring comfort to our eyes and make us an example for the righteous."</p>
      <div class="dua-ref">Surah Al-Furqan • 25:74</div>
    </div>

    <!-- Contact Strip -->
    <div class="contact-strip">
      <div class="contact-col">
        <span class="contact-col-title">Family Contact (Mother: Mrs. Farah Deeba Khan)</span>
        <span class="contact-col-val">+91 72679 17767</span>
      </div>
      <div class="contact-col" style="text-align: right;">
        <span class="contact-col-title">Hometown & Family Residence</span>
        <span class="contact-col-val">Kareli, Allahabad (Prayagraj), UP</span>
      </div>
    </div>
  </div>

</body>
</html>
"""

# ==============================================================================
# 2. 2-PAGE EDITION (Human Voice, Zero Em-Dashes, 2 Generous Photos)
# ==============================================================================
two_page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Marriage Biodata: Mohd Hayaat Ali</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@500;600;700&family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,500&display=swap" rel="stylesheet">

<style>
  @page {{
    size: A4 portrait;
    margin: 0;
  }}
  
  *, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Outfit', sans-serif;
    color: #2D3748;
    background-color: #E2E8F0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page {{
    width: 210mm;
    height: 297mm;
    position: relative;
    background: #FCFAF7;
    margin: 0 auto;
    overflow: hidden;
    page-break-after: always;
    page-break-inside: avoid;
    display: flex;
    flex-direction: column;
    padding: 12mm 15mm;
  }}

  /* Refined Gold Border */
  .page-border {{
    position: absolute;
    top: 5mm;
    left: 5mm;
    right: 5mm;
    bottom: 5mm;
    border: 1.2px solid #C8B38E;
    pointer-events: none;
    z-index: 10;
  }}

  .page-border-inner {{
    position: absolute;
    top: 7mm;
    left: 7mm;
    right: 7mm;
    bottom: 7mm;
    border: 0.6px solid rgba(200, 179, 142, 0.4);
    pointer-events: none;
    z-index: 10;
  }}

  .corner-ornament {{
    position: absolute;
    width: 20px;
    height: 20px;
    border: 2px solid #B8934A;
    pointer-events: none;
    z-index: 11;
  }}
  .corner-tl {{ top: 5.5mm; left: 5.5mm; border-right: none; border-bottom: none; }}
  .corner-tr {{ top: 5.5mm; right: 5.5mm; border-left: none; border-bottom: none; }}
  .corner-bl {{ bottom: 5.5mm; left: 5.5mm; border-right: none; border-top: none; }}
  .corner-br {{ bottom: 5.5mm; right: 5.5mm; border-left: none; border-top: none; }}

  /* Header */
  .header {{
    text-align: center;
    margin-bottom: 12px;
  }}

  .bismillah {{
    font-family: 'Amiri', serif;
    font-size: 20pt;
    color: #142E25;
    line-height: 1.2;
    margin-bottom: 2px;
  }}

  .bismillah-sub {{
    font-family: 'Cinzel', serif;
    font-size: 6.8pt;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    color: #8C734B;
    margin-bottom: 5px;
  }}

  .divider-motif {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 5px;
  }}

  .divider-line {{
    width: 65px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C5A059, transparent);
  }}

  .divider-symbol {{
    color: #B8934A;
    font-size: 8.5pt;
  }}

  .document-title {{
    font-family: 'Cinzel', serif;
    font-size: 13pt;
    letter-spacing: 4px;
    font-weight: 700;
    color: #142E25;
    text-transform: uppercase;
  }}

  /* Hero Profile Card */
  .hero-card {{
    background: #FFFFFF;
    border: 1px solid #E6DDCF;
    border-radius: 9px;
    padding: 13px 18px;
    display: flex;
    gap: 18px;
    align-items: center;
    box-shadow: 0 4px 14px rgba(20, 46, 37, 0.03);
    margin-bottom: 12px;
  }}

  .hero-photo-wrap {{
    position: relative;
    flex-shrink: 0;
  }}

  .hero-photo {{
    width: 112px;
    height: 142px;
    object-fit: cover;
    object-position: center 20%;
    border-radius: 7px;
    border: 2px solid #D6C29E;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    display: block;
  }}

  .hero-info {{
    flex-grow: 1;
  }}

  .hero-name {{
    font-family: 'Playfair Display', serif;
    font-size: 21pt;
    font-weight: 700;
    color: #112820;
    line-height: 1.15;
    margin-bottom: 3px;
  }}

  .hero-designation {{
    font-family: 'Cinzel', serif;
    font-size: 8.8pt;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #94723C;
    margin-bottom: 10px;
  }}

  .badges-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 6.5px;
    margin-bottom: 11px;
  }}

  .badge {{
    background: #F4EFE6;
    border: 1px solid #DFD5C3;
    padding: 3px 11px;
    border-radius: 16px;
    font-size: 7.8pt;
    font-weight: 600;
    color: #1B3F32;
    letter-spacing: 0.3px;
  }}

  .hero-quick-meta {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5.5px 16px;
    font-size: 8.3pt;
  }}

  .meta-item {{
    display: flex;
    align-items: baseline;
    gap: 6px;
  }}

  .meta-label {{
    color: #718096;
    font-weight: 500;
    min-width: 90px;
  }}

  .meta-value {{
    color: #1A202C;
    font-weight: 600;
  }}

  /* Grid 2 Columns */
  .grid-2col {{
    display: grid;
    grid-template-columns: 1fr 1.05fr;
    gap: 12px;
    margin-bottom: 11px;
  }}

  /* Section Card */
  .section-card {{
    background: #FFFFFF;
    border: 1px solid #E6DDCF;
    border-radius: 8px;
    padding: 12px 15px;
    box-shadow: 0 2px 8px rgba(20, 46, 37, 0.02);
    display: flex;
    flex-direction: column;
  }}

  .card-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #EFE6DA;
    padding-bottom: 6px;
    margin-bottom: 9px;
  }}

  .card-icon {{
    width: 14px;
    height: 14px;
    fill: #B8934A;
    flex-shrink: 0;
  }}

  .card-title {{
    font-family: 'Cinzel', serif;
    font-size: 8.8pt;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #142E25;
  }}

  .data-list {{
    display: flex;
    flex-direction: column;
    gap: 7px;
    font-size: 8.3pt;
  }}

  .data-row {{
    display: flex;
    line-height: 1.38;
  }}

  .data-label {{
    width: 82px;
    flex-shrink: 0;
    color: #718096;
    font-weight: 500;
  }}

  .data-value {{
    flex-grow: 1;
    color: #1A202C;
    font-weight: 600;
  }}

  .data-sub {{
    display: block;
    font-size: 7.4pt;
    font-weight: 400;
    color: #556977;
    margin-top: 2px;
    line-height: 1.32;
  }}

  /* Prose Text (Human Voice) */
  .prose-text {{
    font-size: 8.2pt;
    line-height: 1.54;
    color: #374151;
    text-align: justify;
  }}

  .prose-text p + p {{
    margin-top: 6px;
  }}

  /* Subtle In-Card Footnote */
  .meta-sub-row {{
    margin-top: 8px;
    padding-top: 6px;
    border-top: 1px dashed #EFE6DA;
    font-size: 7.6pt;
    color: #556977;
    display: flex;
    gap: 12px;
  }}

  .meta-sub-item {{
    display: flex;
    gap: 4px;
  }}

  .meta-sub-item strong {{
    color: #142E25;
    font-weight: 600;
  }}

  /* Contact Strip */
  .contact-strip {{
    background: #112820;
    color: #F7FAFC;
    border-radius: 7px;
    padding: 12px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1.2px solid #B8934A;
    margin-top: auto;
  }}

  .contact-col {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .contact-col-title {{
    font-family: 'Cinzel', serif;
    font-size: 6.8pt;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #D6C29E;
  }}

  .contact-col-val {{
    font-size: 9.5pt;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 0.4px;
  }}

  /* ============================================================ */
  /* PAGE 2 STYLES: 2-PHOTO PORTFOLIO & REFLECTIONS               */
  /* ============================================================ */

  .gallery-header {{
    text-align: center;
    margin-bottom: 14px;
  }}

  .gallery-title {{
    font-family: 'Cinzel', serif;
    font-size: 14pt;
    letter-spacing: 3.5px;
    font-weight: 700;
    color: #142E25;
    text-transform: uppercase;
  }}

  .gallery-sub {{
    font-family: 'Outfit', sans-serif;
    font-size: 8pt;
    color: #8C734B;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-top: 2px;
  }}

  /* 2-Column Gallery Grid */
  .gallery-grid-2col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 16px;
  }}

  .gallery-card {{
    background: #FFFFFF;
    border: 1px solid #E6DBC9;
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 16px rgba(20, 46, 37, 0.05);
  }}

  .gallery-img-wrap {{
    height: 164mm;
    overflow: hidden;
    position: relative;
    background: #EAE6DF;
  }}

  .gallery-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center top;
    display: block;
  }}

  .gallery-caption {{
    padding: 11px 14px;
    text-align: center;
    background: #FFFFFF;
    border-top: 1px solid #F0EAE1;
  }}

  .caption-tag {{
    font-family: 'Cinzel', serif;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 1.3px;
    color: #142E25;
    text-transform: uppercase;
    display: block;
    margin-bottom: 2.5px;
  }}

  .caption-sub {{
    font-size: 7.5pt;
    color: #718096;
  }}

  /* Dua Banner */
  .dua-banner {{
    background: #FFFFFF;
    border: 1px solid #DFD2BD;
    border-radius: 8px;
    padding: 13px 20px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(20, 46, 37, 0.035);
    margin-top: auto;
    margin-bottom: 10px;
  }}

  .dua-arabic {{
    font-family: 'Amiri', serif;
    font-size: 16.5pt;
    color: #142E25;
    line-height: 1.5;
    margin-bottom: 4px;
    direction: rtl;
  }}

  .dua-english {{
    font-family: 'Outfit', sans-serif;
    font-size: 8pt;
    font-style: italic;
    color: #4A5568;
    line-height: 1.45;
    max-width: 90%;
    margin: 0 auto 4px auto;
  }}

  .dua-ref {{
    font-family: 'Cinzel', serif;
    font-size: 6.8pt;
    letter-spacing: 1.6px;
    color: #94723C;
    text-transform: uppercase;
    font-weight: 600;
  }}

  .gallery-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #E2D9CC;
    padding-top: 8px;
    font-size: 7.8pt;
    color: #64748B;
  }}
</style>
</head>
<body>

  <!-- PAGE 1: CORE BIODATA -->
  <div class="page">
    <div class="page-border"></div>
    <div class="page-border-inner"></div>
    <div class="corner-ornament corner-tl"></div>
    <div class="corner-ornament corner-tr"></div>
    <div class="corner-ornament corner-bl"></div>
    <div class="corner-ornament corner-br"></div>

    <!-- Header -->
    <header class="header">
      <div class="bismillah">بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>
      <div class="bismillah-sub">In the Name of Allah, the Most Gracious, the Most Merciful</div>
      <div class="divider-motif">
        <div class="divider-line"></div>
        <span class="divider-symbol">✦ ❖ ✦</span>
        <div class="divider-line"></div>
      </div>
      <h1 class="document-title">Marriage Biodata</h1>
    </header>

    <!-- Hero Card -->
    <section class="hero-card">
      <div class="hero-photo-wrap">
        <img class="hero-photo" src="{img_kurta}" alt="Mohd Hayaat Ali">
      </div>
      <div class="hero-info">
        <h2 class="hero-name">Mohd Hayaat Ali</h2>
        <div class="hero-designation">Creative Director • Crevia Media</div>
        <div class="badges-row">
          <span class="badge">Age: 28 Yrs</span>
          <span class="badge">Height: 6' 3" (190 cm)</span>
          <span class="badge">Sunni Muslim (Khan)</span>
          <span class="badge">Never Married</span>
        </div>
        <div class="hero-quick-meta">
          <div class="meta-item">
            <span class="meta-label">Date of Birth:</span>
            <span class="meta-value">8th June 1998</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Native Roots:</span>
            <span class="meta-value">Mirzapur, Uttar Pradesh</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Current Work Base:</span>
            <span class="meta-value">Delhi NCR</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Current Hometown:</span>
            <span class="meta-value">Allahabad / Prayagraj, UP</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Row 1: Education & Career | Family Details -->
    <div class="grid-2col">
      <!-- Education & Career -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3z M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/></svg>
          <span class="card-title">Education & Career</span>
        </div>
        <div class="data-list">
          <div class="data-row">
            <span class="data-label">Education:</span>
            <div class="data-value">
              Bachelor of Business Administration (BBA)
              <span class="data-sub">Sam Higginbottom University of Agriculture, Technology and Sciences (SHUATS), Naini, Prayagraj</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Profession:</span>
            <span class="data-value">Creative Director</span>
          </div>
          <div class="data-row">
            <span class="data-label">Company:</span>
            <span class="data-value">Crevia Media</span>
          </div>
          <div class="data-row">
            <span class="data-label">Work Base:</span>
            <span class="data-value">Delhi NCR</span>
          </div>
        </div>
        <div class="meta-sub-row">
          <div class="meta-sub-item"><strong>Languages:</strong> English, Urdu, Hindi</div>
          <div class="meta-sub-item"><strong>Diet:</strong> Halal</div>
        </div>
      </div>

      <!-- Family Details -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
          <span class="card-title">Family Details</span>
        </div>
        <div class="data-list">
          <div class="data-row">
            <span class="data-label">Father:</span>
            <div class="data-value">
              Late Naushad Ahmad Khan
              <span class="data-sub">B.Sc, LL.B. (Allahabad University) • Carpet Manufacturing & Export</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Mother:</span>
            <div class="data-value">
              Mrs. Farah Deeba Khan
              <span class="data-sub">M.A., LL.B. (Shibli National College, Azamgarh) • Advocate & Homemaker</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Sister:</span>
            <div class="data-value">
              Namrah Ali
              <span class="data-sub">Businesswoman / Entrepreneur</span>
            </div>
          </div>
          <div class="data-row">
            <span class="data-label">Hometown:</span>
            <span class="data-value" style="font-size:7.6pt; font-weight:500;">18B/3M/1A, Karamat Chowki, Kareli, Allahabad (Prayagraj)</span>
          </div>
        </div>
        <div class="meta-sub-row">
          <div class="meta-sub-item"><strong>Family Roots:</strong> Mirzapur, UP</div>
        </div>
      </div>
    </div>

    <!-- Row 2: About Me | Partner Expectations (Human Voice, No AI Cliches) -->
    <div class="grid-2col">
      <!-- About Me -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
          <span class="card-title">About Me</span>
        </div>
        <div class="prose-text">
          <p>
            I work as a Creative Director in Delhi. Most of my work involves leading creative teams and designing digital products, while outside of work, I document human stories through photography and filmmaking.
          </p>
          <p>
            Faith and family are central to how I live. I take my work and personal growth seriously, but I try to keep my priorities straight, believing that barakah, peace of mind, and honest effort matter much more than speed or noise.
          </p>
        </div>
      </div>

      <!-- Partner Expectations -->
      <div class="section-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
          <span class="card-title">Partner Vision & Values</span>
        </div>
        <div class="prose-text">
          <p>
            I am looking for a partner who values mutual respect, emotional maturity, and shared Islamic values. Someone who communicates with adab, has a kind nature, and values the sincere commitment of marriage.
          </p>
          <p>
            I appreciate someone who is ambitious yet grounded in faith, looking forward to building a calm, supportive home together with patience and understanding.
          </p>
        </div>
      </div>
    </div>

    <!-- Contact Strip -->
    <div class="contact-strip">
      <div class="contact-col">
        <span class="contact-col-title">Family Contact (Mother: Mrs. Farah Deeba Khan)</span>
        <span class="contact-col-val">+91 72679 17767</span>
      </div>
      <div class="contact-col" style="text-align: right;">
        <span class="contact-col-title">Hometown & Family Residence</span>
        <span class="contact-col-val">Kareli, Allahabad (Prayagraj), UP</span>
      </div>
    </div>
  </div>

  <!-- PAGE 2: PHOTO GALLERY & REFLECTIONS (2 PHOTOS) -->
  <div class="page">
    <div class="page-border"></div>
    <div class="page-border-inner"></div>
    <div class="corner-ornament corner-tl"></div>
    <div class="corner-ornament corner-tr"></div>
    <div class="corner-ornament corner-bl"></div>
    <div class="corner-ornament corner-br"></div>

    <!-- Gallery Header -->
    <header class="gallery-header">
      <div class="bismillah-sub">Visual Portfolio</div>
      <h2 class="gallery-title">Photographic Profile</h2>
      <div class="divider-motif">
        <div class="divider-line"></div>
        <span class="divider-symbol">✦ ❖ ✦</span>
        <div class="divider-line"></div>
      </div>
      <p class="gallery-sub">Traditional Elegance • Creative Direction & Storytelling</p>
    </header>

    <!-- 2-Photo Gallery Grid -->
    <section class="gallery-grid-2col">
      <!-- Photo 1: Traditional Bandhgala -->
      <div class="gallery-card">
        <div class="gallery-img-wrap">
          <img class="gallery-img" src="{img_sherwani}" alt="Traditional Wear">
        </div>
        <div class="gallery-caption">
          <span class="caption-tag">Traditional Elegance</span>
          <span class="caption-sub">Festive Occasions & Family Functions</span>
        </div>
      </div>

      <!-- Photo 2: Documentary at IIT Bombay -->
      <div class="gallery-card">
        <div class="gallery-img-wrap">
          <img class="gallery-img" src="{img_docu}" alt="Directing at IIT Bombay" style="object-position: center 15%;">
        </div>
        <div class="gallery-caption">
          <span class="caption-tag">Direction & Storytelling</span>
          <span class="caption-sub">Filming a Documentary at IIT Bombay</span>
        </div>
      </div>
    </section>

    <!-- Quranic Du'a Banner -->
    <div class="dua-banner">
      <div class="dua-arabic">رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا</div>
      <p class="dua-english">"Our Lord, grant us from among our spouses and offspring comfort to our eyes and make us an example for the righteous."</p>
      <div class="dua-ref">Surah Al-Furqan • 25:74</div>
    </div>

    <!-- Gallery Footer -->
    <footer class="gallery-footer">
      <span><strong>Mohd Hayaat Ali</strong> • Marriage Biodata</span>
      <span>Family Contact (Mother): <strong>+91 72679 17767</strong></span>
      <span>Delhi NCR | Allahabad | Mirzapur</span>
    </footer>
  </div>

</body>
</html>
"""

# Write files
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 1. Generate Single Page
sp_html_path = os.path.join(WORK_DIR, "Mohd_Hayaat_Ali_Marriage_Biodata_SinglePage.html")
sp_pdf_path = os.path.join(WORK_DIR, "Mohd_Hayaat_Ali_Marriage_Biodata_SinglePage.pdf")
with open(sp_html_path, "w", encoding="utf-8") as f:
    f.write(single_page_html)

subprocess.run([
    edge_path, "--headless", "--disable-gpu", "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={sp_pdf_path}", "--no-pdf-header-footer", sp_html_path
], capture_output=True)

# Export Single Page HD PNG
doc_sp = fitz.open(sp_pdf_path)
print(f"Single page PDF page count: {len(doc_sp)}")
sp_png_path = os.path.join(WORK_DIR, "Mohd_Hayaat_Ali_Biodata_SinglePage_HD.png")
doc_sp[0].get_pixmap(dpi=300).save(sp_png_path)
doc_sp[0].get_pixmap(dpi=150).save(os.path.join(WORK_DIR, "single_page_preview.png"))
doc_sp.close()
print("Saved single page preview.")

# 2. Update 2-Page Version
tp_html_path = os.path.join(WORK_DIR, "Mohd_Hayaat_Ali_Marriage_Biodata.html")
tp_pdf_path = os.path.join(WORK_DIR, "Mohd_Hayaat_Ali_Marriage_Biodata.pdf")
with open(tp_html_path, "w", encoding="utf-8") as f:
    f.write(two_page_html)

subprocess.run([
    edge_path, "--headless", "--disable-gpu", "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={tp_pdf_path}", "--no-pdf-header-footer", tp_html_path
], capture_output=True)

# Export 2-Page HD PNGs
doc_tp = fitz.open(tp_pdf_path)
print(f"Two page PDF page count: {len(doc_tp)}")
doc_tp[0].get_pixmap(dpi=300).save(os.path.join(WORK_DIR, "Mohd_Hayaat_Ali_Biodata_Page_1_HD.png"))
doc_tp[1].get_pixmap(dpi=300).save(os.path.join(WORK_DIR, "Mohd_Hayaat_Ali_Biodata_Page_2_HD.png"))
doc_tp[0].get_pixmap(dpi=150).save(os.path.join(WORK_DIR, "page_1.png"))
doc_tp[1].get_pixmap(dpi=150).save(os.path.join(WORK_DIR, "page_2.png"))
doc_tp.close()
print("Saved two page preview.")
