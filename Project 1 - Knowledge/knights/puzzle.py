from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # He can be either one
    Or(AKnight, AKnave),

    # If he is a knight he tells the truth, therefore he is both knight and knave
    Implication(AKnight, And(AKnight, AKnave)),

    # He can not be both at once
    Not(And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Both can be either
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    # If A is a knight he tells the truth therefore they are both knaves
    Implication(
        AKnight,
        And(BKnave, AKnave)
    ),

    # If A is a knave then they aren't both knaves, either one or none is
    Implication(
        AKnave,
        Not(And(BKnave, AKnave))
    ),

    # Cant be both at the same time
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A and B are each either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A says: "We are the same kind" → means both knights or both knaves
    Implication(
        AKnight,
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        )
    ),

    # B says: "We are of different kinds" → means one knight, one knave
    Implication(
        BKnight,
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight)
        )
    ),

    # If A is a knave, their statement is false, so they are not the same kind
    Implication(
        AKnave,
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight)
        )
    ),

    # If B is a knave, their statement is false, so they are the same kind
    Implication(
        BKnave,
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        )
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A, B and C are either knight or knave but can be both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # If A is a knight then he wouldn't say he is a knave.
    Implication(
        AKnight,
        Not(AKnave)
    ),

    # A knave would never say he is a knave
    Implication(
        AKnave,
        Not(AKnave)
    ),

    # If B is a knight then A said he was a knave
    Implication(
        BKnight,
        Implication(
            AKnight,
            AKnave
        )
    ),

    # If B is a knight then C is a Knave, otherwise C is a Knight
    Implication(
        BKnight,
        CKnave
    ),

    Implication(
        BKnave,
        CKnight
    ),

    # If C is a knight then A is a knight, otherwise A is a knave
    Implication(
        CKnight,
        AKnight
    ),

    Implication(
        CKnave,
        AKnave
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")

if __name__ == "__main__":
    main()
