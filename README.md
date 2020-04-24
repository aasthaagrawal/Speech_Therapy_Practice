# Speech_Therapy_Practice

Speech Therapy Practice is an Alexa skill for at-home practice of difficult sounds for people with speech disabilities. User could use their echo device to practice with this skill. 

The skill is developed using Alexa SDK, Python and Amazon Lambda functions.

## Invocation
To open the skill, speak: "Alexa, open Speech Practice"

## Description of application flow
Our skill provides session based practice to the users. A session is created based on user's choice of sound they want to practice, skill level/practice type (words, phrases and sentences) and how many items they want to practice. These user choices are stored as session level attributes. We provide the flexibility to the user to change these choices at any point of time throughout the session. As of now, we have added support for three sounds - 1. R 2. S and 3. L

Using the above three mentioned properties, we create a session and walk the user through a series of practice items. For each practice item, user's speech is captured, analyzed and a useful feedback is provided. We validate each practice item at word level granuality - focusing on words which contain the selected sound. If a user makes a mistake, we highlight where they went wrong and encourage them to speack the entire practice item once again. We also give them flexibility to skip a practice item, if they find it too hard. As of now, we only look for mispronunciation errors in user's speech.

## Basic code flow
* Intent descriptions could be found at interactionModels/custom/en-US.json
* Intent handlers could be found at lambda/lambda_function.py 
* Current collection of practice items is stored in lambda/collection.json
* Alexa responses are stored at lambda/language_strings.json

## User-device interaction


## Future work
* Support for persisting user profile across sessions
* Intent chaining to make the user-device interaction after each practice item more smooth
* Adding more alexa responses to make the session more interesting
* Support for dynamic addition of practice items
* Growing our collection of practice items
* Making session create action faster for repetitive users (giving them option to directly feed in the three choices instead of walking them through each one by one)
