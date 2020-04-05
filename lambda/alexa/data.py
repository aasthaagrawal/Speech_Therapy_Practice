from gettext import gettext as _

WELCOME_MSG = _("Welcome to Speech Therapy Practice. What do you want to practice today?")
WELCOME_REMPROMPT_MSG = _("I want to practice sentences with r sound. What do you want to practice today?")
CREATE_PRACTICE_MSG =  _("Topic selected is {}. Am I correct?")
TOPIC_MISSING_MSG = _("What do you want to practice today?")
START_PRACTICE_MSG = _("Please say the word 'Speech' and then repeat after me: {}")
VALIDATION_INCORRECT_USER_SENTENCE = _("Your said {}. Let's try again! Please say the word 'Speech' and then repeat after me: {}")
VALIDATION_CORRECT_USER_SENTENCE = _("Do you want to quit or continue?")
QUIT_MESSAGE = _("Quitting the session. Bye!")
WELCOME_BACK_MSG = _(
    "Welcome back. It looks like there is {} day until your {}th birthday.")
WELCOME_BACK_MSG_plural = _(
    "Welcome back. It looks like there are {} days until your {}th birthday")
HAPPY_BIRTHDAY_MSG = _("Happy {}th birthday!")
REGISTER_BIRTHDAY_MSG = _("Thanks, I'll remember that you were born {} {} {}")
HELP_MSG = _("You can tell me your date of birth and I'll take note. You can also just say, 'register my birthday' and I will guide you. Which one would you like to try?")
GOODBYE_MSG = _("Goodbye!")
ERROR_MSG = _(
    "Sorry, I couldn't understand what you said. Can you reformulate?")
ERROR_TIMEZONE_MSG = _(
    "I can't determine your timezone. Please check your device settings and make sure a timezone was selected. After that please reopen the skill and try again!")
