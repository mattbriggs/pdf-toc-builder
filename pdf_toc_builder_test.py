'''Tests for pdf-toc-builder.py'''

import pdf_toc_builder as PTB
import config as CF

def test_get_titles_from_repo_paths():
    headings_from_file = PTB.get_titles_from_repo_paths(CF.SUBFOLDERS)
    simple = set(headings_from_file)
    found = False
    if "Install the AKS engine on Linux in Azure Stack Hub" in simple:
        found = True
    assert True == found

