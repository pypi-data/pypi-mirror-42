from sense_text_extractor import SenseTextExtractor
import sense_core as sd

sd.log_init_config('text_extractor', sd.config('log_path'))


def test_text_extract():
    sd.log_info("xxxxxxx")
    extractor = SenseTextExtractor(label='text_extractor')
    text = extractor.extract_text("http://www.baiyintouzi.com/stock/20181216-33842.html", "穆里尼奥在等待复出")
    print(text)


def test_text_extract2():
    extractor = SenseTextExtractor('127.0.0.1', '6681')
    pattern = {
        'title': 'div[@class="post_content_main"]/h1',
        'time': 'div[@class="post_time_source"]',
        'text': 'div[@class="post_text"]',
    }
    text = extractor.extract_text("http://money.163.com/19/0225/07/E8RJ4IP2002581PP.html", "穆里尼奥在等待复出",
                                  pattern=pattern, retry_all=True)
    print(text)
