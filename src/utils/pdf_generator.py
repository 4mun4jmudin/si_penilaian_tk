import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as ReportLabImage

def create_laporan_pdf(filepath, data):
    """
    Fungsi untuk men-generate file PDF Laporan Hasil Belajar.
    data: Dictionary berisi {nama, kelas, periode, hasil, guru}
    """
    
    # 1. Setup Dokumen
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_title = ParagraphStyle(
        name='Title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=10
    )
    style_subtitle = ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=12,
        spaceAfter=20
    )
    style_normal = styles['Normal']
    style_bold = ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='Helvetica-Bold')

    # 2. Kop Surat (Sederhana Teks)
    # Jika ada logo, bisa ditambahkan menggunakan ReportLabImage
    elements.append(Paragraph("YAYASAN PENDIDIKAN ISLAM", style_subtitle))
    elements.append(Paragraph("TK ISLAM PLUS MIFTAHUL JANNAH", style_title))
    elements.append(Paragraph("Jl. Adipati Agung No.40, Baleendah, Kab. Bandung", style_subtitle))
    elements.append(Spacer(1, 0.5*cm))
    
    # Garis Pembatas Kop
    # (Di ReportLab platypus agak tricky, kita pakai Table line saja atau HR manual)
    elements.append(Paragraph("_" * 65, style_subtitle))
    elements.append(Spacer(1, 1*cm))

    # 3. Judul Laporan
    elements.append(Paragraph("LAPORAN HASIL BELAJAR SISWA", style_title))
    elements.append(Spacer(1, 1*cm))

    # 4. Data Siswa (Menggunakan Tabel agar rapi)
    data_siswa = [
        ["Nama Peserta Didik", ": " + data.get('nama', '-')],
        ["Kelas", ": " + data.get('kelas', '-')],
        ["Periode / Semester", ": " + data.get('periode', '-')],
        ["Tanggal Laporan", ": " + datetime.now().strftime("%d %B %Y")]
    ]
    
    t_siswa = Table(data_siswa, colWidths=[4*cm, 10*cm])
    t_siswa.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_siswa)
    elements.append(Spacer(1, 1*cm))

    # 5. Isi Laporan
    elements.append(Paragraph("<b>KESIMPULAN PERKEMBANGAN:</b>", style_normal))
    elements.append(Spacer(1, 0.2*cm))
    
    hasil_data = data.get('hasil', '-')
    
    # Handle backward compatibility jika string biasa
    if isinstance(hasil_data, str):
        hasil_text = hasil_data
        p_hasil = Paragraph(hasil_text, style_normal)
        t_hasil = Table([[p_hasil]], colWidths=[16*cm])
        t_hasil.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
            ('PADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(t_hasil)
        elements.append(Spacer(1, 1*cm))
    else:
        # Jika berupa dict JSON baru
        kesimpulan = hasil_data.get('kesimpulan', '-')
        details = hasil_data.get('detail', [])
        
        # Kesimpulan Box
        p_hasil = Paragraph(kesimpulan, style_bold)
        t_hasil = Table([[p_hasil]], colWidths=[16*cm])
        t_hasil.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
            ('PADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(t_hasil)
        elements.append(Spacer(1, 0.8*cm))
        
        # Detail Tabel
        if details:
            elements.append(Paragraph("<b>RINCIAN PENILAIAN INDIKATOR:</b>", style_normal))
            elements.append(Spacer(1, 0.2*cm))
            
            # Header
            t_data = [["No", "Indikator", "Nilai", "Catatan Guru"]]
            
            teks_nilai = {1: "BB", 2: "MB", 3: "BSH", 4: "BSB"}
            
            # Rows
            for i, d in enumerate(details):
                nilai_huruf = teks_nilai.get(d.get('nilai'), str(d.get('nilai')))
                # Wrap text menggunakan Paragraph agar panjangnya aman
                p_ind = Paragraph(d.get('indikator', '-'), style_normal)
                p_cat = Paragraph(d.get('catatan', '-'), style_normal)
                
                t_data.append([str(i+1), p_ind, nilai_huruf, p_cat])
            
            t_detail = Table(t_data, colWidths=[1*cm, 5*cm, 2*cm, 8*cm])
            t_detail.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey), # Header background
                ('ALIGN', (0,0), (-1,0), 'CENTER'), # Header alignment
                ('ALIGN', (0,1), (0,-1), 'CENTER'), # No alignment
                ('ALIGN', (2,1), (2,-1), 'CENTER'), # Nilai alignment
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(t_detail)
            elements.append(Spacer(1, 1*cm))

    # 6. Tanda Tangan
    # Tabel 2 kolom untuk tanda tangan (kiri: kosong/ortu, kanan: guru)
    nama_guru = data.get('guru', 'Guru Kelas')
    
    data_ttd = [
        ["Mengetahui,", "Baleendah, " + datetime.now().strftime("%d %B %Y")],
        ["Orang Tua / Wali,", "Guru Wali Kelas,"],
        ["", ""],
        ["", ""],
        ["", ""], # Space untuk tanda tangan
        ["( ........................... )", f"( {nama_guru} )"]
    ]
    
    t_ttd = Table(data_ttd, colWidths=[8*cm, 8*cm])
    t_ttd.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ]))
    elements.append(t_ttd)

    # 7. Build PDF
    doc.build(elements)
    return True