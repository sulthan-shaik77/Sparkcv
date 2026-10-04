import zipfile
import io
import json
import base64
import urllib.request

# 1. Test DOCX
buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w') as z:
    z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:t>John Doe Senior Python Developer with FastAPI and Docker experience.</w:t></w:p></w:body></w:document>')

b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
req = urllib.request.Request(
    'http://127.0.0.1:8501/api/upload',
    data=json.dumps({'filename': 'resume.docx', 'filedata': b64}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
print('DOCX Upload Test:', res)
assert "FastAPI" in res["text"], "Failed to extract text from DOCX"

# 2. Test TXT
txt_b64 = base64.b64encode(b"Alex Chen Python and SQL Engineer").decode('utf-8')
req_txt = urllib.request.Request(
    'http://127.0.0.1:8501/api/upload',
    data=json.dumps({'filename': 'resume.txt', 'filedata': txt_b64}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res_txt = json.loads(urllib.request.urlopen(req_txt).read().decode('utf-8'))
print('TXT Upload Test:', res_txt)
assert "Alex Chen" in res_txt["text"], "Failed to extract text from TXT"

print(">>> ALL UPLOAD TESTS PASSED SUCCESSFULLY! <<<")
