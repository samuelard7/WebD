const question = document.getElementById('question');
var user_category = document.getElementById('uc').value;
var no_of_questions_input = parseInt(document.getElementById('noq').value);
var difficulty_of_question = document.getElementById('doq').value;

console.log(no_of_questions_input)

kls = difficulty_of_question.toString().value;
if (user_category == "General Knowledge"){
    user_category =9;
}
else if(user_category=="Mathematics"){
    user_category=19;
}
const choices = Array.from(document.getElementsByClassName('choice-text'));
const progressText = document.getElementById('progressText');
const scoreText = document.getElementById('score');
const progressBarFull = document.getElementById('progressBarFull');
const loader = document.getElementById('loader');
const game = document.getElementById('game');
let currentQuestion = {};
let acceptingAnswers = false;
let score = 0;
let questionCounter = 0;
let availableQuesions = [];
let questions = [];

fetch(
    `https://opentdb.com/api.php?amount=${no_of_questions_input}&category=${user_category}&difficulty=${difficulty_of_question}&type=multiple`
)
    .then((res) => {
        return res.json();
    })
    
    .then((loadedQuestions) => {
        questions = loadedQuestions.results.map((loadedQuestion) => {
            const formattedQuestion = {
                question: loadedQuestion.question,
            };

            const answerChoices = [...loadedQuestion.incorrect_answers];
            formattedQuestion.answer = Math.floor(Math.random() * 4) + 1;
            answerChoices.splice(
                formattedQuestion.answer - 1,
                0,
                loadedQuestion.correct_answer
            );

            answerChoices.forEach((choice, index) => {
                formattedQuestion['choice' + (index + 1)] = choice;
            });

            return formattedQuestion;
        });

        startGame();
    })
    .catch((err) => {
        console.error(err);
    });

//CONSTANTS
const CORRECT_BONUS = 10;

const MAX_QUESTIONS = no_of_questions_input;

startGame = () => {
    questionCounter = 0;
    score = 0;
    availableQuesions = [...questions];
    getNewQuestion();
    game.classList.remove('hidden');
    loader.classList.add('hidden');
};

getNewQuestion = () => {
    if (availableQuesions.length === 0 || questionCounter >= MAX_QUESTIONS) {
        localStorage.setItem('mostRecentScore', score);
        //go to the end page
        return (window.location.href="../templates/end.html");
    }
    questionCounter++;
    progressText.innerText = `Question ${questionCounter}/${no_of_questions_input}`;
    //Update the progress bar
    progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;

    const questionIndex = Math.floor(Math.random() * availableQuesions.length);
    currentQuestion = availableQuesions[questionIndex];
    question.innerText = currentQuestion.question;

    choices.forEach((choice) => {
        const number = choice.dataset['number'];
        choice.innerText = currentQuestion['choice' + number];
    });

    availableQuesions.splice(questionIndex, 1);
    acceptingAnswers = true;
};

choices.forEach((choice) => {
    choice.addEventListener('click', (e) => {
        if (!acceptingAnswers) return;

        acceptingAnswers = false;
        const selectedChoice = e.target;
        const selectedAnswer = selectedChoice.dataset['number'];

        const classToApply =
            selectedAnswer == currentQuestion.answer ? 'correct' : 'incorrect';

        if (classToApply === 'correct') {
            incrementScore(CORRECT_BONUS);
        }

        selectedChoice.parentElement.classList.add(classToApply);

        setTimeout(() => {
            selectedChoice.parentElement.classList.remove(classToApply);
            getNewQuestion();
        }, 1000);
    });
});

incrementScore = (num) => {
    score += num;
    scoreText.innerText = score;
};


// const question = document.getElementById('question');
// const userCategory = document.getElementById('uc').value.toLowerCase();
// const numberOfQuestions = parseInt(document.getElementById('noq').value);
// const difficultyOfQuestion = document.getElementById('doq').value.toLowerCase();

// let score = 0;
// let questionCounter = 0;
// let questions = [];

// const fetchQuestions = async () => {
//     const response = await fetch(`https://opentdb.com/api.php?amount=${numberOfQuestions}&category=${getCategoryCode(userCategory)}&difficulty=${difficultyOfQuestion}&type=multiple`);
//     const data = await response.json();
//     questions = data.results.map(formatQuestion);
//     startGame();
// };

// const formatQuestion = (loadedQuestion) => {
//     const formattedQuestion = {
//         question: loadedQuestion.question,
//         choices: [...loadedQuestion.incorrect_answers],
//         correctAnswer: loadedQuestion.correct_answer
//     };
//     formattedQuestion.choices.splice(Math.floor(Math.random() * 4), 0, formattedQuestion.correctAnswer);
//     return formattedQuestion;
// };

// const getCategoryCode = (category) => {
//     switch (category) {
//         case "general knowledge":
//             return 9;
//         case "mathematics":
//             return 19;
//         default:
//             return 9;
//     }
// };

// const startGame = () => {
//     questionCounter = 0;
//     score = 0;
//     getNewQuestion();
// };

// const getNewQuestion = () => {
//     if (questionCounter >= numberOfQuestions) {
//         localStorage.setItem('mostRecentScore', score);
//         window.location.href = 'http://127.0.0.1:3000/templates/end.html';
//         return;
//     }
//     const currentQuestion = questions[questionCounter];
//     question.innerText = currentQuestion.question;

//     const choiceElements = document.getElementsByClassName('choice-text');
//     Array.from(choiceElements).forEach((choice, index) => {
//         choice.innerText = currentQuestion.choices[index];
//         choice.onclick = () => checkAnswer(choice, currentQuestion);
//     });

//     questionCounter++;
// };

// const checkAnswer = (selectedChoice, currentQuestion) => {
//     const selectedAnswer = selectedChoice.innerText;
//     const classToApply = selectedAnswer === currentQuestion.correctAnswer ? 'correct' : 'incorrect';
//     if (classToApply === 'correct') score += 10;
//     selectedChoice.parentElement.classList.add(classToApply);
//     setTimeout(() => {
//         selectedChoice.parentElement.classList.remove(classToApply);
//         getNewQuestion();
//     }, 1000);
// };

// fetchQuestions();
