import yaml
import xml.etree.ElementTree as xml_tree
import os

# Our goal with this app is to make an itunes rss compatible entries based from the ata that we have from a yaml file

with open('feed.yaml', 'r') as file:
    # load yaml file
    yaml_data = yaml.safe_load(file)

# base url of my webpage which was stored in the yaml file
link_prefix = os.getenv("BASE_URL", "http://localhost")

# make a variable that represents the rss file i'm building
# rss is initialized with the version and dtd used with itunes
rss_element = xml_tree.Element('rss', {
    'version': '2.0', 
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content':'http://purl.org/rss/1.0/modules/content/'
})

# add the subelement 'channel' to the rss_element xml tree
channel_element = xml_tree.SubElement(rss_element, 'channel')

# set the text value of the subelement 'channel' with the data from the yaml file
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'link').text = link_prefix
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix+yaml_data['image']})
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category'] })

# build channel items
for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']
    xml_tree.SubElement(item_element, 'enclosure', {
        'length': item['duration'],
        'type': 'audio/mpeg',
        'url': link_prefix + item['file']    
    })
    
# get the whole rss_element xml tree and assign it to output_tree variable
output_tree = xml_tree.ElementTree(rss_element)
# output this xml_tree to output.xml file, setting the encoding and xml_declaration
output_tree.write('output.xml', encoding='UTF-8', xml_declaration=True)