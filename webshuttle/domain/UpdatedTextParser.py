class UpdatedTextParser:
    def __init__(self, elements, filtering_keyword: str, text_list):
        self.elements = elements
        self.filtering_keyword = filtering_keyword
        self.text_list = text_list
        self.collected_text = ""

    def parse(self):
        if len(self.text_list) == 0:
            self._collect_updated_text_first()
        else:
            self._collect_updated_text()
        return self.collected_text

    def _collect_updated_text_first(self):
        for e in self.elements:
            text: str = e.text
            if len(text) > 0:
                if not self._has_filtering_keyword(text):
                    continue
                self.text_list.append(text)
                self._collect_text(text)

    def _collect_updated_text(self):
        new_text_list = self._new_text_list()
        for new_text in new_text_list:
            if new_text not in self.text_list:
                if len(new_text) > 0:
                    self._collect_text(new_text)

    def _collect_text(self, text):
        # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
        self.collected_text += text.replace("\n", " | ") + "\n"

    def _new_text_list(self):
        result = []
        for e in self.elements:
            text: str = e.text
            if not self._has_filtering_keyword(text):
                continue
            result.append(text)
        return result

    def _has_filtering_keyword(self, text):
        return text.find(self.filtering_keyword) > -1
