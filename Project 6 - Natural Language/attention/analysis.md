# Analysis

## Layer 2, Head 5: Articles attending to nouns

This head appears to focus on the relationship between determiners (like “the” or “a”) 
and the nouns they modify. In many sentences, the attention from the article token is strongly 
concentrated on the noun that immediately follows it.

Example sentences:
“I saw a [MASK] in the garden.” → The attention from “a” is focused on the token that fills [MASK], e.g., “flower.”
“She bought the [MASK] yesterday.” → The attention from “the” is concentrated on [MASK], e.g., “book.”

This suggests that Layer 2, Head 5 has learned to associate articles with the nouns they precede.

## Layer 7, Head 3: Verbs attending to auxiliary verbs

This head seems to capture the relationship between main verbs and auxiliary verbs 
that precede them, such as “is,” “was,” or “have.” 
The main verb token often attends strongly to the auxiliary verb that modifies its tense or aspect.

Example sentences:
“She [MASK] going to the store.” → The main verb token “going” attends to “is” in “is going.”
“They [MASK] finished the project.” → The main verb token “finished” attends to “have” in “have finished.”

This suggests that Layer 7, Head 3 is sensitive to tense and aspect by connecting verbs to their auxiliaries.

