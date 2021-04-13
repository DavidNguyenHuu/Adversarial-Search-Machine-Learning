import copy


def all_token1(s):  # will return a list for all the tokens in the game
    list1 = []
    for i in range(s + 1):
        if i != 0:
            list1.append(i)
    return list1


def remaining_token1(l1, l2):  # will return what tokens that are still available 
    l3 = list(set(l1) ^ set(l2))
    return l3


def available_token1(size):  # will return the available tokens to remove at the first round
    list1 = []
    for i in range(size + 1):
        if i % 2 != 0:
            list1.append(i)
    return list1


def available_token2(number, list1):  # will return the available tokens to remove after the first round
    list2 = []
    for i in list1:
        if i % number == 0 or number % i == 0:
            list2.append(i)
    return list2


class game:   

    def __init__(self, Token_number, Token_taken, List_taken_token, depth, parent):
        self.Token_number = Token_number
        self.All_Tokens = all_token1(self.Token_number)
        self.Token_taken = Token_taken
        self.list_token_taken = []
        for i in List_taken_token:
            self.list_token_taken.append(i)
        self.remaining_token = remaining_token1(self.All_Tokens, self.list_token_taken)
        self.List_taken_token = List_taken_token
        self.depth = depth
        self.parent = parent
        if Token_taken % 2 == 0:
            self.player = "Max"
        else:
            self.player = "Min"

def tokens_to_remove(game1):  # will return a list of tokens that can be removed
    initial_list = []
    second_list = []
    if game1.Token_taken == 0:
        size = int(game1.Token_number / 2)
        initial_list = available_token1(size)
        return initial_list
    else:
        factor = game1.List_taken_token[-1]
        second_list = available_token2(factor, game1.remaining_token)
        if not second_list:
            return []
        else:
            return second_list


def remove_token(list1, item1, game1):  # will return a new state after removing a a token
    item = item1
    test_game = copy.deepcopy(game1)
    father_list = test_game.remaining_token
    list2 = []
    list3 = []
    for i in father_list:
        if i == item:
            father_list.remove(i)
            break
    list2 = father_list
    list3 = test_game.list_token_taken
    list3.append(item)
    game_child = game(game1.Token_number, game1.Token_taken + 1, list3, game1.depth + 1, game1)
    return game_child


def remove_all_available_tokens(list1, game1):  # will return a list of all the possible moves  
    child_list = []
    for i in list1:
        child_list.append(remove_token(list1, i, game1))
    return child_list




def static_board_eval(game1):  # will return a value based on the board evaluation
    list1 = tokens_to_remove(game1)  # will save the list of tokens that can be removed in the current state
    x = 0
    if game1.Token_taken > 0:
        y = game1.List_taken_token[-1]  # will save the last taken token
    multiplies = 0  # number of multiplies of the last taken token in case it was prime
    one_is_taken = False  # False if 1 is not taken and True if 1 is taken
    if list1 == [] and game1.player == "Max":  # will return -1 if it's max turn and there are no tokens to take
        x = -1
        return x
    if list1 == [] and game1.player == "Min":  # will return 1 if it's min turn and there are no tokens to take
        x = 1
        return x
    for x in game1.List_taken_token:  # will check if 1 is taken
        if x == 1:
            one_is_taken = True  # if 1 is taken set to True

    if not one_is_taken:  # if 1 is not taken return 0
        x = 0
        return x
    if game1.player == "Max":  # if the player is max
        if y == 1:  # the last taken token is 1
            if len(list1) % 2 == 0:  # if the count of the possible successors is even return -0.5
                x = -0.5
                return x
            else:  # if the count of the possible successors is odd return 0.5
                x = 0.5
                return x
        if sympy.isprime(y):  # the last taken token is prime number
            child_list = remove_all_available_tokens(list1, game1)  # return all the possible successors
            for child in child_list:  # check for any multiple of the prime number in the  successors
                for number in child.remaining_token:
                    if number % y == 0:  # when a multiple is found increase the number of multiples by 1
                        multiplies = multiplies + 1
            if multiplies % 2 == 0:  # if the count of the multiples  is even return -0.7
                x = -0.7
                return x
            else:  # if the count of the multiples  is odd return 0.7
                x = 0.7
                return x
        if not sympy.isprime(y):  # the last taken token is composite number
            max_prime = 0  # the largest prime that can divide the last taken token
            for number in game1.remaining_token:
                if y % number == 0:  # check if the number can divide the lase taken token
                    print(number)
                    if sympy.isprime(number):  # check if the number is prime
                        if number > max_prime:  # set max prime to the number we found
                            max_prime = number
            if max_prime > 0:  # if a prime number was found
                child_list = remove_all_available_tokens(list1, game1)
                for child in child_list:  # check for any multiple of the prime number in the  successors
                    for number in child.remaining_token:
                        if number % max_prime == 0:  # when a multiple is found increase the number of multiples by 1
                            multiplies = multiplies + 1
                print("the length of the multiples ", multiplies)
                if multiplies % 2 != 0:  # if the count of the multiples  is odd return 0.6
                    x = 0.6
                    return x
                else:  # if the count of the multiples  is even return -0.6
                    x = -0.6
                    return x
            else:  # any other case return -0.6
                x = -0.6
                return x
    else:
        if y == 1:
            if len(list1) % 2 == 0:
                x = 0.5
                return x
            else:
                x = -0.5
                return x
        if sympy.isprime(y):
            child_list= remove_all_available_tokens(list1,game1)
            for child in child_list:
                for number in child.remaining_token:
                    multiplies = multiplies + 1
            if multiplies % 2 == 0:
                x = 0.7
                return x
            else:
                x = -0.7
                return x
        if not sympy.isprime(y):
            max_prime = 0
            for number in game1.remaining_token:
                if y % number == 0:
                    if sympy.isprime(number):
                        if number > max_prime:
                            max_prime = number
            if max_prime > 0:
                child_list= remove_all_available_tokens(list1,game1)
                for child in child_list:
                    for number in child.remaining_token:
                        if number % max_prime == 0:
                            multiplies = multiplies +1
                if multiplies % 2 != 0:
                    x = -0.6
                    return x
                else:
                    x = 0.6
                    return x
            else:
                x = 0.6
                return x
            
            
def build_search_tree(game1):
    tree1 = [game1]
    tree2 = [game1]
    print("the first element in the tree is :", tree1[0].list_token_taken)
    while tree1:
        test = tree1.pop(0)
        list1 = tokens_to_remove(test)
        if list1:
            child_list = remove_all_available_tokens(list1, test)
            for x in child_list:
                tree2.append(x)
                list2 = tokens_to_remove(x)
                if list2:
                    tree1.append(x)

    return tree2

def main():
    game1 = game(7, 2, [1, 3], 2, None)
    print("the player is :", game1.player)
    print("the player took these tokens", game1.list_token_taken)
    print("the remaining tokens are :", game1.remaining_token)
    search_tree = build_search_tree(game1)
    print("the elements in the tree")
    for x in search_tree:
        print("the element is", x.list_token_taken,"the player turn is",x.player, " the depth is ", x.depth)



if __name__ == '__main__':
    main()
