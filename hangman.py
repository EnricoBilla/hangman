(lambda word, guess, count: [count[-1] and print("", end=(("Congrats, it was {}\n".format(count.sort(reverse=True) or word) if (guess.append(input(''.join(word[i] if (word[i] in guess or i==0 or i==len(word)-1) else "_" for i in range(len(word)))+"\n> ")) or (count.insert(0, False) and False) or ((guess[-1] in word[1:-1] or guess[-1] in guess[:-1] or count.pop()) and False) or (guess[-1]==word and (count.sort(reverse=True) or True)) or set(guess).issuperset(word[1:-1])) else ("You lose, it was {} :(\n".format(word) if not count[-1] else "")) if _ else "")) for _ in count])("cane", [], [False] + [True]*5)
