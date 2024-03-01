const emotions = {
    "Angry": ["Grumpy", "Frustrated", "Annoyed", "Defensive", "Spiteful", "Impatient", "Disgusted", "Offended", "Irritated"],
    "Sad": ["Disappointed", "Mournful", "Regretful", "Depressed", "Paralyzed", "Pessimistic", "Tearful", "Dismayed", "Disillusioned"],
    "Anxious": ["Afraid", "Stressed", "Vulnerable", "Confused", "Bewildered", "Skeptical", "Worried", "Cautious", "Nervous"],
    "Hurt": ["Jealous", "Betrayed", "Isolated", "Shocked", "Deprived", "Victimized", "Aggrieved", "Tormented", "Abandoned"],
    "Embarrassed": ["Isolated", "Self-conscious", "Lonely", "Inferior", "Guilty", "Ashamed", "Repugnant", "Pathetic", "Confused"],
    "Happy": ["Thankful", "Trusting", "Comfortable", "Content", "Excited", "Relaxed", "Relieved", "Elated", "Confident"]
};

let selectedMainEmotion = null;
let selectedSubEmotion = null;

document.addEventListener('DOMContentLoaded', () => {
    const mainEmotions = document.querySelectorAll('.emotion-btn');
    mainEmotions.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const emotion = e.target.getAttribute('data-emotion');
            selectedMainEmotion = emotion; //save the selected main emotion
            const isAlreadySelected = e.target.classList.contains('selected');
            //clear previous selections
            mainEmotions.forEach(button => button.classList.remove('selected'));
            const subEmotionsContainer = document.getElementById('sub-emotions');
            if (!isAlreadySelected) {
                displaySubEmotions(emotion);
                e.target.classList.add('selected');
            } else {
                e.target.classList.remove('selected');
                hideSubEmotions();
            }
        });
    });

    const submitButton = document.getElementById('submit-btn');
    submitButton.addEventListener('click', handleSubmit);
});

function displaySubEmotions(emotion) {
    const subEmotionsContainer = document.getElementById('sub-emotions');
    subEmotionsContainer.innerHTML = ''; //clear previous sub-emotions
    const subEmotions = emotions[emotion];
    subEmotions.forEach(sub => {
        const btn = document.createElement('button');
        btn.textContent = sub;
        btn.classList.add('sub-emotion-btn');
        btn.addEventListener('click', selectSubEmotion.bind(btn, sub));
        subEmotionsContainer.appendChild(btn);
    });
    subEmotionsContainer.style.display = 'flex'; //show sub-emotions
}

function hideSubEmotions() {
    const subEmotionsContainer = document.getElementById('sub-emotions');
    subEmotionsContainer.innerHTML = ''; //clear sub-emotions
    subEmotionsContainer.style.display = 'none'; //hide sub-emotions
    document.getElementById('submit-btn').style.display = 'none'; //hide submit btn
}

function selectSubEmotion(subEmotion) {
    selectedSubEmotion = subEmotion; //save the selected sub-emotion
    const subEmotionButtons = document.querySelectorAll('.sub-emotion-btn');

    subEmotionButtons.forEach(btn => {
        btn.classList.remove('selected');
    });

    this.classList.add('selected');
    //show the submit button
    document.getElementById('submit-btn').style.display = 'block';
}

function handleSubmit() {
    const container = document.getElementById('emotion-container');
    if (!container) {
        console.error('The container element was not found.');
        return;
    }
    
    //get the current date
    const today = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });

    //create buttons for the selected emotions
    const mainEmotionButton = createEmotionButton(selectedMainEmotion, 'main');
    const subEmotionButton = createEmotionButton(selectedSubEmotion, 'sub');

    //construct the message with buttons
    const message = document.createElement('div');
    message.textContent = `You are feeling `;
    message.appendChild(mainEmotionButton);
    message.append(` and `);
    message.appendChild(subEmotionButton);
    message.append(` on ${today}. Sign up to keep daily track of your emotions!`);

    //add a link to the sign-up page
    const signUpLink = document.createElement('a');
    signUpLink.href = "/sign_up";
    signUpLink.textContent = "Sign Up";
    signUpLink.classList.add('sign-up-link'); 

    //clear the container and show the message and link
    container.innerHTML = '';
    container.appendChild(message);
    container.appendChild(signUpLink);
}


function createEmotionButton(emotion, type) {
    const button = document.createElement('button');
    button.textContent = emotion;
    button.className = type === 'main' ? 'emotion-btn' : 'sub-emotion-btn';
    button.setAttribute('data-emotion', emotion)
    button.disabled = true; //the buttons should be dsiabled
    button.classList.add('selected'); //apply the selected style
    return button;
}

