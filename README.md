# Abandoned Wordle Algo

I had set out to create a binary search type of algorithm for choosing wordle letters / words.  

Ideally I would choose a letter that would split a word set between "includes that letter" : "does not include that letter".

Then I would choose a letter from each of those data sets to ~equally split those data sets.  

That would give me 3 letters I'd prioritize. 

I could also consider the middle-ish letters from those last 4 split sets.

However, I ran into trouble with smaller data sets, and a ton of if conditions to consider. 

So the current route is now to find a word from the remaining words with the best "middleness" score (but not taking into account how each letter could split the word list).

Alongside the middleness score there will also be a positional score to consider. 
