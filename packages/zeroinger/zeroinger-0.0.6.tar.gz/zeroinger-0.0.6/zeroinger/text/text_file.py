class TextFile:
    def __init__(self):
        pass

    @staticmethod
    def load_lines(file_path, encoding='utf-8'):
        """
        :param file_path: file path
        :param encoding: default utf-8 
        :return: list of line 
        """
        data = []
        inf = open(file_path, 'r', encoding=encoding)
        for line in inf:
            # delete \n in the end
            data.append(line.replace('\n', ''))
        inf.close()
        return data
        pass

    @staticmethod
    def dump_lines(file_path, list_of_line, encoding='utf-8'):
        """
        :param file_path: 
        :param list_of_line: 
        :param encoding: 
        :return: 
        """
        outf = open(file_path, 'w', encoding=encoding)
        for line in list_of_line:
            outf.write(line + '\n')
        outf.close()
        pass
