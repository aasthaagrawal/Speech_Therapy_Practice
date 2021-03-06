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

<table>
  <tbody>
    <tr>
      <th>Alexa's question / Scenario</th>
      <th align="center">Response accepted</th>
    </tr>
    <tr>
      <td>Invocation / To open the alexa skill</td>
      <td>Alexa, open Speech Practice</td>
    </tr>
    <tr>
      <td>Which sound option user wants to practice</td>
      <td>
        <ul>
          <li>option {1/2/3}</li>
          <li>{1/2/3}</li>
          <li>I want to practice option {1/2/3}</li>
          <li>I want to practice {1/2/3}</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Which practice type to focus on</td>
      <td>
        <ul>
          <li>practice {words/phrases/sentences}</li>
          <li>{words/phrases/sentences}</li>
          <li>I want to practice {words/phrases/sentences}</li>
          <li>Let's do {words/phrases/sentences}</li>
          <li>I will work with {words/phrases/sentences}</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>How many practice items to practice</td>
      <td>
        <ul>
          <li>I would like to practice {number} {selected practice_type}</li>
          <li>{number} {selected practice_type}</li>
          <li>I want to practice {number} {selected practice_type}</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Practice the item</td>
      <td>{practice_item}</td>
    </tr>
    <tr>
      <td>
        <ul>
          <li>To start the session</li>
          <li>To move to the next practice item</li>
          <li>Skip practice item</li>
          <li>To continue with practice after initial number of practice items are done</li>
        </ul>
      </td>
      <td>
        <ul>
          <li>I'm ready</li>
          <li>ready</li>
          <li>I am ready</li>
          <li>next</li>
          <li>skip this sentence</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>To ask Alexa to repeat alphabet/sound options</td>
      <td>
        <ul>
          <li>Could you repeat the sound options</li>
          <li>What are my sound options</li>
          <li>Could you repeate the alphabet options</li>
          <li>Could you repeate the alphabet options</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>To quit the alexa skill</td>
      <td>
        <ul>
          <li>Quit the session</li>
          <li>Exit the session</li>
          <li>I want to exit</li>
          <li>Exit</li>
          <li>I want to quit</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## Future work
* Support for persisting user profile across sessions
* Intent chaining to make the user-device interaction after each practice item more smooth
* Adding more alexa responses to make the session more interesting
* Support for dynamic addition of practice items
* Growing our collection of practice items
* Making session create action faster for repetitive users (giving them option to directly feed in the three choices instead of walking them through each one by one)
