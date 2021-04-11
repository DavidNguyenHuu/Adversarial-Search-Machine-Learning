def all_token1(s):  # will return a list for all the tokens in the game
    list1 = []
    for i in range(s + 1):
        if i != 0:
            list1.append(i)
    return list1


def remaining_token1(l1, l2):  # will return what tokens can be taken
    l3 = list(set(l1) ^ set(l2))
    return l3


def available_token1(size):  # will return the available token at the first round
    list1 = []
    for i in range(size + 1):
        if i % 2 != 0:
            list1.append(i)
    return list1


def available_token2(number, list):  # will return the available token after the first round
    list11 = []
    for i in list:
        if i % number == 0 or number % i == 0:
            list11.append(i)
    return list11


class game:

    def __init__(self, Token_number, Token_taken, List_taken_token, depth):
        self.Token_number = Token_number
        self.All_Tokens = all_token1(self.Token_number)
        self.Token_taken = Token_taken
        self.list_token_taken = []
        for i in List_taken_token:
            self.list_token_taken.append(i)
        self.remaining_token = remaining_token1(self.All_Tokens, self.list_token_taken)
        self.List_taken_token = List_taken_token
        self.depth = depth


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


def remove_token(list, game1):   # will return a new state after removing a a token
    item = list.pop(0)
    list2 = []
    list3 = []
    for i in game1.remaining_token:
        if i == item:
            game1.remaining_token.remove(i)
    list2 = game1.remaining_token
    list3 = game1.list_token_taken
    list3.append(item)
    game_child = game(game1.Token_number, game1.Token_taken + 1, list3, game1.depth + 1)
    return game_child


def main():
    game1 = game(7, 4, [3,6,2], 0)
    print("the number of tokens :", game1.Token_number)
    print("all the tokens  :", game1.All_Tokens)
    print("the number of taken tokens :", game1.Token_taken)
    print("the taken tokens  :", game1.list_token_taken)
    print("the remaining tokens  :", game1.remaining_token)
    print("the depth of the game is :", game1.depth)
    list1 = tokens_to_remove(game1)
    if list1 is not None:
        print("the available tokens to remove :", list1)
    else:
        print("you've lost the game")

    child = remove_token(list1, game1)
    print("the number of tokens in the child state:", child.Token_number)
    print("all the tokens in the child state :", child.All_Tokens)
    print("the number of taken tokens in the child state :", child.Token_taken)
    print("the taken tokens in the child state :", child.list_token_taken)
    print("the remaining tokens in the child state :", child.remaining_token)
    print("the depth of the game in the child state is :", child.depth)
    list2 = tokens_to_remove(child)
    if list2 is not None:
        print("the available tokens to remove in the child state :", list2)
    else:
        print("you've lost the game")


if __name__ == '__main__':
    main()
