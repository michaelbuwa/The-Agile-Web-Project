document.addEventListener('DOMContentLoaded', () => {
  const startButton = document.getElementById('start-button');
  const timer = document.getElementById('timer');
  const timeLeft = document.getElementById('time-left');
  const blackScreen = document.getElementById('black-screen');
  const blackTimeLeft = document.getElementById('black-time-left');
  const colorSelection = document.getElementById('color-selection');
  const colorOptions = document.getElementById('color-options');
  const result = document.getElementById('result');
  const resultMessage = document.getElementById('result-message');
  const againButton = document.getElementById('again-button');
  const finishButton = document.getElementById('finish-button');
  
  
  let correctColor = '';
  let countdown;
  
  //For tracking correct and incorrect answers
  let correctGuesses = 0;
  let incorrectGuesses = 0;
  const colorTracker = []; // an Array that stores all user results: correct and incorrect guesses
  // and all options shown to the user

  // Generate a random color
  function getRandomColor() {
      const r = Math.floor(Math.random() * 256);
      const g = Math.floor(Math.random() * 256);
      const b = Math.floor(Math.random() * 256);
      return `rgb(${r}, ${g}, ${b})`;
  }

  // Generate a similar color
  function getSimilarColor(baseColor) {
      const [r, g, b] = baseColor.match(/\d+/g).map(Number);
      const variation = 20; 
      const newR = Math.min(255, Math.max(0, r + (Math.random() > 0.5 ? variation : -variation)));
      const newG = Math.min(255, Math.max(0, g + (Math.random() > 0.5 ? variation : -variation)));
      const newB = Math.min(255, Math.max(0, b + (Math.random() > 0.5 ? variation : -variation)));
      return `rgb(${newR}, ${newG}, ${newB})`;
  }

  // Start the test
  startButton.addEventListener('click', () => {
      //const navbar = document.getElementById('navbar');
      const navbar = document.querySelector('.navbar');
      navbar.style.display = 'none'; // The nav bar is hidden
      const initialColor = getRandomColor();
      document.body.style.backgroundColor = initialColor;
      startButton.classList.add('hidden'); // Hide the start button after generating the color
      document.querySelector('.test-container').classList.add('hidden'); // Hide the test container text

      timer.classList.remove('timer-hidden');
      let time = 10;
      timeLeft.textContent = time;

      countdown = setInterval(() => {
          time--;
          timeLeft.textContent = time;

          if (time === 0) {
              clearInterval(countdown);
              timer.classList.add('timer-hidden'); // Hide the timer when it reaches 0

              // Set to black screen
              blackScreen.classList.remove('hidden');
              blackScreen.style.transform = 'translateY(0)';

              let blackTime = 5;
              blackTimeLeft.textContent = blackTime;

              const blackCountdown = setInterval(() => {
                  blackTime--;
                  blackTimeLeft.textContent = blackTime;

                  if (blackTime === 0) {
                      clearInterval(blackCountdown);

                      // Hide black screen and reset background
                      blackScreen.style.transform = 'translateY(-100%)';
                      blackScreen.classList.add('hidden');
                      
                      document.body.style.backgroundColor = '#f4f4f4';

                      // Show color options
                      const options = [
                          getSimilarColor(initialColor),
                          getSimilarColor(initialColor),
                          initialColor,
                      ];
                      options.sort(() => Math.random() - 0.5);

                      correctColor = initialColor;

                      options.forEach((color, index) => {
                          const option = document.getElementById(`option-${index + 1}`);
                          option.style.backgroundColor = color;
                          option.dataset.color = color;
                          option.classList.remove('hidden');
                      });
                      colorSelection.classList.remove('hidden');
                      document.getElementById('selection-message').classList.remove('hidden');
                      colorOptions.classList.remove('hidden');
                  }
              }, 1000); // 1-second interval
          }
      }, 1000); // 1-second interval
  });

  colorOptions.addEventListener('click', (e) => {
    if (e.target.classList.contains('color-container')) {
        const selectedColor = e.target.dataset.color;
        // Remove the 'selected' class from all containers
        document.querySelectorAll('.color-container').forEach(container => {
            container.classList.remove('selected');
        });

        // Add the 'selected' class to the clicked container
        e.target.classList.add('selected');

        // Disable further clicks on the color options
        colorOptions.style.pointerEvents = 'none';

        // Determine if the match is correct
        const isCorrect = selectedColor === correctColor;

        // Send the result to the backend
        fetch('/api/update_match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                is_correct: isCorrect,
                selected_color: selectedColor,
                correct_color: correctColor
        }),

        })
        .then(response => response.json())
        .then(data => {
            console.log('Match result updated:', data);
        })
        .catch(err => console.error('Error updating match result:', err));

        if (selectedColor === correctColor) {
            correctGuesses++; // Increment the correct colour counter
            e.target.classList.add('correct');
            resultMessage.textContent = 'This color match was correct!';
            resultMessage.style.color = 'green'; // Set feedback text color to green

            // Log the result in the console
            console.log(`Selected Color: ${selectedColor}`);
            console.log('Result: Correct');
        } else {
            incorrectGuesses++; //Increment the incorrect colour counter
            e.target.classList.add('incorrect');
            resultMessage.textContent = 'This color match was incorrect!';
            resultMessage.style.color = 'red'; // Set feedback text color to red

            // Log the result in the console
            console.log(`Selected Color: ${selectedColor}`);
            console.log('Result: Incorrect');
        }

        // Highlight all color containers to show the correct and incorrect colors
        document.querySelectorAll('.color-container').forEach(container => {
            if (container.dataset.color === correctColor) {
                container.classList.add('correct');
            } else {
                container.classList.add('incorrect');
            }
        });

        // Log the correct color in the console
        console.log(`Correct Color: ${correctColor}`);

        const colorsGiven = { // Use the console log to double check results BEFORE sending to the database
            round: colorTracker.length + 1,
            selectedColor: selectedColor,
            correctColor: correctColor,
            wasCorrect: selectedColor === correctColor,
            correctCount: correctGuesses,
            incorrectCount: incorrectGuesses,
            //Fetch the colors of the options
            optionIds: ['option-1', 'option-2', 'option-3'].join(', '),
            optionColors: [
                document.getElementById('option-1').dataset.color,
                document.getElementById('option-2').dataset.color,
                document.getElementById('option-3').dataset.color
            ].join(' | ')
          };
    
        colorTracker.push(colorsGiven);
        //Shows in the table format
        console.table(colorTracker);

        // Show the result message and hide the color options
        result.classList.remove('hidden');
        colorOptions.classList.add('hidden');
    }
});

  // Restart & Finish the test
  againButton.addEventListener('click', () => {
      location.reload(); // Reload the page
  });

  finishButton.addEventListener('click', () => {
      const url = finishButton.dataset.url;
      window.location.href = url;
  // Redirect to the visualise.html page
  });
});
