class Word:
    def __init__(self):
        # 没有处理过的字符串
        self.raw_text = ''
        # 查询的是什么
        self.text = ''
        # 存储基本示意，包括形容词，动词等词性
        # 存储形式： props['n.'] = ''
        self.props = {}
        # 变形
        self.changes = {}

