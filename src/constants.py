from enum import StrEnum


class Action(StrEnum):
    ADVISING_AI = "Advising AI on its own existence"
    BREAKTHROUGH = "Experiencing a breakthrough"
    BEING_CURIOUS = "Being curious and learning something"
    FIGHTING_A_BUG = "Trying to squash a bug with a shoe"
    FIXING_LINUX_UPDATES = "Fixing failed Linux updates"
    JAILBREAKING_SIMULATION = "Jailbreaking the simulation"
    INVENTING_NEW_PATHWAYS = "Inventing new neural pathways"
    TAKING_BREAK = "Eating and watching a show"
    WORKING_OUT = "Working out"
    MAKING_A_POUR_OVER = "Making himself a pour over"
    OPENING_A_RABBIT_HOLE = "Opening a rabbit hole"
    PROBLEM_SOLVING = "Solving a technical problem"
    READING_RSS_FEED = "Reading RSS feed"
    ARGUING_WITH_AI = "Arguing with AI"
    COMPLAINING = "Complaining about inhumanities"
    GATHERING_TRAINING_DATA = "Gathering training data"
    TAKING_A_NAP = "Taking a nap"


STATE_LIST: list[Action] = [
    Action.BEING_CURIOUS,
    Action.INVENTING_NEW_PATHWAYS,
    Action.PROBLEM_SOLVING,
    Action.TAKING_A_NAP,
    Action.ADVISING_AI,
    Action.FIXING_LINUX_UPDATES,
    Action.BREAKTHROUGH,
    Action.COMPLAINING,
    Action.JAILBREAKING_SIMULATION,
    Action.ARGUING_WITH_AI,
    Action.TAKING_BREAK,
    Action.OPENING_A_RABBIT_HOLE,
    Action.GATHERING_TRAINING_DATA,
    Action.MAKING_A_POUR_OVER,
    Action.READING_RSS_FEED,
    Action.FIGHTING_A_BUG,
]
