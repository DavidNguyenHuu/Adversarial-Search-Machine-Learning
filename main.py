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


def print_winner(game1):  # will check if the winner is Max or Min 
    if game1.Token_taken % 2 == 0:
        print("Max will win")
    else:
        print("Min will win")


def find_leaves(game1):  # will return a list of all the leaves in the game 
    leaves_list = []
    depth1 = 0
    max_depth = game1.Token_number - game1.Token_taken
    test_game = game1
    while depth1 <= max_depth:
        list1 = tokens_to_remove(test_game)
        print("the list of taken tokens", test_game.list_token_taken)
        print("the remaining tokens ", test_game.remaining_token)
        print("the tokens that can be taken", list1)
        child_list = remove_all_available_tokens(list1, test_game)
        for x in child_list:
            test_game = x
            print("we will test the game ", test_game.List_taken_token)
            list2 = tokens_to_remove(x)
            if not list2:
                leaves_list.append(x)
                print("the first leave is", leaves_list[0].List_taken_token)

        depth1 = depth1 + 1
    return leaves_list


def main():
    game1 = game(7, 0, [], 0, None)
    list1 = find_leaves(game1)
    print("the leaves list :", list1)


if __name__ == '__main__':
    main()
