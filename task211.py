import sys

class State:
    def __init__(self):
        self.long_len = 0
        self.link = -1
        self.next = {}
        
        self.first_pos_of_end = 1

class SuffAutomation:
    def __init__(self):
        self.states = []
        self.last_st = 0
        self.states.append(State())
        self.max_size = 1
        
    def add_char(self, c):
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

        for c in text:
            self.add_char(c)
        
    def search_str_in_text(self, string):
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
	print("Please, entry search querie")
	string = input()
	entrance = suff_auto.search_str_in_text(string)
	if (entrance != -1):
		print("Entrance in : ", entrance, " position.")
	else:
		print("No entrance.")
	









