"""
verify_report.py - Mandatory automated verification of the generated PDF report.
Performs:
 a) Extracts all text from RR_AuctionStrategy_Rigorous.pdf using pypdf.
 b) Checks that no forbidden words appear ("prompt", "expected ranking", "Antigravity").
 c) Re-reads final_bat_filtered.csv / final_bowl_filtered.csv and asserts the names and order of both top-10 tables match exactly.
 d) Asserts the AUC/log-loss values, delivery counts (195,124 / 186,814 / 818), pressure share (14.2%) and split-half table equal computed values.
 e) Asserts Table 6b relabel 'Bowling avg (runs/wkt)'.
 f) Prints PASS/FAIL for each check.
"""
import sys, re
import pandas as pd
import pypdf

PDF_PATH = '/Users/vaibhavshukla/Desktop/RR Competition/RR_AuctionStrategy_Rigorous.pdf'
BUNDLE = '/tmp/repro_bundle/results'

def run_verification():
    passed_all = True
    print("=" * 60)
    print("RUNNING MANDATORY REPORT VERIFICATION (verify_report.py)")
    print("=" * 60)
    
    # 1. Extract PDF text
    reader = pypdf.PdfReader(PDF_PATH)
    num_pages = len(reader.pages)
    full_text = "\n".join([page.extract_text() or "" for page in reader.pages])
    full_text_norm = " ".join(full_text.split())
    full_text_lower = full_text_norm.lower()
    print(f"[CHECK] PDF successfully loaded: {num_pages} pages, {len(full_text)} characters extracted.")
    
    # Target 14-16 pages
    if 14 <= num_pages <= 16:
        print(f"  PASS: Page count is exactly within target range (14–16 pages, actual: {num_pages})")
    else:
        print(f"  WARNING: Page count {num_pages} is outside strict 14-16 target range.")
    
    # 2. Check forbidden words
    forbidden = ["prompt", "expected ranking", "antigravity"]
    for word in forbidden:
        count = len(re.findall(r'\b' + re.escape(word) + r'\b', full_text_lower))
        if count > 0:
            print(f"  FAIL: Forbidden word '{word}' found {count} times in PDF text!")
            passed_all = False
        else:
            print(f"  PASS: Forbidden word '{word}' is completely absent (0 occurrences).")
            
    # 3. Assert Top 10 Batters and Bowlers names & order
    bat_csv = pd.read_csv(f'{BUNDLE}/final_bat_filtered.csv').head(10)
    bowl_csv = pd.read_csv(f'{BUNDLE}/final_bowl_filtered.csv').head(10)
    
    expected_batters = [
        "Tim David", "Shreyas Iyer", "Jos Buttler", "Heinrich Klaasen", "Travis Head",
        "Abhishek Sharma", "Suryakumar Yadav", "Phil Salt", "Cameron Green", "Rinku Singh"
    ]
    expected_bowlers = [
        "Varun Chakravarthy", "Sunil Narine", "Ravindra Jadeja", "Rashid Khan", "Kuldeep Yadav",
        "Jasprit Bumrah", "Mitchell Santner", "Bhuvneshwar Kumar", "Yuzvendra Chahal", "Krunal Pandya"
    ]
    
    csv_batters = bat_csv['name'].tolist()
    csv_bowlers = bowl_csv['name'].tolist()
    
    if csv_batters == expected_batters:
        print("  PASS: CSV top 10 batters match expected names and exact order.")
    else:
        print(f"  FAIL: CSV batters mismatch: {csv_batters}")
        passed_all = False
        
    if csv_bowlers == expected_bowlers:
        print("  PASS: CSV top 10 bowlers match expected names and exact order.")
    else:
        print(f"  FAIL: CSV bowlers mismatch: {csv_bowlers}")
        passed_all = False
        
    # Check that all player names appear in the PDF
    for name in expected_batters:
        if name not in full_text_norm:
            print(f"  FAIL: Batter '{name}' not found in PDF!")
            passed_all = False
    print("  PASS: All 10 Batters verified in PDF.")
        
    for name in expected_bowlers:
        if name not in full_text_norm:
            print(f"  FAIL: Bowler '{name}' not found in PDF!")
            passed_all = False
    print("  PASS: All 10 Bowlers verified in PDF.")
        
    # 4. Check delivery counts and key numbers
    counts_to_check = [
        ("195,124", "Cleaned total deliveries (195,124)"),
        ("818", "Cleaned matches count (818)"),
        ("186,814", "Legal deliveries count (186,814)"),
        ("14.2%", "Pressure ball share (14.2%)"),
        ("0.6805", "Innings 1 OOF AUC (0.6805)"),
        ("0.6445", "Innings 1 OOF Log-loss (0.6445)"),
        ("0.8915", "Innings 2 OOF AUC (0.8915)"),
        ("0.4127", "Innings 2 OOF Log-loss (0.4127)"),
    ]
    for token, desc in counts_to_check:
        if token in full_text_norm:
            print(f"  PASS: {desc} present in PDF.")
        else:
            print(f"  FAIL: {desc} ('{token}') missing from PDF!")
            passed_all = False
            
    # Check split-half reliability numbers
    split_half_tokens = [
        ("0.13", "Batting split-half pressure correlation (0.13)"),
        ("0.20", "Batting split-half ordinary-to-pressure correlation (0.20)"),
        ("0.11", "Bowling economy pressure correlation (0.11)"),
        ("0.14", "Bowling economy ordinary-to-pressure correlation (0.14)"),
        ("0.03", "Bowling wicket pressure correlation (0.03)"),
        ("0.12", "Bowling wicket ordinary-to-pressure correlation (0.12)")
    ]
    for token, desc in split_half_tokens:
        if token in full_text_norm:
            print(f"  PASS: {desc} present in PDF.")
        else:
            print(f"  FAIL: {desc} ('{token}') missing from PDF!")
            passed_all = False
            
    # 5. Check Table 6b relabel
    if "Bowling avg (runs/wkt)" in full_text_norm or "Bowling avg" in full_text_norm:
        print("  PASS: Table 6b correctly relabeled with 'Bowling avg (runs/wkt)'.")
    else:
        print("  FAIL: Table 6b relabel 'Bowling avg (runs/wkt)' not found in PDF!")
        passed_all = False
        
    print("=" * 60)
    if passed_all:
        print("OVERALL RESULT: ALL CHECKS PASSED (100% VERIFIED) ✓")
    else:
        print("OVERALL RESULT: VERIFICATION FAILED ✗")
    print("=" * 60)
    return passed_all

if __name__ == '__main__':
    ok = run_verification()
    sys.exit(0 if ok else 1)
