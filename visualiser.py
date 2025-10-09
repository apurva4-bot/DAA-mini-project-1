<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insertion Sort Step-by-Step Visualizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 30px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            color: #666;
            font-size: 1.1em;
        }

        .controls {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
            align-items: center;
        }

        .input-group label {
            font-weight: bold;
            color: #333;
        }

        .input-group input {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
            min-width: 200px;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            color: white;
            transition: all 0.3s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .btn-primary { background: #2196F3; }
        .btn-warning { background: #FF9800; }
        .btn-danger { background: #F44336; }
        .btn-secondary { background: #607D8B; }
        .btn-success { background: #4CAF50; }

        .playback-controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }

        .speed-control {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-left: auto;
        }

        .speed-control input[type="range"] {
            width: 150px;
        }

        .visualization {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            min-height: 250px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .array-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .array-element {
            background: #E3F2FD;
            border: 3px solid #2196F3;
            border-radius: 8px;
            padding: 15px;
            min-width: 60px;
            text-align: center;
            transition: all 0.3s;
        }

        .array-element.sorted {
            background: #4CAF50;
            border-color: #388E3C;
            color: white;
        }

        .array-element.current {
            background: #FF9800;
            border-color: #F57C00;
            color: white;
            transform: scale(1.1);
        }

        .array-element.comparing {
            background: #F44336;
            border-color: #D32F2F;
            color: white;
            transform: scale(1.1);
        }

        .element-value {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .element-index {
            font-size: 0.8em;
            opacity: 0.7;
        }

        .legend {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .legend-color {
            width: 30px;
            height: 30px;
            border-radius: 5px;
            border: 2px solid #333;
        }

        .info-section {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        .info-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #ddd;
        }

        .info-box h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2em;
        }

        .info-box p {
            color: #666;
            line-height: 1.6;
        }

        .stats {
            font-size: 1.1em;
        }

        .stats div {
            margin-bottom: 10px;
        }

        .progress-section {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .progress-bar {
            flex: 1;
            height: 30px;
            background: #ddd;
            border-radius: 15px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }

        @media (max-width: 768px) {
            .info-section {
                grid-template-columns: 1fr;
            }
            
            .speed-control {
                margin-left: 0;
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔢 Insertion Sort Visualizer</h1>
            <p>Watch how insertion sort builds the sorted array one element at a time</p>
        </div>

        <div class="controls">
            <div class="input-group">
                <label>Array:</label>
                <input type="text" id="arrayInput" value="64 34 25 12 22 11 90 88">
                <button class="btn btn-primary" onclick="setCustomArray()">Set Array</button>
                <button class="btn btn-warning" onclick="generateRandomArray()">Random Array</button>
                <button class="btn btn-danger" onclick="resetVisualization()">Reset</button>
            </div>

            <div class="playback-controls">
                <button class="btn btn-secondary" onclick="firstStep()">⏮️ First</button>
                <button class="btn btn-secondary" onclick="previousStep()">⏪ Previous</button>
                <button class="btn btn-success" id="playBtn" onclick="toggleAutoPlay()">▶️ Play</button>
                <button class="btn btn-secondary" onclick="nextStep()">Next ⏩</button>
                <button class="btn btn-secondary" onclick="lastStep()">Last ⏭️</button>
                
                <div class="speed-control">
                    <label>Speed:</label>
                    <input type="range" id="speedSlider" min="0.2" max="3" step="0.1" value="1">
                    <span id="speedValue">1.0x</span>
                </div>
            </div>
        </div>

        <div class="visualization" id="visualization">
            <div class="array-container" id="arrayContainer"></div>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #4CAF50;"></div>
                    <span>Sorted</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #FF9800;"></div>
                    <span>Current</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #F44336;"></div>
                    <span>Comparing</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #E3F2FD;"></div>
                    <span>Unsorted</span>
                </div>
            </div>
        </div>

        <div class="info-section">
            <div class="info-box">
                <h3>Step Information</h3>
                <p id="stepDescription">Initial unsorted array</p>
            </div>
            <div class="info-box">
                <h3>Statistics</h3>
                <div class="stats" id="stats">
                    <div>Comparisons: <strong>0</strong></div>
                    <div>Movements: <strong>0</strong></div>
                    <div>Current Step: <strong>1/1</strong></div>
                </div>
            </div>
        </div>

        <div class="progress-section">
            <span><strong>Progress:</strong></span>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%">0%</div>
            </div>
            <span id="progressText">1/1</span>
        </div>
    </div>

    <script>
        let originalArray = [64, 34, 25, 12, 22, 11, 90, 88];
        let steps = [];
        let currentStep = 0;
        let autoPlay = false;
        let speed = 1.0;
        let autoPlayInterval = null;

        function generateSteps() {
            steps = [];
            const arr = [...originalArray];
            const n = arr.length;
            let comparisons = 0;
            let movements = 0;

            steps.push({
                array: [...arr],
                description: "Initial unsorted array",
                currentElement: -1,
                sortedPart: 0,
                comparingWith: -1,
                action: 'start',
                comparisons: 0,
                movements: 0
            });

            for (let i = 1; i < n; i++) {
                const key = arr[i];
                let j = i - 1;

                steps.push({
                    array: [...arr],
                    description: `Step ${i}: Select element ${key} at index ${i} to insert into sorted portion`,
                    currentElement: i,
                    sortedPart: i,
                    comparingWith: -1,
                    action: 'select',
                    comparisons,
                    movements
                });

                while (j >= 0) {
                    comparisons++;

                    steps.push({
                        array: [...arr],
                        description: `Compare ${key} with ${arr[j]} at index ${j}`,
                        currentElement: i,
                        sortedPart: i,
                        comparingWith: j,
                        action: 'compare',
                        comparisons,
                        movements
                    });

                    if (arr[j] > key) {
                        steps.push({
                            array: [...arr],
                            description: `${arr[j]} > ${key}, so shift ${arr[j]} one position right`,
                            currentElement: i,
                            sortedPart: i,
                            comparingWith: j,
                            action: 'shift',
                            comparisons,
                            movements
                        });

                        arr[j + 1] = arr[j];
                        movements++;

                        steps.push({
                            array: [...arr],
                            description: `Array after shifting: [${arr.join(', ')}]`,
                            currentElement: i,
                            sortedPart: i,
                            comparingWith: j,
                            action: 'shifted',
                            comparisons,
                            movements
                        });

                        j--;
                    } else {
                        steps.push({
                            array: [...arr],
                            description: `${arr[j]} ≤ ${key}, found correct position at index ${j + 1}`,
                            currentElement: i,
                            sortedPart: i,
                            comparingWith: j,
                            action: 'found_position',
                            comparisons,
                            movements
                        });
                        break;
                    }
                }

                arr[j + 1] = key;
                movements++;

                steps.push({
                    array: [...arr],
                    description: `Insert ${key} at position ${j + 1}. Sorted portion now: [${arr.slice(0, i + 1).join(', ')}]`,
                    currentElement: j + 1,
                    sortedPart: i + 1,
                    comparingWith: -1,
                    action: 'insert',
                    comparisons,
                    movements
                });
            }

            steps.push({
                array: [...arr],
                description: `Sorting complete! Final sorted array: [${arr.join(', ')}]`,
                currentElement: -1,
                sortedPart: arr.length,
                comparingWith: -1,
                action: 'complete',
                comparisons,
                movements
            });
        }

        function displayCurrentStep() {
            if (steps.length === 0) return;

            const step = steps[currentStep];
            const container = document.getElementById('arrayContainer');
            container.innerHTML = '';

            step.array.forEach((value, index) => {
                const element = document.createElement('div');
                element.className = 'array-element';

                if (step.action === 'complete' || index < step.sortedPart) {
                    element.classList.add('sorted');
                } else if (index === step.currentElement) {
                    element.classList.add('current');
                } else if (index === step.comparingWith) {
                    element.classList.add('comparing');
                }

                element.innerHTML = `
                    <div class="element-value">${value}</div>
                    <div class="element-index">index: ${index}</div>
                `;

                container.appendChild(element);
            });

            document.getElementById('stepDescription').textContent = step.description;
            
            document.getElementById('stats').innerHTML = `
                <div>Comparisons: <strong>${step.comparisons}</strong></div>
                <div>Movements: <strong>${step.movements}</strong></div>
                <div>Current Step: <strong>${currentStep + 1}/${steps.length}</strong></div>
            `;

            const progress = steps.length > 1 ? (currentStep / (steps.length - 1)) * 100 : 0;
            const progressFill = document.getElementById('progressFill');
            progressFill.style.width = progress + '%';
            progressFill.textContent = Math.round(progress) + '%';
            document.getElementById('progressText').textContent = `${currentStep + 1}/${steps.length}`;
        }

        function setCustomArray() {
            const input = document.getElementById('arrayInput').value.trim();
            if (!input) {
                alert('Please enter array elements separated by spaces.');
                return;
            }

            try {
                let newArray = input.split(/\s+/).map(x => parseInt(x));
                if (newArray.some(isNaN)) {
                    alert('Invalid input! Please enter integers separated by spaces.');
                    return;
                }

                if (newArray.length > 20) {
                    alert('Array too large! Using first 20 elements.');
                    newArray = newArray.slice(0, 20);
                } else if (newArray.length < 2) {
                    alert('Array too small! Need at least 2 elements.');
                    return;
                }

                originalArray = newArray;
                resetVisualization();
            } catch (e) {
                alert('Error processing input!');
            }
        }

        function generateRandomArray() {
            const size = Math.floor(Math.random() * 8) + 5;
            originalArray = Array.from({length: size}, () => Math.floor(Math.random() * 99) + 1);
            document.getElementById('arrayInput').value = originalArray.join(' ');
            resetVisualization();
        }

        function resetVisualization() {
            currentStep = 0;
            autoPlay = false;
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
            }
            document.getElementById('playBtn').textContent = '▶️ Play';
            generateSteps();
            displayCurrentStep();
        }

        function firstStep() {
            currentStep = 0;
            displayCurrentStep();
        }

        function previousStep() {
            if (currentStep > 0) {
                currentStep--;
                displayCurrentStep();
            }
        }

        function nextStep() {
            if (currentStep < steps.length - 1) {
                currentStep++;
                displayCurrentStep();
                return true;
            }
            return false;
        }

        function lastStep() {
            currentStep = steps.length - 1;
            displayCurrentStep();
        }

        function toggleAutoPlay() {
            autoPlay = !autoPlay;
            const playBtn = document.getElementById('playBtn');

            if (autoPlay) {
                playBtn.textContent = '⏸️ Pause';
                startAutoPlay();
            } else {
                playBtn.textContent = '▶️ Play';
                if (autoPlayInterval) {
                    clearInterval(autoPlayInterval);
                    autoPlayInterval = null;
                }
            }
        }

        function startAutoPlay() {
            autoPlayInterval = setInterval(() => {
                if (!nextStep()) {
                    autoPlay = false;
                    document.getElementById('playBtn').textContent = '▶️ Play';
                    clearInterval(autoPlayInterval);
                    autoPlayInterval = null;
                }
            }, 1000 / speed);
        }

        document.getElementById('speedSlider').addEventListener('input', function() {
            speed = parseFloat(this.value);
            document.getElementById('speedValue').textContent = speed.toFixed(1) + 'x';
            
            if (autoPlay && autoPlayInterval) {
                clearInterval(autoPlayInterval);
                startAutoPlay();
            }
        });

        // Initialize
        generateSteps();
        displayCurrentStep();
    </script>
</body>
</html>
