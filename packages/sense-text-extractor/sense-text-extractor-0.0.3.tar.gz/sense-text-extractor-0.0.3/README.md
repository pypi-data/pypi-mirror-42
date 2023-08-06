# sense-text-extractor

sense-text-extractor是正文抽取客户端库


## 安装方式(当前版本0.0.1)

    pip install sense-text-extractor
    
## 使用指南

基于sense-core的settings.ini的label配置调用：
    
    from sense_text_extractor import SenseTextExtractor
    extractor = SenseTextExtractor(label='text_extractor')
    text = extractor.extract_text("http://sports.sina.com.cn/g/pl/2019-01-11/doc-ihqhqcis5048507.shtml", "穆里尼奥在等待复出")
    print(text)
   
使用host和port的调用：

    extractor = SenseTextExtractor('52.83.143.61', '6681')
    text = extractor.extract_text("http://sports.sina.com.cn/g/pl/2019-01-11/doc-ihqhqcis5048507.shtml", "穆里尼奥在等待复出")
    print(text)


## 使用说明

extract_text方法可能抛出异常，需要自己捕捉。返回结果是string，如果是''字符串，表示可能没有抽取出正文。
如果用于爬虫，extract_text需要传入第三个参数，也就是下载的html源码，否则extractor的sever端因为获取超时而抛出异常，也容易被反爬虫限制。

