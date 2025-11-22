// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing chatbot...');

    // Get DOM elements
    var chatContainer = document.getElementById('chat-container');
    var userInput = document.getElementById('user-input');
    var sendBtn = document.getElementById('send-btn');
    var typingIndicator = document.getElementById('typing-indicator');
    var weatherBtn = document.getElementById('weather-btn');
    var timerBtn = document.getElementById('timer-btn');
    var timeBtn = document.getElementById('time-btn');
    var gameBtn = document.getElementById('game-btn');
    var snakeBtn = document.getElementById('snake-btn');

    // Check if elements are found
    console.log('Game button found:', gameBtn);
    console.log('Weather button found:', weatherBtn);
    console.log('Timer button found:', timerBtn);
    console.log('Time button found:', timeBtn);
    console.log('Snake button found:', snakeBtn);

    // Modal elements
    var weatherModal = document.getElementById('weather-modal');
    var weatherLoadingModal = document.getElementById('weather-loading-modal');
    var weatherSuccessModal = document.getElementById('weather-success-modal');
    var weatherErrorModal = document.getElementById('weather-error-modal');
    var timerModal = document.getElementById('timer-modal');
    var timerRunningModal = document.getElementById('timer-running-modal');
    var timerFinishedModal = document.getElementById('timer-finished-modal');
    var gameModal = document.getElementById('game-modal');
    var gameWonModal = document.getElementById('game-won-modal');
    var snakeLinkModal = document.getElementById('snake-link-modal');

    var cityInput = document.getElementById('city-input');
    var loadingCity = document.getElementById('loading-city');
    var weatherSuccessCity = document.getElementById('weather-success-city');
    var weatherSuccessInfo = document.getElementById('weather-success-info');
    var weatherErrorCity = document.getElementById('weather-error-city');

    var timerCountdown = document.getElementById('timer-countdown');

    // Timer input elements
    var timerHours = document.getElementById('timer-hours');
    var timerMinutes = document.getElementById('timer-minutes');
    var timerSeconds = document.getElementById('timer-seconds');
    var totalSecondsDisplay = document.getElementById('total-seconds-display');

    // Game elements
    var guessInput = document.getElementById('guess-input');
    var submitGuess = document.getElementById('submit-guess');
    var newGameBtn = document.getElementById('new-game');
    var closeGameBtn = document.getElementById('close-game');
    var playAgainBtn = document.getElementById('play-again');
    var closeGameWonBtn = document.getElementById('close-game-won');
    var attemptsCount = document.getElementById('attempts-count');
    var gameMessage = document.getElementById('game-message');
    var wonNumber = document.getElementById('won-number');
    var wonAttempts = document.getElementById('won-attempts');

    // Game range elements
    var minRangeInput = document.getElementById('min-range');
    var maxRangeInput = document.getElementById('max-range');
    var setRangeBtn = document.getElementById('set-range');
    var currentMin = document.getElementById('current-min');
    var currentMax = document.getElementById('current-max');
    var wonRange = document.getElementById('won-range');

    // Weather buttons
    var confirmWeather = document.getElementById('confirm-weather');
    var cancelWeather = document.getElementById('cancel-weather');
    var closeWeatherSuccess = document.getElementById('close-weather-success');
    var retryWeather = document.getElementById('retry-weather');
    var closeWeatherError = document.getElementById('close-weather-error');

    // Timer buttons
    var startTimer = document.getElementById('start-timer');
    var cancelTimer = document.getElementById('cancel-timer');
    var stopTimer = document.getElementById('stop-timer');
    var closeTimer = document.getElementById('close-timer');

    // Snake buttons
    var confirmSnakeLink = document.getElementById('confirm-snake-link');
    var cancelSnakeLink = document.getElementById('cancel-snake-link');

    // Timer variables
    var timerInterval = null;
    var remainingTime = 0;

    // Game variables
    var targetNumber = 0;
    var attempts = 0;
    var gameActive = false;
    var minRange = 1;
    var maxRange = 100;

    // OpenWeatherMap API configuration
    var OPENWEATHER_API_KEY = '4f9b892a2219c03b01e425ac9bcd4240';

    // Bot responses
    var responses = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hi there! What can I do for you?",
        "help": "I can help you with weather information, timers, time, and games! Use the buttons above or type your request.",
        "thanks": "You're welcome!",
        "bye": "Goodbye! Have a great day!"
    };

    // Add message to chat
    function addMessage(message, isUser) {
        if (isUser === undefined) isUser = false;
        
        var messageDiv = document.createElement('div');
        var messageClass = isUser ? 'user-message' : 'bot-message';
        messageDiv.className = 'message ' + messageClass;
        
        messageDiv.textContent = message;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        return messageDiv;
    }

    // Format time as HH:MM:SS or MM:SS
    function formatTime(totalSeconds) {
        var hours = Math.floor(totalSeconds / 3600);
        var mins = Math.floor((totalSeconds % 3600) / 60);
        var secs = totalSeconds % 60;
        
        if (hours > 0) {
            return hours.toString().padStart(2, '0') + ':' + 
                   mins.toString().padStart(2, '0') + ':' + 
                   secs.toString().padStart(2, '0');
        } else {
            return mins.toString().padStart(2, '0') + ':' + 
                   secs.toString().padStart(2, '0');
        }
    }

    // Show typing indicator
    function showTyping() {
        typingIndicator.style.display = 'block';
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Hide typing indicator
    function hideTyping() {
        typingIndicator.style.display = 'none';
    }

    // Get bot response
    function getResponse(input) {
        input = input.toLowerCase();
        
        if (input.indexOf("weather") !== -1) {
            showWeatherModal();
            return "Please enter a city/Country name:";
        } else if (input.indexOf("timer") !== -1) {
            showTimerModal();
            return "Please enter time in hours, minutes, and seconds:";
        } else if (input.indexOf("time") !== -1) {
            return "Current time: " + new Date().toLocaleTimeString();
        } else if (input.indexOf("game") !== -1 || input.indexOf("guess") !== -1) {
            showGameModal();
            return "Let's play a guessing game! I'm thinking of a number between " + minRange + " and " + maxRange + ".";
        } else if (input.indexOf("snake") !== -1) {
            showSnakeLinkModal();
            return "Opening Snake game...";
        }
        
        for (var key in responses) {
            if (input.indexOf(key) !== -1) {
                return responses[key];
            }
        }
        
        return "I'm sorry, I don't understand that. Try asking about weather, timer, time, or game!";
    }

    // Handle user input
    function handleUserInput() {
        var input = userInput.value.trim();
        if (!input) return;
        
        addMessage(input, true);
        userInput.value = '';
        
        showTyping();
        
        setTimeout(function() {
            hideTyping();
            var response = getResponse(input);
            if (response && response.indexOf("Please enter") === -1) {
                addMessage(response);
            }
        }, 1000);
    }

    // Weather modal functions
    function showWeatherModal() {
        weatherModal.style.display = 'flex';
        cityInput.value = '';
        cityInput.focus();
    }

    function hideWeatherModal() {
        weatherModal.style.display = 'none';
    }

    function showWeatherLoadingModal(city) {
        loadingCity.textContent = city;
        weatherLoadingModal.style.display = 'flex';
    }

    function hideWeatherLoadingModal() {
        weatherLoadingModal.style.display = 'none';
    }

    function showWeatherSuccessModal(city, condition, temp) {
        weatherSuccessCity.textContent = city;
        weatherSuccessInfo.textContent = condition + ", " + temp + " Celsius";
        weatherSuccessModal.style.display = 'flex';
    }

    function hideWeatherSuccessModal() {
        weatherSuccessModal.style.display = 'none';
    }

    function showWeatherErrorModal(city) {
        weatherErrorCity.textContent = city;
        weatherErrorModal.style.display = 'flex';
    }

    function hideWeatherErrorModal() {
        weatherErrorModal.style.display = 'none';
    }

    // Timer modal functions
    function showTimerModal() {
        timerModal.style.display = 'flex';
        timerHours.value = '0';
        timerMinutes.value = '0';
        timerSeconds.value = '10';
        updateTotalSecondsDisplay();
        timerSeconds.focus();
    }

    function hideTimerModal() {
        timerModal.style.display = 'none';
    }

    function showTimerRunningModal() {
        timerRunningModal.style.display = 'flex';
    }

    function hideTimerRunningModal() {
        timerRunningModal.style.display = 'none';
    }

    function showTimerFinishedModal() {
        timerFinishedModal.style.display = 'flex';
    }

    function hideTimerFinishedModal() {
        timerFinishedModal.style.display = 'none';
    }

    // Game modal functions
    function showGameModal() {
        if (!gameActive) {
            initGame();
        }
        gameModal.style.display = 'flex';
        guessInput.focus();
        console.log('Game modal shown');
    }

    function hideGameModal() {
        gameModal.style.display = 'none';
    }

    function showGameWonModal() {
        wonNumber.textContent = targetNumber;
        wonAttempts.textContent = attempts;
        wonRange.textContent = minRange + "-" + maxRange;
        gameWonModal.style.display = 'flex';
    }

    function hideGameWonModal() {
        gameWonModal.style.display = 'none';
    }

    // Snake modal functions
    function showSnakeLinkModal() {
        snakeLinkModal.style.display = 'flex';
    }

    function hideSnakeLinkModal() {
        snakeLinkModal.style.display = 'none';
    }

    // Calculate total seconds and update display
    function calculateTotalSeconds() {
        var hours = parseInt(timerHours.value) || 0;
        var minutes = parseInt(timerMinutes.value) || 0;
        var seconds = parseInt(timerSeconds.value) || 0;
        
        return hours * 3600 + minutes * 60 + seconds;
    }

    // Update total seconds display
    function updateTotalSecondsDisplay() {
        var totalSeconds = calculateTotalSeconds();
        var hours = Math.floor(totalSeconds / 3600);
        var minutes = Math.floor((totalSeconds % 3600) / 60);
        var seconds = totalSeconds % 60;
        
        var displayText = "Total: ";
        if (hours > 0) {
            displayText += hours + "h ";
        }
        if (minutes > 0 || hours > 0) {
            displayText += minutes + "m ";
        }
        displayText += seconds + "s";
        
        totalSecondsDisplay.textContent = displayText;
    }

    // Set number range
    function setNumberRange() {
        var newMin = parseInt(minRangeInput.value);
        var newMax = parseInt(maxRangeInput.value);
        
        if (isNaN(newMin) || isNaN(newMax) || newMin >= newMax) {
            alert("Please enter valid numbers where minimum is less than maximum");
            return;
        }
        
        if (newMin < 1 || newMax > 1000) {
            alert("Please enter numbers between 1 and 1000");
            return;
        }
        
        minRange = newMin;
        maxRange = newMax;
        
        // Update display
        currentMin.textContent = minRange;
        currentMax.textContent = maxRange;
        guessInput.placeholder = "Enter number";
        guessInput.min = minRange;
        guessInput.max = maxRange;
        
        // Start new game with new range
        initGame();
        
        gameMessage.textContent = "Range set to " + minRange + "-" + maxRange + ". New game started!";
        gameMessage.style.color = "#28a745";
    }

    // Initialize game
    function initGame() {
        targetNumber = Math.floor(Math.random() * (maxRange - minRange + 1)) + minRange;
        attempts = 0;
        gameActive = true;
        
        attemptsCount.textContent = attempts;
        currentMin.textContent = minRange;
        currentMax.textContent = maxRange;
        gameMessage.textContent = "I'm thinking of a number between " + minRange + " and " + maxRange + ". Can you guess it?";
        gameMessage.style.color = "#007bff";
        
        // Update guess input attributes
        guessInput.placeholder = "Enter number";
        guessInput.min = minRange;
        guessInput.max = maxRange;
        guessInput.value = "";
        guessInput.focus();
        
        console.log('New game started. Target number:', targetNumber, 'Range:', minRange + '-' + maxRange);
    }

    // Check user's guess
    function checkGuess() {
        if (!gameActive) return;
        
        var userGuess = parseInt(guessInput.value);
        
        // Validate input
        if (isNaN(userGuess) || userGuess < minRange || userGuess > maxRange) {
            gameMessage.textContent = "Please enter a valid number between " + minRange + " and " + maxRange + "!";
            gameMessage.style.color = "#dc3545";
            guessInput.value = "";
            guessInput.focus();
            return;
        }
        
        attempts++;
        attemptsCount.textContent = attempts;
        
        // Check guess
        if (userGuess === targetNumber) {
            // Correct guess
            gameMessage.textContent = "Correct! You guessed the number!";
            gameMessage.style.color = "#28a745";
            gameActive = false;
            addMessage("I won the guess game in " + attempts + " attempts! The number was " + targetNumber + " (range: " + minRange + "-" + maxRange + ").", true);
            
            // Show win modal after a short delay
            setTimeout(function() {
                hideGameModal();
                showGameWonModal();
            }, 1500);
            
        } else if (userGuess < targetNumber) {
            // Too low
            minRange = userGuess + 1;
            gameMessage.textContent = "Too low! Try between " + minRange + " and " + maxRange + ".";
            gameMessage.style.color = "#ffc107";
            
            currentMin.textContent = minRange;
            guessInput.min = minRange;
            guessInput.placeholder = "Enter number (" + minRange + "-" + maxRange + ")";
            
        } else {
            // Too high
            maxRange = userGuess - 1;
            gameMessage.textContent = "Too high! Try between " + minRange + " and " + maxRange + ".";
            gameMessage.style.color = "#fd7e14";
            
            currentMax.textContent = maxRange;
            guessInput.max = maxRange;
            guessInput.placeholder = "Enter number (" + minRange + "-" + maxRange + ")";
        }
        
        guessInput.value = ""; 
        guessInput.focus();
    }

    // Start timer with countdown display in modal
    function startTimerFunction() {
        var totalSeconds = calculateTotalSeconds();
        
        if (totalSeconds <= 0) {
            alert("Please enter a valid time (at least 1 second)");
            return;
        }
        
        if (totalSeconds > 24 * 3600) {
            alert("Timer cannot be set for more than 24 hours");
            return;
        }
        
        remainingTime = totalSeconds;
        timerCountdown.textContent = formatTime(remainingTime);
        
        // Hide setup modal and show running modal
        hideTimerModal();
        showTimerRunningModal();
        
        // Create display message
        var hours = Math.floor(totalSeconds / 3600);
        var minutes = Math.floor((totalSeconds % 3600) / 60);
        var seconds = totalSeconds % 60;
        
        var message = "Timer set for ";
        if (hours > 0) message += hours + "h ";
        if (minutes > 0) message += minutes + "m ";
        if (seconds > 0) message += seconds + "s";
        
        addMessage(message, true);
        
        // Start the countdown
        timerInterval = setInterval(function() {
            remainingTime--;
            timerCountdown.textContent = formatTime(remainingTime);
            
            if (remainingTime <= 0) {
                clearInterval(timerInterval);
                timerInterval = null;
                
                // Hide running modal and show finished modal
                hideTimerRunningModal();
                showTimerFinishedModal();
                
                // Add completion message to chat
                addMessage("Timer completed! Time's up!");
            }
        }, 1000);
    }

    // Stop timer
    function stopTimerFunction() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        hideTimerRunningModal();
        
        var hours = Math.floor(remainingTime / 3600);
        var minutes = Math.floor((remainingTime % 3600) / 60);
        var seconds = remainingTime % 60;
        
        var message = "Timer stopped with ";
        if (hours > 0) message += hours + "h ";
        if (minutes > 0) message += minutes + "m ";
        message += seconds + "s remaining";
        
        addMessage(message);
    }

    // Check weather using OpenWeatherMap API
    function checkWeather() {
        var city = cityInput.value.trim();
        if (!city) {
            alert("Please enter a city name");
            return;
        }
        
        addMessage("Check weather for " + city, true);
        hideWeatherModal();
        
        // Show loading modal
        showWeatherLoadingModal(city);
        
        // Make API call to OpenWeatherMap
        var apiUrl = 'https://api.openweathermap.org/data/2.5/weather?q=' + encodeURIComponent(city) + '&appid=' + OPENWEATHER_API_KEY + '&units=metric';
        
        fetch(apiUrl)
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                hideWeatherLoadingModal();
                
                if (data.cod === 200) {
                    // Valid city - show success with real weather data
                    var temperature = Math.round(data.main.temp);
                    var condition = data.weather[0].main;
                    var cityName = data.name;
                    
                    showWeatherSuccessModal(cityName, condition, temperature);
                    addMessage("Weather in " + cityName + ": " + condition + ", " + temperature + " Celsius");
                } else {
                    // Invalid city - show error
                    showWeatherErrorModal(city);
                    addMessage("Sorry, couldn't find weather data for " + city);
                }
            })
            .catch(function(error) {
                // Network error or other issues
                console.error('Error fetching weather data:', error);
                hideWeatherLoadingModal();
                showWeatherErrorModal(city);
                addMessage("Failed to fetch weather data due to a network error.");
            });
    }

    // Open Snake game
    function openSnakeGame() {
        window.open('http://127.0.0.1:5001', '_blank');
        hideSnakeLinkModal();
        addMessage('Opened Snake Game at http://127.0.0.1:5001', 'user');
    }

    // Event listeners using addEventListener
    if (sendBtn) {
        sendBtn.addEventListener('click', handleUserInput);
    }

    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleUserInput();
            }
        });
    }

    if (weatherBtn) {
        weatherBtn.addEventListener('click', function() {
            addMessage("Check weather", true);
            showWeatherModal();
        });
    }

    if (timerBtn) {
        timerBtn.addEventListener('click', function() {
            addMessage("Set timer", true);
            showTimerModal();
        });
    }

    if (timeBtn) {
        timeBtn.addEventListener('click', function() {
            addMessage("Current time", true);
            showTyping();
            setTimeout(function() {
                hideTyping();
                addMessage("Current time: " + new Date().toLocaleTimeString());
            }, 1000);
        });
    }

    if (gameBtn) {
        gameBtn.addEventListener('click', function() {
            console.log('Game button clicked');
            addMessage("Start guess game", true);
            showGameModal();
        });
    }

    if (snakeBtn) {
        snakeBtn.addEventListener('click', function() {
            addMessage("Open Snake game", true);
            showSnakeLinkModal();
        });
    }

    // Weather event listeners
    if (confirmWeather) confirmWeather.addEventListener('click', checkWeather);
    if (cancelWeather) cancelWeather.addEventListener('click', hideWeatherModal);
    if (closeWeatherSuccess) closeWeatherSuccess.addEventListener('click', hideWeatherSuccessModal);
    if (retryWeather) retryWeather.addEventListener('click', function() {
        hideWeatherErrorModal();
        showWeatherModal();
    });
    if (closeWeatherError) closeWeatherError.addEventListener('click', hideWeatherErrorModal);

    // Timer event listeners
    if (startTimer) startTimer.addEventListener('click', startTimerFunction);
    if (cancelTimer) cancelTimer.addEventListener('click', hideTimerModal);
    if (stopTimer) stopTimer.addEventListener('click', stopTimerFunction);
    if (closeTimer) closeTimer.addEventListener('click', hideTimerFinishedModal);

    // Game event listeners
    if (submitGuess) submitGuess.addEventListener('click', checkGuess);
    if (newGameBtn) newGameBtn.addEventListener('click', initGame);
    if (closeGameBtn) closeGameBtn.addEventListener('click', hideGameModal);
    if (playAgainBtn) playAgainBtn.addEventListener('click', function() {
        hideGameWonModal();
        initGame();
        showGameModal();
    });
    if (closeGameWonBtn) closeGameWonBtn.addEventListener('click', hideGameWonModal);
    if (setRangeBtn) setRangeBtn.addEventListener('click', setNumberRange);

    // Snake event listeners
    if (confirmSnakeLink) confirmSnakeLink.addEventListener('click', openSnakeGame);
    if (cancelSnakeLink) cancelSnakeLink.addEventListener('click', hideSnakeLinkModal);

    // Timer input event listeners
    if (timerHours) timerHours.addEventListener('input', updateTotalSecondsDisplay);
    if (timerMinutes) timerMinutes.addEventListener('input', updateTotalSecondsDisplay);
    if (timerSeconds) timerSeconds.addEventListener('input', updateTotalSecondsDisplay);

    if (timerHours) {
        timerHours.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') startTimerFunction();
        });
    }
    if (timerMinutes) {
        timerMinutes.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') startTimerFunction();
        });
    }
    if (timerSeconds) {
        timerSeconds.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') startTimerFunction();
        });
    }

    // Game input event listener
    if (guessInput) {
        guessInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') checkGuess();
        });
    }

    // Range input event listeners
    if (minRangeInput) {
        minRangeInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') setNumberRange();
        });
    }
    if (maxRangeInput) {
        maxRangeInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') setNumberRange();
        });
    }

    // Enter key in weather modal
    if (cityInput) {
        cityInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') checkWeather();
        });
    }

    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === weatherModal) hideWeatherModal();
        if (e.target === timerModal) hideTimerModal();
        if (e.target === gameModal) hideGameModal();
        if (e.target === gameWonModal) hideGameWonModal();
        if (e.target === weatherSuccessModal) hideWeatherSuccessModal();
        if (e.target === weatherErrorModal) hideWeatherErrorModal();
        if (e.target === timerFinishedModal) hideTimerFinishedModal();
        if (e.target === snakeLinkModal) hideSnakeLinkModal();
    });

    // Initialize game when page loads
    initGame();
    
    console.log('Chatbot initialized successfully! All event listeners attached.');
});