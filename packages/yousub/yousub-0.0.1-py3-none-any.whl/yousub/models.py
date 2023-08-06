import json
import os
import urllib.request
import xml.etree.ElementTree as ET
import logging


from .tools import seconds_to_srt_time, unescape

logger = logging.getLogger('yousub')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class YouSub:
    LANG_URL = 'https://video.google.com/timedtext?type=list&v=%s'
    SUBTITLE_URL = "https://video.google.com/timedtext?hl=%s&lang=%s&name=&v=%s"

    @classmethod
    def get_lang_codes_list(cls, vid):
        url = cls.LANG_URL % vid
        root = cls.parse_xml_from_url(url)
        codes = []
        for child in root:
            codes.append(child.attrib['lang_code'])
        if codes:
            logger.info("Found subtitle languages: %s" % ", ".join(codes))
        else:
            raise NoSubtitleException("No subtitle available for this video")
        return codes

    @classmethod
    def get_subtitle_by_lang_code(cls, lang_code, vid, directory, filetype):
        url = cls.SUBTITLE_URL % (lang_code, lang_code, vid)
        filename = ""
        if filetype == 'srt':
            root = cls.parse_xml_from_url(url)
            str_data = cls.xml_to_srt(root)
            filename = lang_code + '_' + vid + '.srt'
            cls.write_file(directory, filename, unescape(str_data))
        if filetype == 'xml':
            root = cls.parse_xml_from_url(url)
            filename = lang_code + '_' + vid + '.xml'
            str_data = ET.tostring(root, encoding="unicode", method="xml")
            cls.write_file(directory, filename, str_data)
        if filetype == 'json':
            root = cls.parse_xml_from_url(url)
            filename = lang_code + '_' + vid + '.json'
            str_data = cls.xml_to_json(root)
            cls.write_file(directory, filename, str_data)
        logger.info("Successfully download file %s" % filename)
    @staticmethod
    def parse_xml_from_url(url):
        logger.debug("Retrieve from url: %s" % url)
        with urllib.request.urlopen(url, timeout=7) as response:
            xml = response.read()
            root = ET.fromstring(xml)
        return root

    @staticmethod
    def xml_to_json(root):
        subtitle_data = []
        line = 1
        for child in root:
            subtitle_data.append({
                "line": line,
                "text": unescape(child.text or ""),
                "start": child.attrib['start'],
                "dur": child.attrib['dur']
            })
            line += 1
        return json.dumps(subtitle_data, ensure_ascii=False, indent=4)

    @staticmethod
    def xml_to_srt(root):
        subtitle_data = []
        line = 1
        for child in root:
            subtitle_data.append({
                "line": line,
                "text": child.text,
                "start": child.attrib['start'],
                "dur": child.attrib['dur']
            })
            line += 1

        srt_line = []
        for item in subtitle_data:
            srt_line.append("{}\n{} --> {}\n{}\n\n".format(item['line'],
                                                           seconds_to_srt_time(item['start']),
                                                           seconds_to_srt_time(
                                                               "%.3f" % (float(item['start']) + float(item['dur']))),
                                                           item['text']))
        return "".join(srt_line)

    @staticmethod
    def save_xml(url, directory, lang_code):
        pass

    @staticmethod
    def write_file(directory, filename, str_data):
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
            f.write(str_data)

    @classmethod
    def run(cls, url, dir, show, lang, filetype):
        codes = []
        codes = YouSub.get_lang_codes_list(url)
        if show:
            return
        if lang:
            if lang in codes:
                YouSub.get_subtitle_by_lang_code(lang, url, dir, filetype)
            else:
                raise NoSubtitleException("No subtitle of language %s found" % lang)
        else:
            for l in codes:
                YouSub.get_subtitle_by_lang_code(l, url, dir, filetype)


class NoSubtitleException(Exception):
    def __init__(self, msg):
        self.msg = msg
