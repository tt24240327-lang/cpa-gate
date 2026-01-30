
import sys
import os
import random
import hashlib

sys.path.append('h:\\checkpoint-system\\api')
try:
    from index import app, GeneEngine, block_home_overview, render_page, block_header, block_footer, block_archive_main
    print("Successfully imported index.py")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

def test_diversity():
    with app.test_request_context('/?k=test'):
        print("Testing 24 Skeletons Generation...")
        for i in range(1, 25):
            ge = GeneEngine(f"test_seed_{i}")
            ge.skeleton_id = i # Force ID
            
            # Update flags based on forced ID
            ge.has_sidebar = (ge.skeleton_id in [1, 9, 10, 15, 20])
            ge.has_widgets = (ge.skeleton_id in [2, 10, 16, 21])
            ge.is_minimal = (ge.skeleton_id in [3, 6, 8, 11, 14, 19])
            ge.is_feed = (ge.skeleton_id in [5, 13, 17, 22])
            ge.is_dashboard = (ge.skeleton_id in [7, 18, 23, 24])
            
            try:
                home_html = block_home_overview(ge)
                header_html = block_header(ge)
                page = render_page(ge, [home_html])
                print(f"[OK] Skeleton {i}: Generated Page Length {len(page)}")
                
                # Check for specific features
                if ge.is_feed:
                    if "리얼타임 기술 피드" not in home_html: print(f"[WARN] Skeleton {i} (Feed) missing feed keywords")
                if ge.is_dashboard:
                    if "실시간 관제 현황" not in home_html: print(f"[WARN] Skeleton {i} (Dashboard) missing dashboard keywords")
                    
            except Exception as e:
                print(f"[FAIL] Skeleton {i}: {e}")
                # import traceback
                # traceback.print_exc()

    print("\nTesting 10 Archive Styles...")
    with app.test_request_context('/?k=test'):
        for i in range(1, 11):
            ge = GeneEngine(f"archive_test_{i}")
            ge.archive_style = i
            try:
                archive_html = block_archive_main(ge)
                print(f"[OK] Archive Style {i}: Generated Block Length {len(archive_html)}")
            except Exception as e:
                print(f"[FAIL] Archive Style {i}: {e}")

    print("\nTesting Detail Pages (Lego Text Engine)...")
    with app.test_request_context('/?k=test'):
        for i in range(1, 6):
            doc_id = f"TEST-DOC-{i}"
            ge = GeneEngine(f"test_detail_{i}")
            try:
                # Test block_detail_view
                from index import block_detail_view
                detail_html = block_detail_view(ge, doc_id)
                print(f"[OK] Detail Page {i}: Generated Length {len(detail_html)}")
                
                # Check for Lego Text features
                if "Technical Abstract" not in detail_html:
                    print(f"[WARN] Detail Page {i}: Missing Technical Abstract section")
                if "책임연구원" not in detail_html:
                    print(f"[WARN] Detail Page {i}: Missing Official Seal")
                    
            except Exception as e:
                print(f"[FAIL] Detail Page {i}: {e}")

if __name__ == "__main__":
    test_diversity()
