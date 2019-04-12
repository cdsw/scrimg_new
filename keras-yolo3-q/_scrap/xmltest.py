import xml.etree.ElementTree as ET
filename = 'X00000_Latin108.xml'
tree = ET.parse(filename)
root = tree.getroot()
annotations = "./Labeling/input/" + filename
for boxes in root.iter('object'):
    meta = boxes.getchildren()
    cls_id = str(["latin", "thai", "inuktitut"].index(meta[0].text))
    box = meta[4]
    xmin, ymin, xmax, ymax = box[0].text, box[1].text, box[2].text, box[3].text
    annotations += ' ' + xmin + ',' +  ymin + ',' +  xmax + ',' +  ymax + ',' + cls_id
print(annotations)
    
