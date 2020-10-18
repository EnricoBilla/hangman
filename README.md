# hangman
One-liner hangman in python

## Why?
They challenged me, I had to

## How?
I started with a basic idea, which you can see here:

```
word = "xylophone"
guess = ""
count = 5

for _ in range(count):
    a = input()
    if len(a) == 1:
        guess = guess + a
    else:
        print("Yass" if a == word else "Nope")
    print(''.join(word[i] if (word[i] in guess or i==0 or i==len(word)-1) else "_" for i in range(len(word)))+"\n")
```

`word` contains the word the player has to guess, `count` contains the number of errors the player can make and `guess` is the list of characters the player guessed.

This had two main problems:
- you had to guess the specific word to win, guessing all characters of the word won't make you win
- even correct characters are considered wrong when counting errors (but I found it later)

But, most importantly it wouldn't end right after you guessed the right word, but you have to use all  your remaining guesses to end the game; so let's fix this now.

```
word = "xylophone"
guess = []
count = [False] + [True]*5

while count.pop():
    print("Yass" if (guess.append(input(''.join(word[i] if (word[i] in guess or i==0 or i==len(word)-1) else "_" for i in range(len(word)))+"\n")) or (guess[-1]==word and (count.sort(reverse=True) or True))) else "Retry")
```

Instead of having a `for` that iterates a fixed number of times, now I'm using a `while` loop that pops the last element of the list `count`, which is now a list of booleans, once all `True`s are popped the remaining element is `False` so the `while` loop ends.

Now `guess`, instead of being a `string`, is a `list` of `string`s so that every input by the user is in a different item. This way I can check whether the last input was the correct word separately.

I also edited things in the loop, instead of having separate `input()` and `print()` I exploited the fact that input can also print to do both in one single line.

In this last snippet, I also used a _short-circuit evaluation_ to do multiple things in one line, which is basically the idea behing the all program; you'll see later. After the player wrote his guess, the input is appended to `guess` through `list.append()`, which doesn't return anything (`void` functions in python return `None`, which is _falsy_).


That means that to evaluate the expression the program has also to evaluate the next condition after the `or`, which is `guess[-1]==word and (count.sort(reverse=True) or True)`. Having an `and` as operator, both conditions here must be `True`, so if the last guess of the player isn't equal to `word` the program would skip the other expressions, having already got a `False` result. If the player guesses correctly, the `count` list would sort in descending order (`False` at the end); `list.sort()` does not return so I added a `or True` in order to print the _You won_ string.

Now I wanted to fix the fact that in order to win the player had to guess the whole word and it wasn't enough to guess all the characters:

```
word = "xylophone"
guess = []
count = [False] + [True]*10

while count.pop():
    print("Congrats, it was {}".format(count.sort(reverse=True) or word) if (guess.append(input(''.join(word[i] if (word[i] in guess or i==0 or i==len(word)-1) else "_" for i in range(len(word)))+"\n")) or guess[-1]==word or set(guess).issuperset(word[1:-1])) else ("Retry" if count[-1] else "It was {} :(".format(word)))
```

Here, I just added the `set(guess).issuperset(word[1:-1])` which checks whether all characters (excluding first and last) have been guessed by the player. The only other thing I did is to move the `list.sort(...)` thing inside the `.format()` of the winning string for readablity (_yes, I said readability lol_).

Time to get rid of the last problem, the wrong counting of errors:

```
word = "xylophone"
guess = []
count = [False] + [True]*10

while count[-1]:
    print("Congrats, it was {}".format(count.sort(reverse=True) or word) if (guess.append(input(''.join(word[i] if (word[i] in guess or i==0 or i==len(word)-1) else "_" for i in range(len(word)))+"\n")) or ((guess[-1] in word[1:-1] or guess[-1] in guess[:-1] or count.pop()) and False) or guess[-1]==word or set(guess).issuperset(word[1:-1])) else ("Retry" if count[-1] else "It was {} :(".format(word)))
```

Before, every input was considered an error, but only wrong characters should be considered error. To fix this instead of popping the list every cycle of the `while` loop I decided to call `.pop()` only if conditions are met later in the program.

So, I added to the boolean expression `guess[-1] in word[1:-1] or guess[-1] in guess[:-1] or count.pop()` all `and`ed with a False, to not modify the whole meaning of that boolean expression. That line pops the `count` list only if the guessed characters is not in the word and if that same guess had not been guessed previously.

Well, now it's finished, right? _No_, I have been able to do all this in only 5 lines, 3 of which are only variables initialisation and 2 are the program itself. I can do better.

```
var = ["xylophone", [], [False] + [True]*10]

while var[2][-1]: print("Congrats, it was {}".format(var[2].sort(reverse=True) or var[0]) if (var[1].append(input(''.join(var[0][i] if (var[0][i] in var[1] or i==0 or i==len(var[0])-1) else "_" for i in range(len(var[0])))+"\n")) or ((var[1][-1] in var[0][1:-1] or var[1][-1] in var[1][:-1] or var[2].pop()) and False) or var[1][-1]==var[0] or set(var[1]).issuperset(var[0][1:-1])) else ("Retry" if var[2][-1] else "It was {} :(".format(var[0])))
```

Since inside the loop there is only one method called, it can be put on the same line of the `while`. Also, it's possible to use a single list to contain all the three variables; doing so I ended up having only _two_ lines of code.

Now the last challenge, write the two lines as a single line. The first thing that came to my mind was to put the `while` inside a `lambda` and call it with variables as parameters. Easy no? _No_, obviously!
In fact, in python `while` is a statement and `lambda`s cannot contain statement...
I had to find another solution, and the only thing I came up to was converting the `while` into something else that could be repeated until a condition is met; I tried `map()`, `filter()` and other things. The only thing that could work is using an inline `for`.

So I stepped back, and edited the code to work with a different type of loop:


```
word = "xylophone"
guess = []
count = [False] + [True]*10

for _ in count:
    print("", end=(("Congrats, it was {}\n".format(count.sort(reverse=True) or word) if (guess.append(input(''.join(word[i] if (word[i] in guess or i==0 or i==len(word)-1) else "_" for i in range(len(word)))+"\n> ")) or (count.insert(0, False) and False) or ((guess[-1] in word[1:-1] or guess[-1] in guess[:-1] or count.pop()) and False) or guess[-1]==word or set(guess).issuperset(word[1:-1])) else ("You lose, it was {} :(\n".format(word) if not count[-1] else "")) if count[-1] else ""))
```

I decided to cycle every element of the `count` list, and every cycle I add a new element at the start of the list with the same basic  trick in the boolean expression: `count.insert(0, False) and False`. Maybe `and False` is not necessary since `list.insert()` is `void` but I wanted to be sure :). Now I have an infinite loop, just gotta add a terminating condition, so I moved the condition from the old `while` to an `if` inside the `print`, if the condition is not met, just print nothing.

The point is that by default `print()` prints a new line at the end, but the behaviour can be set using the `end` parameter of the `print()` function, so I had to create a condition to decide whether I wanted a new line. Instead of doing that I moved everything to the `end` parameter, and leaving the first parameter of `print()` empty.

Now that I have a for with only a method inside of it I can put everything inside a `lambda` and call it directly with the parameters I want instead of creating a new variable:

```
(lambda word, guess, count: [print("", end=(("Congrats, it was {}\n".format(count.sort(reverse=True) or word) if (guess.append(input(''.join(word[i] if (word[i] in guess or i==0 or i==len(word)-1) else "_" for i in range(len(word)))+"\n> ")) or (count.insert(0, False) and False) or ((guess[-1] in word[1:-1] or guess[-1] in guess[:-1] or count.pop()) and False) or guess[-1]==word or set(guess).issuperset(word[1:-1])) else ("You lose, it was {} :(\n".format(word) if not count[-1] else "")) if count[-1] else "")) for _ in count])("xylophone", [], [False] + [True]*10)
```

And here is the final result, a **one-liner hangman**!
