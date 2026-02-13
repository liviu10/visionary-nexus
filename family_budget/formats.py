import re
import tablib
import pdfplumber
from import_export.formats.base_formats import Format
from .models import Account

class INGPDF(Format):
    def __init__(self, *args, **kwargs):
        pass

    def get_title(self):
        return "ING PDF"

    def can_import(self):
        return True

    def can_export(self):
        return False

    def create_dataset(self, in_stream, **kwargs):
        import logging
        import io
        import re
        import pdfplumber
        import tablib
        from .models import Account

        logger = logging.getLogger(__name__)
        dataset = tablib.Dataset()
        dataset.headers = ['date', 'details', 'debit', 'credit', 'bank_account_id']
        
        print("\n--- PARSING WITH NOISE FILTERING ---")

        RO_MONTHS = {
            'ianuarie': '01', 'februarie': '02', 'martie': '03', 'aprilie': '04',
            'mai': '05', 'iunie': '06', 'iulie': '07', 'august': '08',
            'septembrie': '09', 'octombrie': '10', 'noiembrie': '11', 'decembrie': '12'
        }

        # Cuvinte care marchează finalul util al unei pagini sau zgomot administrativ
        STOP_WORDS = [
            "roxana petria", "alexandra ilie", "sef serviciu", "ing bank", "sucursala",
            "informatii despre schema", "garantare a depozitelor", "www.ing.ro", "titular cont",
            "numar cont", "moneda:", "data detalii tranzactie", "valabil fara semnatura",
            "pagina", "extras de cont", "pentru perioada"
        ]

        def parse_ro_date(text):
            for ro, mm in RO_MONTHS.items():
                if ro in text.lower():
                    # Căutăm data la începutul rândului (ING pune data prima)
                    match = re.match(r'^\s*(\d{1,2})\s+' + ro + r'\s+(\d{4})', text.lower())
                    if match:
                        return f"{match.group(2)}-{mm}-{match.group(1).zfill(2)}"
            return None

        def clean_amount(text):
            # Căutăm sume de tipul 1.234,56 sau 267,00 la final de rând
            match = re.search(r'(\d+[\d.,]*,\d{2})\s*$', text)
            if match:
                val = match.group(1).replace('.', '').replace(',', '.')
                return val
            return "0"

        try:
            if isinstance(in_stream, (bytes, str)):
                if isinstance(in_stream, str): in_stream = in_stream.encode('utf-8')
                in_stream = io.BytesIO(in_stream)

            with pdfplumber.open(in_stream) as pdf:
                # IBAN Discovery
                full_content = "".join([p.extract_text() or "" for p in pdf.pages])
                iban_match = re.search(r'RO\d{2}[A-Z]{4}[A-Z0-9]{16}', full_content.replace(" ", ""))
                account_id = None
                if iban_match:
                    iban_clean = iban_match.group(0).upper()
                    try:
                        account_id = Account.objects.get(iban_account__iexact=iban_clean).id
                    except: pass

                current_tx = None

                for page in pdf.pages:
                    lines = page.extract_text().split('\n')
                    
                    for line in lines:
                        line_clean = line.strip()
                        if not line_clean: continue
                        
                        # Verificăm dacă rândul conține zgomot administrativ
                        if any(stop.lower() in line_clean.lower() for stop in STOP_WORDS):
                            continue

                        found_date = parse_ro_date(line_clean)
                        
                        if found_date:
                            # Salvăm tranzacția anterioară
                            if current_tx:
                                dataset.append([current_tx['date'], current_tx['details'].strip(), current_tx['debit'], current_tx['credit'], account_id])
                            
                            amount = clean_amount(line_clean)
                            
                            # Curățăm detaliile de pe primul rând (eliminăm data și suma)
                            # Re-creăm textul detaliilor fără data de la început
                            detail_start = re.sub(r'^\d{1,2}\s+\w+\s+\d{4}', '', line_clean, flags=re.I).strip()
                            # Eliminăm suma de la final
                            detail_start = re.sub(r'\d+[\d.,]*,\d{2}\s*$', '', detail_start).strip()

                            current_tx = {
                                'date': found_date,
                                'details': detail_start,
                                'debit': "0",
                                'credit': "0"
                            }
                            
                            # Logică Debit/Credit: ING pune Credit (încăsări) la final de tot
                            # Dacă în linie avem "Incasare" sau suma e pozitivă fără semn de plată
                            if "incasare" in line_clean.lower():
                                current_tx['credit'] = amount
                            else:
                                current_tx['debit'] = amount
                        elif current_tx:
                            # Dacă rândul nu are dată, dar avem o tranzacție activă, este un rând de detalii
                            line_amount = clean_amount(line_clean)
                            
                            # Dacă găsim o sumă pe rândul de detalii (și nu aveam una deja)
                            if line_amount != "0" and current_tx['credit'] == "0" and current_tx['debit'] == "0":
                                if "incasare" in current_tx['details'].lower():
                                    current_tx['credit'] = line_amount
                                else:
                                    current_tx['debit'] = line_amount
                            
                            # Adăugăm la detalii doar dacă nu e sumă pură
                            clean_detail_line = re.sub(r'\d+[\d.,]*,\d{2}\s*$', '', line_clean).strip()
                            if clean_detail_line:
                                current_tx['details'] += " " + clean_detail_line
                
                # Ultima tranzacție din tot documentul
                if current_tx:
                    dataset.append([current_tx['date'], current_tx['details'].strip(), current_tx['debit'], current_tx['credit'], account_id])

        except Exception as e:
            print(f"DEBUG EROARE: {e}")

        print(f"--- FINAL: Dataset are {len(dataset)} randuri ---")
        return dataset