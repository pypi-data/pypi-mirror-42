def help_menu():
    print('Let\'s start sorting\n'
          'Here are the options:...\n'
          'Press "b" for Bubble Sort\n'
          'Press "i" for Insertion Sort \n'
          'Press "q" for Quick Sort\n'
          'Press "s" for Selection Sort\n'
          'Press "e" to exit\n'
          'Press "h" for help\n'
          )

    while True:
        # numbers = input("What would you like to sort?")
        numbers = [54, 26, 93, 17, 77, 31, 44, 55, 20]
        user_input = input("How would you like to sort? ")
        if user_input == 'b':
            bubble_sort(numbers)
            continue
        elif user_input == 'i':
            insertion_sort(numbers)
            continue
        elif user_input == 'q':
            quick_sort(numbers)
            continue
        elif user_input == 's':
            selection_sort(numbers)
            continue
        elif user_input == 'h':
            help_menu()
            continue
        elif user_input == 'e':
            print('Goodbye! Thanks for sorting!')
            break
        else:
            print('Please pick a sort')
            help_menu()
            continue
