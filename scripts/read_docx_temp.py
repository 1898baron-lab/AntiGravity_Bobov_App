import sys, zipfile, xml.etree.ElementTree as ET
try:
    with zipfile.ZipFile(sys.argv[1]) as d:
        t = [ "".join(n.text for n in p.findall('.//w:t', {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) if n.text) for p in ET.fromstring(d.read('word/document.xml')).findall('.//w:p', {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) ]
        print(chr(10).join(t))
except Exception as e:
    print(e)
