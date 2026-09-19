from nexus.secrets import scan
from pathlib import Path
def test_secret_scan(tmp_path):
    p=tmp_path/"x.txt"; p.write_text("api_key=ABCDEF1234567890")
    cfg={"ignore_paths":[],"max_file_size":100000}
    result=scan(tmp_path,cfg)
    assert result and result[0]["severity"]=="HIGH"
