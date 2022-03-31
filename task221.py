import sys

"""
Рассмотрим любую непустую подстроку t строки s. Тогда назовём множеством окончаний endpos(t) множество всех позиций в строке s,
в которых оканчиваются вхождения строки t. Мы будем называть две подстроки t_1 и t_2 endpos-эквивалентными, если их множества
окончаний совпадают: endpos(t_1) = endpos(t_2).
"""

class State:
    """
    Класс состояния ячейки автомата.
    Xранит всю информацию о конкретном переходе.

    ...

    Attributes
    ----------
    long_len : int
        длина наибольшей строки соответствующей State.
    link : int
        Суффиксная ссылка link ведёт в такое состояние, которому соответствует наидлиннейший суффикс строки,
        находящийся в другом классе endpos-эквивалентности.
    next : dict
        Список переходов из этого состояния.
    first_pos_of_end : int
        Позиция окончания первого вхождения.


    Methods
    -------
    __init__(self):
        Инициализация нулевого состояния.
    """

    def __init__(self):
        self.long_len = 0
        self.link = -1
        self.next = {}
        self.first_pos_of_end = 1

class SuffAutomation:
    """
    Класс суффиксного автомата.

    ...

    Attributes
    ----------
    states :  list
        Массив состояний суффиксного автомата.
    last_st : int
        Номер последнего состояния с самым длинным вхождением.
    max_size : int
        длина максимального вхождения.

    Methods
    -------
    add_char(c):
        Добовляем новый символ в текущий суффиксный автомат.

    build_suff_tree(text, create_new = True):
        Построение суфиксного дерева на основе текста text.
        Если create_new == True то строим автомат начиная с нулевого состояния.

    search_str_in_text(string):
        Поиск строки в тексте.
    """

    def __init__(self):
        """
        Инициализация единственного нулевого состояния.

        Parameters
        ----------
            states :  list
                Массив состояний суффиксного автомата.
            last_st : int
                Номер последнего состояния с самым длинным вхождением.
            max_size : int
                длина максимального вхождения.

        """
        self.states = []
        self.last_st = 0
        self.states.append(State())
        self.max_size = 1

    def add_char(self, c):
        """
        Добавления одного символа c в конец текущей строки.
        Алгоритм онлайновый, т.е. будет добавляем по одному символу строки s, перестраивая соответствующим образом текущий автомат.


        Parameters
        ----------
        c : char


        Returns
        -------
        None
        """

        curr_state = self.max_size
        self.max_size += 1
        self.states.append(State())
        self.states[curr_state].long_len = self.states[self.last_st].long_len + 1
        self.states[curr_state].first_pos_of_end = self.states[curr_state].long_len - 1
        iterator = self.last_st

        while (iterator != -1 and c not in self.states[iterator].next):
            self.states[iterator].next[c] = curr_state
            iterator = self.states[iterator].link
        if iterator == -1:
            self.states[curr_state].link = 0
        else:
            st_without_c = self.states[iterator].next[c]
            if self.states[iterator].long_len + 1 == self.states[st_without_c].long_len:
                self.states[curr_state].link = st_without_c
            else:
                clone_state = self.max_size
                self.max_size += 1
                self.states.append(State())
                self.states[clone_state].long_len = self.states[iterator].long_len + 1
                self.states[clone_state].next = self.states[st_without_c].next
                self.states[clone_state].link = self.states[st_without_c].link
                self.states[clone_state].first_pos_of_end = self.states[st_without_c].first_pos_of_end
                while (iterator != -1 and self.states[iterator].next[c] == st_without_c):
                    self.states[iterator].next[c] = clone_state
                    iterator = self.states[iterator].link
                self.states[st_without_c].link = clone_state
                self.states[curr_state].link = clone_state
        self.last_st = curr_state

    def build_suff_tree(self, text, create_new = True):
        """
        Построение суфиксного дерева на основе текста text.


        Parameters
        ----------
        create_new : bool, optional
            Если create_new == True то строим автомат начиная с нулевого состояния.

        text: str
        Текст на основе которого строится автомат.

        Returns
        -------
        None
        """

        if create_new:
            self.states = []
            self.last_st = 0
            self.states.append(State())
            self.max_size = 1

        for c in text:
            self.add_char(c)

    def search_str_in_text(self, string):
        """
        Поиск строки в тексте.

        Parameters
        ----------
        additional : str, optional
            More info to be displayed (default is None)

        Returns
        -------
        Возвращает -1 если вхождение не найдено, иначе индекс первого вхождения.
        """

        curr_state = self.states[0]
        first_pos = -1
        for c in string:
            if c in curr_state.next:
                curr_state = self.states[curr_state.next[c]]
                first_pos = curr_state.first_pos_of_end
            else:
                return -1
        return first_pos - len(string) + 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        large_text = open(sys.argv[1], "r")
    else:
        raise Exception("Please, enter the name of file with text as 1st arg!")


suff_auto = SuffAutomation()

for line in large_text:
    suff_auto.build_suff_tree(line, create_new = False)

large_text.close()


print("Please, entry number of search queries.")
n = int(input())
for i in range(n):
    print("Please, entry search querie.")
    string = input()
    entrance = suff_auto.search_str_in_text(string)
    if (entrance != -1):
        print("Entrance in ", entrance, " position.")
    else:
        print("No entrance.")