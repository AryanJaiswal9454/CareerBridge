from careerbridge import ai

INTERVIEW_QUESTION_BANK = {

    "python": [
        "What are the main differences between a list, tuple and set in Python?",
        "Explain the difference between == and is in Python.",
        "What is a Python dictionary and how does it store data?",
        "What are functions in Python and why are they useful?",
        "Explain exception handling in Python."
    ],

    "sql": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "What is the difference between WHERE and HAVING?",
        "What is normalization in a relational database?",
        "What is a primary key and how is it different from a foreign key?",
        "How would you find duplicate records in a SQL table?"
    ],

    "excel": [
        "What is a Pivot Table and when would you use one?",
        "What is the difference between VLOOKUP and XLOOKUP?",
        "How would you clean duplicate data in Excel?",
        "What are conditional formatting rules used for?",
        "How would you create a dashboard in Excel?"
    ],

    "power bi": [
        "What is Power BI and what problems does it solve?",
        "What is Power Query used for?",
        "What is DAX?",
        "What is the difference between a calculated column and a measure?",
        "How would you design a Power BI dashboard for sales data?"
    ],

    "tableau": [
        "What is Tableau used for?",
        "What is the difference between a worksheet and a dashboard in Tableau?",
        "How do filters work in Tableau?",
        "What are calculated fields?",
        "How would you create an interactive Tableau dashboard?"
    ],

    "statistics": [
        "What is the difference between mean, median and mode?",
        "What is standard deviation?",
        "What is correlation?",
        "What is the difference between correlation and causation?",
        "What is hypothesis testing?"
    ],

    "django": [
        "What is Django and why is it used?",
        "Explain Django's MVT architecture.",
        "What is a Django model?",
        "What is Django REST Framework?",
        "How would you implement authentication in a Django REST API?"
    ],

    "javascript": [
        "What is the difference between let, const and var?",
        "What is a JavaScript closure?",
        "What is the difference between == and ===?",
        "What are promises in JavaScript?",
        "What is asynchronous JavaScript?"
    ],

    "react": [
        "What is React?",
        "What are React components?",
        "What is the difference between props and state?",
        "What are React hooks?",
        "How would you fetch data from a REST API in React?"
    ],
}


BEHAVIORAL_QUESTIONS = [
    "Tell me about yourself.",
    "Why are you interested in this role?",
    "Why should we hire you?",
    "Tell me about a challenging project you worked on.",
    "Tell me about a time you had to learn something quickly.",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in the next three years?",
]


# ---------------------------------------------------------
# MCQ question bank: skill -> list of {question, options, correct_option, explanation}
# ---------------------------------------------------------

MCQ_BANK = {
    "python": [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["func", "def", "function", "lambda"],
            "correct_option": "B",
            "explanation": "def is the keyword used to define a named function in Python.",
            "difficulty": "easy",
        },
        {
            "question": "Which data type in Python is immutable?",
            "options": ["List", "Dictionary", "Tuple", "Set"],
            "correct_option": "C",
            "explanation": "Tuples cannot be changed after creation, unlike lists, dictionaries and sets.",
            "difficulty": "medium",
        },
        {
            "question": "What does the 'len()' function return for a dictionary?",
            "options": ["Number of keys", "Sum of values", "Number of characters", "Nothing, it errors"],
            "correct_option": "A",
            "explanation": "len() on a dict returns the number of key-value pairs (i.e. number of keys).",
            "difficulty": "medium",
        },
        {
            "question": "What's the key difference between a Python generator and a list when iterating over large data?",
            "options": [
                "There's no real difference",
                "A generator produces items lazily, one at a time, using far less memory than building a full list",
                "Generators can only be used once ever, in any context",
                "Lists are always faster to iterate",
            ],
            "correct_option": "B",
            "explanation": "Generators yield values on demand instead of building the whole sequence in memory upfront — critical for large or infinite sequences.",
            "difficulty": "hard",
        },
    ],
    "sql": [
        {
            "question": "Which SQL keyword retrieves data from a table?",
            "options": ["GET", "SELECT", "FETCH", "PULL"],
            "correct_option": "B",
            "explanation": "SELECT is the standard SQL keyword for querying/retrieving data from a table.",
            "difficulty": "easy",
        },
        {
            "question": "Which SQL clause is used to filter groups after a GROUP BY?",
            "options": ["WHERE", "HAVING", "FILTER", "ORDER BY"],
            "correct_option": "B",
            "explanation": "HAVING filters aggregated groups, while WHERE filters rows before grouping.",
            "difficulty": "medium",
        },
        {
            "question": "Which JOIN returns all rows from the left table, and matched rows from the right?",
            "options": ["INNER JOIN", "RIGHT JOIN", "LEFT JOIN", "CROSS JOIN"],
            "correct_option": "C",
            "explanation": "LEFT JOIN keeps every row from the left table, with NULLs where there's no match on the right.",
            "difficulty": "medium",
        },
    ],
    "excel": [
        {
            "question": "Which Excel feature summarizes large datasets interactively without formulas?",
            "options": ["Conditional formatting", "Pivot Table", "Data validation", "Freeze panes"],
            "correct_option": "B",
            "explanation": "Pivot Tables let you summarize, group and rearrange data interactively.",
            "difficulty": "medium",
        },
        {
            "question": "Which lookup function can search to the left of the lookup column (unlike classic VLOOKUP)?",
            "options": ["VLOOKUP", "HLOOKUP", "XLOOKUP", "SUMIF"],
            "correct_option": "C",
            "explanation": "XLOOKUP (and INDEX/MATCH) can look in any direction, unlike VLOOKUP which only looks right.",
            "difficulty": "medium",
        },
    ],
    "power bi": [
        {
            "question": "What language is used to write custom calculations (measures) in Power BI?",
            "options": ["DAX", "SQL", "Python", "M code only"],
            "correct_option": "A",
            "explanation": "DAX (Data Analysis Expressions) is the formula language used for measures and calculated columns.",
            "difficulty": "medium",
        },
    ],
    "statistics": [
        {
            "question": "Which measure of central tendency is most affected by extreme outliers?",
            "options": ["Median", "Mode", "Mean", "Range"],
            "correct_option": "C",
            "explanation": "The mean is pulled toward outliers, while the median and mode are more resistant to them.",
            "difficulty": "medium",
        },
    ],
    "javascript": [
        {
            "question": "Which keyword declares a block-scoped variable that cannot be reassigned?",
            "options": ["var", "let", "const", "static"],
            "correct_option": "C",
            "explanation": "const creates a block-scoped binding that cannot be reassigned after declaration.",
            "difficulty": "medium",
        },
    ],
    "react": [
        {
            "question": "Which hook lets a function component hold local state?",
            "options": ["useEffect", "useState", "useMemo", "useRef"],
            "correct_option": "B",
            "explanation": "useState returns a state value and a setter function for updating it.",
            "difficulty": "medium",
        },
    ],
    "django": [
        {
            "question": "In Django REST Framework, what converts model instances to and from JSON?",
            "options": ["Middleware", "Serializer", "Migration", "Template"],
            "correct_option": "B",
            "explanation": "Serializers handle converting complex data (like model instances) to and from JSON.",
            "difficulty": "medium",
        },
    ],
    "html": [
        {
            "question": "Which HTML tag is used to create a hyperlink?",
            "options": ["<link>", "<a>", "<href>", "<nav>"],
            "correct_option": "B",
            "explanation": "The <a> (anchor) tag with an href attribute creates a hyperlink.",
            "difficulty": "easy",
        },
        {
            "question": "Which HTML5 element is used to define independent, self-contained content, like a blog post?",
            "options": ["<section>", "<div>", "<article>", "<aside>"],
            "correct_option": "C",
            "explanation": "<article> represents content that could stand alone and be redistributed independently, like a blog post or news item.",
            "difficulty": "medium",
        },
        {
            "question": "What's the accessibility purpose of the `alt` attribute on an `<img>` tag?",
            "options": [
                "It sets the image's file size",
                "It provides alternative text for screen readers and when the image fails to load",
                "It changes the image's alignment",
                "It has no real purpose today",
            ],
            "correct_option": "B",
            "explanation": "Screen readers announce the alt text, and browsers display it if the image can't load — both matter for accessibility and robustness.",
            "difficulty": "hard",
        },
    ],
    "css": [
        {
            "question": "Which CSS property controls the space between an element's border and its content?",
            "options": ["margin", "padding", "spacing", "gap"],
            "correct_option": "B",
            "explanation": "Padding is the space inside the border, between the border and the content; margin is the space outside the border.",
            "difficulty": "easy",
        },
        {
            "question": "In Flexbox, which property aligns items along the cross axis?",
            "options": ["justify-content", "align-items", "flex-direction", "order"],
            "correct_option": "B",
            "explanation": "align-items controls alignment on the cross axis; justify-content controls the main axis.",
            "difficulty": "medium",
        },
        {
            "question": "Why can `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))` be preferable to a fixed number of columns for a responsive layout?",
            "options": [
                "It's shorter to type, nothing more",
                "It automatically adjusts the column count to fit the available width",
                "It disables responsiveness entirely",
                "It only works in older browsers",
            ],
            "correct_option": "B",
            "explanation": "auto-fit with minmax lets the grid recalculate how many columns fit the container width, giving responsive behavior without media queries.",
            "difficulty": "hard",
        },
    ],
    "git": [
        {
            "question": "Which command creates a new branch and switches to it in one step?",
            "options": ["git branch new-branch", "git checkout -b new-branch", "git merge new-branch", "git clone new-branch"],
            "correct_option": "B",
            "explanation": "git checkout -b creates the branch and switches to it in a single command (git switch -c is the newer equivalent).",
            "difficulty": "easy",
        },
        {
            "question": "What does `git rebase` do differently from `git merge`?",
            "options": [
                "It deletes the branch history entirely",
                "It replays your commits on top of another branch, creating a linear history",
                "It only works on the main branch",
                "It's identical to merge in every way",
            ],
            "correct_option": "B",
            "explanation": "Rebase moves/replays commits onto a new base, producing a linear history, instead of merge's history-preserving merge commit.",
            "difficulty": "medium",
        },
        {
            "question": "You accidentally committed a secret key. It's already pushed. What's the most correct next step?",
            "options": [
                "Just delete the file in a new commit",
                "Rotate/invalidate the leaked secret, then rewrite history if needed to remove it",
                "Nothing — git history can't be changed anyway",
                "Rename the repository",
            ],
            "correct_option": "B",
            "explanation": "Deleting the file in a new commit leaves the secret in history — the secret must be treated as compromised and rotated regardless of history cleanup.",
            "difficulty": "hard",
        },
    ],
    "streamlit": [
        {
            "question": "Which Streamlit function displays text, numbers, dataframes or charts with minimal formatting decisions?",
            "options": ["st.write()", "st.print()", "st.display()", "st.render()"],
            "correct_option": "A",
            "explanation": "st.write() is Streamlit's general-purpose display function that auto-detects how to render many different data types.",
            "difficulty": "easy",
        },
        {
            "question": "How does Streamlit's default execution model work when a user interacts with a widget?",
            "options": [
                "Only the changed component updates",
                "The entire script re-runs top to bottom on every interaction",
                "Nothing happens until the page is refreshed",
                "It requires a separate backend API call you must write yourself",
            ],
            "correct_option": "B",
            "explanation": "Streamlit re-runs the whole script from top to bottom on each interaction by default, which is why caching (st.cache_data) matters for performance.",
            "difficulty": "medium",
        },
        {
            "question": "Why would you use `st.session_state` in a Streamlit app?",
            "options": [
                "To style the page with CSS",
                "To persist values across reruns, since local variables reset every rerun",
                "It's required to import any library",
                "To connect to a database",
            ],
            "correct_option": "B",
            "explanation": "Because the whole script reruns on each interaction, session_state is how you keep values (like a counter or form input) alive between reruns.",
            "difficulty": "hard",
        },
    ],
    "python libraries": [
        {
            "question": "In pandas, which method would you use to view the first 5 rows of a DataFrame?",
            "options": ["df.top()", "df.head()", "df.first()", "df.show()"],
            "correct_option": "B",
            "explanation": "df.head() returns the first 5 rows by default (or a custom number if you pass one).",
            "difficulty": "easy",
        },
        {
            "question": "What's the key difference between NumPy arrays and Python lists for numerical work?",
            "options": [
                "There's no real difference",
                "NumPy arrays support fast, vectorized operations and use less memory for numeric data",
                "Python lists are always faster",
                "NumPy arrays can't hold numbers",
            ],
            "correct_option": "B",
            "explanation": "NumPy arrays are stored contiguously and support vectorized (C-level) operations, making them far faster than looping over Python lists for numeric work.",
            "difficulty": "medium",
        },
        {
            "question": "In pandas, what's the difference between `df.loc[]` and `df.iloc[]`?",
            "options": [
                "They're interchangeable in every case",
                "loc selects by label, iloc selects by integer position",
                "loc is for columns only, iloc is for rows only",
                "iloc is deprecated and shouldn't be used",
            ],
            "correct_option": "B",
            "explanation": "loc uses row/column labels (like index names), while iloc uses purely integer positions — they can behave very differently on a non-default index.",
            "difficulty": "hard",
        },
    ],
}


# ---------------------------------------------------------
# Coding question bank: skill -> {question, starter_code, sample_solution, explanation}
# ---------------------------------------------------------

CODING_BANK = {
    "python": {
        "question": "Write a function `count_vowels(text)` that returns the number of vowels (a, e, i, o, u) in a string, case-insensitive.",
        "starter_code": "def count_vowels(text):\n    # your code here\n    pass",
        "sample_solution": "def count_vowels(text):\n    return sum(1 for ch in text.lower() if ch in 'aeiou')",
        "explanation": "Iterate over the lowercased string and count characters that are in the vowel set.",
            "difficulty": "medium",
        "language": "python",
    },
    "sql": {
        "question": "Write a SQL query to find the second highest salary from an `employees` table with columns (id, name, salary).",
        "starter_code": "SELECT ... FROM employees ...",
        "sample_solution": "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);",
        "explanation": "Exclude the highest salary first, then take the max of what remains to get the second highest.",
            "difficulty": "medium",
        "language": "sql",
    },
    "javascript": {
        "question": "Write a function `reverseString(str)` that returns the reverse of a string without using the built-in reverse() array method directly on a for loop is fine.",
        "starter_code": "function reverseString(str) {\n  // your code here\n}",
        "sample_solution": "function reverseString(str) {\n  return str.split('').reverse().join('');\n}",
        "explanation": "Split the string into characters, reverse the array, then join it back into a string.",
            "difficulty": "medium",
        "language": "javascript",
    },
    "react": {
        "question": "Write a small React component `Counter` that renders a number and a button which increments it by 1 when clicked.",
        "starter_code": "function Counter() {\n  // your code here\n}",
        "sample_solution": "function Counter() {\n  const [count, setCount] = useState(0);\n  return <button onClick={() => setCount(count + 1)}>{count}</button>;\n}",
        "explanation": "useState holds the current count; the onClick handler updates it, triggering a re-render.",
            "difficulty": "medium",
        "language": "javascript",
    },
    "django": {
        "question": "Write a Django REST Framework view (function or class based) that returns a JSON list of all `Book` model titles.",
        "starter_code": "class BookTitlesView(APIView):\n    def get(self, request):\n        # your code here\n        pass",
        "sample_solution": "class BookTitlesView(APIView):\n    def get(self, request):\n        titles = list(Book.objects.values_list('title', flat=True))\n        return Response(titles)",
        "explanation": "values_list('title', flat=True) pulls just the title column efficiently, then it's wrapped in a Response.",
            "difficulty": "medium",
        "language": "python",
    },
    "excel": {
        "question": "Describe (in formula form) how you would use XLOOKUP to find a customer's email in a table given their ID in cell A2, where the ID column is D:D and email column is F:F.",
        "starter_code": "=XLOOKUP(...)",
        "sample_solution": "=XLOOKUP(A2, D:D, F:F, \"Not found\")",
        "explanation": "XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found]) searches D:D for A2 and returns the matching value from F:F.",
            "difficulty": "medium",
        "language": "excel",
    },
    "html": {
        "question": "Write a simple HTML form with a text input for 'name' and a submit button.",
        "starter_code": "<form>\n  <!-- your code here -->\n</form>",
        "sample_solution": "<form>\n  <label for=\"name\">Name</label>\n  <input id=\"name\" name=\"name\" type=\"text\">\n  <button type=\"submit\">Submit</button>\n</form>",
        "explanation": "A labeled input tied to the field via for/id, plus a submit button, is both functional and accessible.",
        "difficulty": "easy",
        "language": "html",
    },
    "css": {
        "question": "Write CSS to center a div both horizontally and vertically inside its parent using Flexbox.",
        "starter_code": ".parent {\n  /* your code here */\n}",
        "sample_solution": ".parent {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}",
        "explanation": "justify-content centers on the main axis and align-items centers on the cross axis — together they center in both directions.",
        "difficulty": "easy",
        "language": "css",
    },
    "git": {
        "question": "You're on a feature branch and want to update it with the latest changes from main without creating a merge commit. What commands would you run?",
        "starter_code": "# git checkout your-branch\n# ...",
        "sample_solution": "git checkout your-branch\ngit fetch origin\ngit rebase origin/main",
        "explanation": "Rebasing your branch onto the latest main replays your commits on top of it, keeping history linear instead of adding a merge commit.",
        "difficulty": "medium",
        "language": "bash",
    },
    "streamlit": {
        "question": "Write a minimal Streamlit app that shows a slider from 0 to 100 and displays the selected value squared.",
        "starter_code": "import streamlit as st\n\n# your code here",
        "sample_solution": "import streamlit as st\n\nvalue = st.slider('Pick a number', 0, 100)\nst.write(f'Squared: {value ** 2}')",
        "explanation": "st.slider returns the current value directly; since Streamlit reruns the script on each interaction, using that value immediately is enough.",
        "difficulty": "medium",
        "language": "python",
    },
    "python libraries": {
        "question": "Given a pandas DataFrame `df` with a 'sales' column, write code to add a new column 'sales_category' that is 'high' if sales > 1000, else 'low'.",
        "starter_code": "import pandas as pd\n\n# df is already defined\n# your code here",
        "sample_solution": "df['sales_category'] = df['sales'].apply(lambda x: 'high' if x > 1000 else 'low')",
        "explanation": "apply() with a lambda runs the condition row-by-row; for large data, a vectorized np.where(df['sales'] > 1000, 'high', 'low') would be faster.",
        "difficulty": "medium",
        "language": "python",
    },
}


GENERIC_MCQ_FALLBACK_POOL = [
    {
        "question": "Which of the following is generally considered a best practice when learning a new technical skill for a job?",
        "options": [
            "Only reading theory, never practicing",
            "Building small practical projects and reviewing mistakes",
            "Avoiding documentation",
            "Memorizing answers without understanding them",
        ],
        "correct_option": "B",
        "explanation": "Hands-on practice with real feedback builds deeper, more durable understanding than passive reading alone.",
    },
    {
        "question": "When you're stuck debugging an unfamiliar error, what's usually the most effective first step?",
        "options": [
            "Rewrite the whole program from scratch",
            "Read the error message carefully and isolate where it happens",
            "Ignore it and hope it resolves itself",
            "Ask someone else to fix it without looking yourself",
        ],
        "correct_option": "B",
        "explanation": "Most errors point directly at the problem if you actually read them closely and narrow down where execution breaks.",
    },
    {
        "question": "Why do interviewers often ask you to explain your reasoning out loud while solving a problem?",
        "options": [
            "To make the interview take longer",
            "To see your problem-solving process, not just the final answer",
            "It's just a formality with no real purpose",
            "To test how fast you can type",
        ],
        "correct_option": "B",
        "explanation": "Interviewers weigh how you approach a problem — breaking it down, checking assumptions — as much as whether you get the exact right answer.",
    },
    {
        "question": "What's generally the best way to prepare for questions on a topic you're weak in?",
        "options": [
            "Skip it and hope it doesn't come up",
            "Build one small, real project using that topic",
            "Only read the documentation once",
            "Memorize unrelated trivia about it",
        ],
        "correct_option": "B",
        "explanation": "Applying a concept in a small real project cements understanding far better than passive review.",
    },
    {
        "question": "When comparing two approaches to solve the same problem, what usually matters most in an interview setting?",
        "options": [
            "Picking whichever approach uses the fewest characters",
            "Being able to explain the trade-offs between them (time, memory, readability)",
            "Always picking the most complex-sounding option",
            "There's no meaningful difference between approaches",
        ],
        "correct_option": "B",
        "explanation": "Interviewers care more about whether you understand the trade-offs than which single 'correct' approach you pick.",
    },
    {
        "question": "If you don't fully know the answer to a technical question, what's usually the best response?",
        "options": [
            "Stay silent until you're certain",
            "Say what you do know, reason through it out loud, and be honest about the gap",
            "Guess confidently without explaining your reasoning",
            "Change the subject",
        ],
        "correct_option": "B",
        "explanation": "Interviewers value transparent reasoning and honesty about uncertainty far more than a confident wrong guess.",
    },
]

GENERIC_CODING_FALLBACK_POOL = [
    {
        "question": "Describe, step by step, how you would approach solving a problem in this skill area that you haven't seen before.",
        "starter_code": "# Describe your approach in comments, then write any code you can.",
        "sample_solution": "A strong answer breaks the problem into smaller steps, identifies inputs/outputs, considers edge cases, and tests incrementally.",
        "explanation": "Interviewers value structured problem-solving as much as the final answer.",
    },
    {
        "question": "Write out, in pseudocode or comments, how you'd validate and clean a messy real-world dataset or input before using it.",
        "starter_code": "# List the checks you'd run (missing values, wrong types, duplicates) and how you'd handle each.",
        "sample_solution": "Check for nulls/missing values, confirm data types match expectations, remove or flag duplicates, and log what was changed rather than silently dropping data.",
        "explanation": "Real-world data is rarely clean — showing a systematic validation approach matters as much as any single technique.",
    },
    {
        "question": "Explain how you'd test a function you just wrote to make sure it actually works, before considering it done.",
        "starter_code": "# Outline the test cases you'd try, including edge cases.",
        "sample_solution": "Test the typical case, an empty/minimal input, a large input, and an invalid input — and check the function fails predictably rather than silently.",
        "explanation": "Interviewers want to see you think about correctness proactively, not just write code and assume it works.",
    },
    {
        "question": "If your solution works but is slow on large inputs, walk through how you'd figure out where the bottleneck is.",
        "starter_code": "# Describe how you'd profile/narrow down the slow part.",
        "sample_solution": "Time or profile different sections, look for nested loops or repeated work that could be cached, and confirm the fix actually helps by re-measuring, not just guessing.",
        "explanation": "Interviewers want to see a measurement-driven approach to performance, not guesswork.",
    },
]

GENERIC_CONCEPTUAL_FALLBACK_POOL = [
    {
        "question": "Explain, in your own words, a core concept of {topic} you'd expect to use on the job.",
        "model_answer": "A strong answer names a specific {topic} concept, explains what problem it solves, and gives a brief concrete example of using it — rather than a textbook definition alone.",
        "key_points": ["Name a specific concept, not a vague generality", "Explain why/when it's used", "Back it with a concrete example"],
    },
    {
        "question": "What's a mistake beginners commonly make when learning {topic}, and how would you avoid it?",
        "model_answer": "A strong answer names a specific, realistic beginner mistake in {topic}, explains why it happens, and describes a concrete habit or check that prevents it.",
        "key_points": ["A specific, realistic mistake", "Why it happens", "A concrete way to avoid it"],
    },
    {
        "question": "How would you explain {topic} to someone with no technical background?",
        "model_answer": "A strong answer uses a simple, accurate analogy for {topic}, avoids jargon, and connects it to something the listener already understands.",
        "key_points": ["A clear, accurate analogy", "No unexplained jargon", "Ties back to something familiar"],
    },
    {
        "question": "What would you look up or double-check the first time you used {topic} on a real project?",
        "model_answer": "A strong answer names the specific documentation, convention, or gotcha they'd verify for {topic}, showing they know what they don't yet know rather than guessing.",
        "key_points": ["Names something concrete to check, not vague 'the docs'", "Shows awareness of common gotchas", "Reflects real caution, not overconfidence"],
    },
]

_fallback_rotation = {"mcq": 0, "coding": 0, "conceptual": 0}


def _next_fallback(kind, pool):
    index = _fallback_rotation[kind] % len(pool)
    _fallback_rotation[kind] += 1
    return pool[index]


# Free, well-known external practice/mock platforms, by skill — so a user
# can go do a full topic-wise mock test beyond what we generate in-app.
# Links point at each site's topic/practice landing page, never a
# fabricated specific-question URL.
EXTERNAL_PRACTICE_PROVIDERS = {
    "python": [
        {"provider": "HackerRank", "url": "https://www.hackerrank.com/domains/python"},
        {"provider": "LeetCode", "url": "https://leetcode.com/problemset/?topicSlugs=python"},
        {"provider": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/python-programming-language/"},
    ],
    "sql": [
        {"provider": "HackerRank", "url": "https://www.hackerrank.com/domains/sql"},
        {"provider": "LeetCode", "url": "https://leetcode.com/problemset/database/"},
        {"provider": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/"},
    ],
    "javascript": [
        {"provider": "HackerRank", "url": "https://www.hackerrank.com/domains/javascript"},
        {"provider": "LeetCode", "url": "https://leetcode.com/problemset/?topicSlugs=javascript"},
        {"provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"},
    ],
    "react": [
        {"provider": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/reactjs/reactjs-interview-questions/"},
        {"provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/"},
    ],
    "django": [
        {"provider": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/django-interview-questions/"},
        {"provider": "InterviewBit", "url": "https://www.interviewbit.com/django-interview-questions/"},
    ],
    "excel": [
        {"provider": "IndiaBix", "url": "https://www.indiabix.com/aptitude/questions-and-answers/"},
        {"provider": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/basic-excel-interview-questions/"},
    ],
    "power bi": [
        {"provider": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/power-bi-interview-questions/"},
    ],
    "statistics": [
        {"provider": "IndiaBix", "url": "https://www.indiabix.com/aptitude/questions-and-answers/"},
        {"provider": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/statistics-interview-questions/"},
    ],
    "machine learning": [
        {"provider": "HackerRank", "url": "https://www.hackerrank.com/domains/ai"},
        {"provider": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org/machine-learning-interview-questions/"},
    ],
}

GENERIC_PRACTICE_PROVIDERS = [
    {"provider": "GeeksforGeeks Interview Corner", "url": "https://www.geeksforgeeks.org/interview-corner/"},
    {"provider": "InterviewBit", "url": "https://www.interviewbit.com/"},
]


def get_external_practice_links(skills):
    """Curated free mock-test/practice-platform links for a set of skills,
    for taking a full topic-wise mock outside of CareerBridge."""
    seen_urls = set()
    links = []
    for skill in skills:
        normalized = normalize_skill(skill)
        for entry in EXTERNAL_PRACTICE_PROVIDERS.get(normalized, GENERIC_PRACTICE_PROVIDERS):
            if entry["url"] in seen_urls:
                continue
            seen_urls.add(entry["url"])
            links.append({"skill": skill, "provider": entry["provider"], "url": entry["url"]})
    return links[:8]


def normalize_skill(skill):
    return (skill or "").strip().lower()


def _ai_mcq_or_fallback(skill):
    try:
        result = ai.generate_mcq_question(skill)
    except Exception:
        result = None
    if result and result.get("options") and len(result.get("options", [])) >= 2:
        return {
            "question": result["question"],
            "options": result["options"],
            "correct_option": result.get("correct_option", "A"),
            "explanation": result.get("explanation", ""),
        }
    fallback = dict(_next_fallback("mcq", GENERIC_MCQ_FALLBACK_POOL))
    fallback["question"] = f"({skill.title()}) " + fallback["question"]
    return fallback


def _ai_coding_or_fallback(skill):
    try:
        result = ai.generate_coding_question(skill)
    except Exception:
        result = None
    if result and result.get("question"):
        result.setdefault("language", "text")
        return result
    fallback = dict(_next_fallback("coding", GENERIC_CODING_FALLBACK_POOL))
    fallback["question"] = f"({skill.title()}) " + fallback["question"]
    return fallback


def get_mcq_questions_for_skills(skills, limit):
    questions = []
    used_skills = set()
    for skill in skills:
        if len(questions) >= limit:
            break
        normalized = normalize_skill(skill)
        if normalized in used_skills:
            continue
        used_skills.add(normalized)
        bank_items = MCQ_BANK.get(normalized)
        item = bank_items[0] if bank_items else _ai_mcq_or_fallback(skill)
        questions.append({
            "question": item["question"],
            "category": "technical",
            "question_type": "mcq",
            "related_skill": skill,
            "expected_points": [],
            "options": item["options"],
            "correct_option": item["correct_option"],
            "explanation": item["explanation"],
        })
    return questions


def get_coding_questions_for_skills(skills, limit):
    questions = []
    used_skills = set()
    for skill in skills:
        if len(questions) >= limit:
            break
        normalized = normalize_skill(skill)
        if normalized in used_skills:
            continue
        used_skills.add(normalized)
        item = CODING_BANK.get(normalized) or _ai_coding_or_fallback(skill)
        questions.append({
            "question": item["question"],
            "category": "technical",
            "question_type": "coding",
            "related_skill": skill,
            "expected_points": [],
            "starter_code": item.get("starter_code", ""),
            "language": item.get("language", "text"),
            "sample_solution": item.get("sample_solution", ""),
            "explanation": item.get("explanation", ""),
        })
    return questions


def get_open_questions_for_skills(skills, limit):
    questions = []
    for skill in skills:
        if len(questions) >= limit:
            break
        normalized = normalize_skill(skill)
        bank_questions = INTERVIEW_QUESTION_BANK.get(normalized, [])
        for question in bank_questions:
            questions.append({
                "question": question,
                "category": "technical",
                "question_type": "open",
                "related_skill": skill,
                "expected_points": [],
            })
            if len(questions) >= limit:
                break
    return questions


def get_behavioral_questions(limit):
    return [{
        "question": question,
        "category": "behavioral",
        "question_type": "open",
        "related_skill": None,
        "expected_points": [],
    } for question in BEHAVIORAL_QUESTIONS[:limit]]


def get_priority_skills(match_result):
    """Skills to prioritize for interview prep, worst gaps first."""
    return (
        match_result.skills_to_improve
        + match_result.missing_skills
        + match_result.matched_skills
    ) or ["python"]


def generate_interview_questions(match_result, session_type="mixed", limit=5):
    priority_skills = get_priority_skills(match_result)

    questions = []

    if session_type == "mcq":
        # Pure MCQ round across the priority skills.
        questions.extend(get_mcq_questions_for_skills(priority_skills, limit))

    elif session_type == "technical":
        # Explicit ask: technical round should contain both MCQs and coding questions.
        coding_count = max(1, limit // 2)
        mcq_count = limit - coding_count
        questions.extend(get_coding_questions_for_skills(priority_skills, coding_count))
        questions.extend(get_mcq_questions_for_skills(priority_skills, mcq_count))

    elif session_type == "behavioral":
        questions.extend(get_behavioral_questions(limit))

    else:  # mixed
        coding_count = max(1, limit // 3)
        mcq_count = max(1, limit // 3)
        behavioral_count = limit - coding_count - mcq_count
        questions.extend(get_coding_questions_for_skills(priority_skills, coding_count))
        questions.extend(get_mcq_questions_for_skills(priority_skills, mcq_count))
        questions.extend(get_behavioral_questions(behavioral_count))

    return questions[:limit]


# ===========================================================
# Question Bank: a category+difficulty browsable practice set,
# separate from the job-match-driven mock interview above.
# Hybrid approach: curated items for reliability and zero API
# cost, topped up with AI-generated ones for variety and to
# reach the requested count, and to cover difficulty levels the
# curated bank doesn't distinguish (it's tagged "medium" by
# default — "easy"/"hard" requests lean more on AI generation).
# ===========================================================

# ===========================================================
# Role -> Skill -> Topic Question Bank
# ===========================================================

ROLE_CATALOG = [
    {
        "id": "software-developer",
        "name": "Software Developer",
        "category": "Software Development",
        "skills": {
            "Programming Fundamentals": ["OOP", "Data Structures", "Algorithms", "Exception Handling"],
            "Python": ["Functions and Modules", "OOP in Python", "Collections", "Exceptions and Files"],
            "Java": ["OOP", "Collections", "Exception Handling", "Streams"],
            "JavaScript": ["ES6+", "Async JavaScript", "DOM", "Error Handling"],
            "Git": ["Branching", "Merge and Rebase", "Conflict Resolution", "Git Workflows"],
            "Problem Solving": ["Complexity", "Pattern Recognition", "Debugging", "Edge Cases"],
        },
    },
    {
        "id": "python-developer",
        "name": "Python Developer",
        "category": "Software Development",
        "skills": {
            "Python": ["Functions and Modules", "OOP", "Decorators", "Generators", "File Handling", "Testing"],
            "Django": ["Models and ORM", "Views and URLs", "DRF", "Authentication", "Middleware"],
            "FastAPI": ["Routes", "Pydantic", "Dependency Injection", "Async APIs"],
            "SQL": ["Joins", "Aggregation", "Subqueries", "Indexes"],
            "Git": ["Branching", "Pull Requests", "Rebase", "Release Workflow"],
        },
    },
    {
        "id": "java-developer",
        "name": "Java Developer",
        "category": "Software Development",
        "skills": {
            "Java": ["OOP", "Collections", "Streams", "Concurrency", "Exception Handling"],
            "Spring Boot": ["REST APIs", "Dependency Injection", "JPA", "Security"],
            "SQL": ["Joins", "Transactions", "Indexes", "Query Optimization"],
            "DSA": ["Arrays", "Trees", "Graphs", "Complexity"],
            "Testing": ["JUnit", "Mocking", "Integration Tests", "Test Design"],
        },
    },
    {
        "id": "full-stack-developer",
        "name": "Full Stack Developer",
        "category": "Software Development",
        "skills": {
            "HTML/CSS": ["Semantic HTML", "Flexbox", "Grid", "Responsive Design"],
            "JavaScript": ["ES6+", "Promises", "Async/Await", "DOM"],
            "React": ["Components", "State and Props", "Hooks", "API Integration"],
            "Backend APIs": ["REST", "Authentication", "Validation", "Error Handling"],
            "SQL": ["Joins", "Indexes", "Transactions", "Schema Design"],
            "Git": ["Branching", "Code Review", "Merge Conflicts", "CI Workflow"],
        },
    },
    {
        "id": "frontend-developer",
        "name": "Frontend Developer",
        "category": "Software Development",
        "skills": {
            "HTML/CSS": ["Semantic HTML", "Flexbox", "Grid", "Accessibility"],
            "JavaScript": ["Closures", "Async JavaScript", "DOM", "ES Modules"],
            "React": ["Hooks", "State Management", "Rendering", "Performance"],
            "TypeScript": ["Types", "Generics", "Interfaces", "Narrowing"],
            "Web Performance": ["Lazy Loading", "Caching", "Core Web Vitals", "Bundle Optimization"],
        },
    },
    {
        "id": "backend-developer",
        "name": "Backend Developer",
        "category": "Software Development",
        "skills": {
            "REST APIs": ["HTTP Methods", "Status Codes", "Validation", "Pagination"],
            "Python": ["OOP", "Error Handling", "Testing", "Concurrency"],
            "SQL": ["Joins", "Transactions", "Indexes", "Optimization"],
            "Authentication": ["JWT", "Sessions", "Authorization", "Password Security"],
            "System Design": ["Caching", "Queues", "Scalability", "Reliability"],
        },
    },
    {
        "id": "django-developer",
        "name": "Django Developer",
        "category": "Software Development",
        "skills": {
            "Django": ["Models and ORM", "Views and URLs", "Templates", "Middleware", "Signals"],
            "Django REST Framework": ["Serializers", "APIView", "Permissions", "Authentication"],
            "Python": ["OOP", "Decorators", "Exceptions", "Testing"],
            "SQL": ["Joins", "Indexes", "Transactions", "Query Optimization"],
            "Deployment": ["Gunicorn", "Static Files", "Environment Variables", "Production Settings"],
        },
    },
    {
        "id": "react-developer",
        "name": "React Developer",
        "category": "Software Development",
        "skills": {
            "React": ["Components", "Props and State", "Hooks", "Context", "Performance"],
            "JavaScript": ["Closures", "Promises", "Async/Await", "Modules"],
            "TypeScript": ["Types", "Generics", "React Types", "Utility Types"],
            "API Integration": ["Axios", "REST", "Loading States", "Error Handling"],
            "Testing": ["Component Testing", "Mocks", "User Interaction", "Test Strategy"],
        },
    },
    {
        "id": "mobile-developer",
        "name": "Mobile App Developer",
        "category": "Software Development",
        "skills": {
            "Mobile Architecture": ["Navigation", "State", "Offline Data", "App Lifecycle"],
            "APIs": ["REST", "Authentication", "Caching", "Error Handling"],
            "Performance": ["Memory", "Rendering", "Network Optimization", "Battery"],
            "Testing": ["Unit Tests", "UI Tests", "Mocks", "Release Testing"],
        },
    },
    {
        "id": "data-analyst",
        "name": "Data Analyst",
        "category": "Data & Analytics",
        "skills": {
            "SQL": ["Joins", "Aggregation", "Subqueries", "Window Functions", "CTEs", "Query Optimization"],
            "Python": ["Pandas", "NumPy", "Data Cleaning", "Visualization"],
            "Excel": ["Lookup Functions", "Pivot Tables", "Data Cleaning", "Dashboards"],
            "Statistics": ["Descriptive Statistics", "Probability", "Hypothesis Testing", "Correlation"],
            "Power BI": ["Power Query", "DAX", "Data Modeling", "Dashboard Design"],
            "Data Visualization": ["Chart Selection", "Storytelling", "KPIs", "Dashboard UX"],
        },
    },
    {
        "id": "business-analyst",
        "name": "Business Analyst",
        "category": "Data & Analytics",
        "skills": {
            "Requirements Analysis": ["Elicitation", "User Stories", "Acceptance Criteria", "Prioritization"],
            "SQL": ["Joins", "Aggregation", "Data Validation", "Business Queries"],
            "Excel": ["Pivot Tables", "Lookups", "Scenario Analysis", "Dashboards"],
            "Data Visualization": ["KPIs", "Storytelling", "Charts", "Stakeholder Reporting"],
            "Problem Solving": ["Root Cause Analysis", "Trade-offs", "Process Analysis", "Decision Making"],
        },
    },
    {
        "id": "bi-analyst",
        "name": "BI Analyst",
        "category": "Data & Analytics",
        "skills": {
            "Power BI": ["DAX", "Power Query", "Data Modeling", "Dashboard Design"],
            "SQL": ["Joins", "CTEs", "Window Functions", "Optimization"],
            "Data Warehousing": ["Star Schema", "Fact Tables", "Dimensions", "ETL"],
            "Excel": ["Pivot Tables", "Power Pivot", "Lookups", "Data Cleaning"],
        },
    },
    {
        "id": "data-scientist",
        "name": "Data Scientist",
        "category": "Data & AI",
        "skills": {
            "Python": ["Pandas", "NumPy", "Visualization", "Data Pipelines"],
            "Statistics": ["Probability", "Hypothesis Testing", "Regression", "Experiment Design"],
            "Machine Learning": ["Classification", "Regression", "Feature Engineering", "Model Evaluation"],
            "SQL": ["Joins", "Window Functions", "CTEs", "Data Extraction"],
            "Model Deployment": ["APIs", "Serialization", "Monitoring", "Drift"],
        },
    },
    {
        "id": "data-engineer",
        "name": "Data Engineer",
        "category": "Data & AI",
        "skills": {
            "SQL": ["Query Optimization", "Window Functions", "CTEs", "Transactions"],
            "Python": ["Data Processing", "ETL", "Testing", "Automation"],
            "ETL": ["Pipelines", "Validation", "Incremental Loads", "Orchestration"],
            "Data Warehousing": ["Star Schema", "Partitioning", "Fact Tables", "Dimensions"],
            "Cloud Data": ["Object Storage", "Data Lakes", "Managed Warehouses", "Security"],
        },
    },
    {
        "id": "ml-engineer",
        "name": "Machine Learning Engineer",
        "category": "Data & AI",
        "skills": {
            "Machine Learning": ["Training", "Feature Engineering", "Evaluation", "Tuning"],
            "Python": ["NumPy", "Pandas", "Scikit-learn", "Testing"],
            "Deep Learning": ["Neural Networks", "CNNs", "Transformers", "Training"],
            "MLOps": ["Model Registry", "Deployment", "Monitoring", "CI/CD"],
            "Statistics": ["Probability", "Bias Variance", "Confidence", "Experimentation"],
        },
    },
    {
        "id": "ai-engineer",
        "name": "AI Engineer",
        "category": "Data & AI",
        "skills": {
            "Generative AI": ["Prompt Design", "Structured Output", "RAG", "Evaluation"],
            "Python": ["APIs", "Data Processing", "Async", "Testing"],
            "Machine Learning": ["Embeddings", "Classification", "Evaluation", "Deployment"],
            "LLM Applications": ["Tool Calling", "Agents", "Guardrails", "Context Management"],
            "MLOps": ["Monitoring", "Versioning", "Deployment", "Cost Control"],
        },
    },
    {
        "id": "nlp-conversational-ai",
        "name": "NLP / Conversational AI Engineer",
        "category": "Data & AI",
        "skills": {
            "NLP": ["Tokenization", "Embeddings", "Text Classification", "Information Extraction"],
            "Chatbots": ["Intent Detection", "Dialogue Management", "Fallbacks", "Evaluation"],
            "LLMs": ["Prompting", "RAG", "Tool Calling", "Context Windows"],
            "Python": ["Text Processing", "APIs", "Testing", "Data Pipelines"],
        },
    },
    {
        "id": "sql-developer",
        "name": "SQL Developer",
        "category": "Database & BI",
        "skills": {
            "SQL": ["Joins", "CTEs", "Window Functions", "Subqueries", "Optimization"],
            "Database Design": ["Normalization", "Keys", "Constraints", "Relationships"],
            "Transactions": ["ACID", "Isolation", "Locks", "Deadlocks"],
            "Performance": ["Indexes", "Execution Plans", "Query Tuning", "Partitioning"],
        },
    },
    {
        "id": "database-administrator",
        "name": "Database Administrator",
        "category": "Database & BI",
        "skills": {
            "MySQL": ["Indexes", "Backup", "Replication", "Performance"],
            "PostgreSQL": ["Indexes", "Transactions", "Backup", "Replication"],
            "Database Security": ["Users", "Privileges", "Encryption", "Auditing"],
            "High Availability": ["Replication", "Failover", "Backups", "Recovery"],
        },
    },
    {
        "id": "devops-engineer",
        "name": "DevOps Engineer",
        "category": "Cloud & DevOps",
        "skills": {
            "Linux": ["Processes", "Permissions", "Networking", "Shell"],
            "Docker": ["Images", "Containers", "Volumes", "Networking"],
            "CI/CD": ["Pipelines", "Testing", "Deployment", "Rollback"],
            "Git": ["Branching", "Rebase", "Release Flow", "Code Review"],
            "Cloud": ["Compute", "Storage", "Networking", "IAM"],
        },
    },
    {
        "id": "aws-cloud-engineer",
        "name": "AWS Cloud Engineer",
        "category": "Cloud & DevOps",
        "skills": {
            "AWS": ["EC2", "S3", "IAM", "VPC", "Lambda"],
            "Cloud Security": ["IAM", "Encryption", "Least Privilege", "Auditing"],
            "Networking": ["VPC", "Subnets", "Load Balancers", "DNS"],
            "Infrastructure as Code": ["Terraform", "Modules", "State", "Drift"],
        },
    },
    {
        "id": "cybersecurity-analyst",
        "name": "Cybersecurity Analyst",
        "category": "Cybersecurity",
        "skills": {
            "Network Security": ["TCP/IP", "Firewalls", "IDS/IPS", "Segmentation"],
            "Security Monitoring": ["Logs", "SIEM", "Alerts", "Incident Triage"],
            "Web Security": ["OWASP", "Authentication", "Sessions", "Input Validation"],
            "Incident Response": ["Detection", "Containment", "Eradication", "Recovery"],
        },
    },
    {
        "id": "qa-automation-engineer",
        "name": "QA / Automation Engineer",
        "category": "Testing & Quality",
        "skills": {
            "Testing Fundamentals": ["Test Cases", "Boundary Testing", "Regression", "Smoke Testing"],
            "Automation": ["Page Objects", "Locators", "Assertions", "Test Data"],
            "API Testing": ["REST", "Status Codes", "Schemas", "Negative Testing"],
            "Python": ["Pytest", "Fixtures", "Mocks", "Assertions"],
        },
    },
    {
        "id": "ui-ux-designer",
        "name": "UI/UX Designer",
        "category": "Design & Product",
        "skills": {
            "UX Research": ["Interviews", "Personas", "Journey Maps", "Usability Testing"],
            "UI Design": ["Typography", "Color", "Spacing", "Visual Hierarchy"],
            "Figma": ["Components", "Auto Layout", "Prototyping", "Design Systems"],
            "Accessibility": ["Contrast", "Keyboard Navigation", "Semantics", "Inclusive Design"],
        },
    },
    {
        "id": "technical-support-engineer",
        "name": "Technical Support Engineer",
        "category": "IT & Support",
        "skills": {
            "Troubleshooting": ["Root Cause", "Logs", "Reproduction", "Escalation"],
            "Networking": ["DNS", "HTTP", "TCP/IP", "Connectivity"],
            "Linux": ["Processes", "Permissions", "Logs", "Shell"],
            "Customer Communication": ["Clarification", "Empathy", "Documentation", "Incident Updates"],
        },
    },
]

ROLE_BY_ID = {role["id"]: role for role in ROLE_CATALOG}

_DIFFICULTY_TO_AI_LEVEL = {
    "easy": "beginner",
    "medium": "intermediate",
    "hard": "advanced",
}

QUESTION_TYPES = {"mcq", "coding", "conceptual"}

_FALLBACK_QUESTION_TEMPLATES = {
    "conceptual": [
        "For {topic} in {skill}, explain the main problem it solves and give a practical example you would discuss in a {role} interview.",
        "Suppose you are working as a {role}. When would you choose one approach related to {topic} over another, and what trade-off would you consider?",
        "A teammate says they understand {topic} but cannot explain when it matters in production. How would you test their understanding as a {role} candidate?",
        "Describe a common mistake involving {topic}. How would you detect it, debug it, and prevent it from recurring?",
        "How would you explain {topic} to a non-technical stakeholder while keeping the explanation accurate enough for a {role} project?",
        "Give a realistic workplace scenario in which a decision around {topic} affects reliability, performance, cost, or maintainability. Explain your reasoning.",
        "What edge case or failure mode would you check first when implementing something involving {topic} as a {role}?",
        "Compare two common ways of handling {topic}. What criteria would you use to decide between them in a real project?",
        "If an implementation involving {topic} works in development but fails in production, what would you investigate first and why?",
        "What interview follow-up question could expose whether a candidate really understands {topic}, and how would you answer it?",
        "Describe one practical project task where knowledge of {topic} would make a meaningful difference for a {role}.",
        "What limitation or trade-off should an experienced {role} candidate mention when discussing {topic}?",
    ],
    "coding": [
        "Write a small {skill} solution that demonstrates {topic}. Include input validation and explain the time/space trade-off.",
        "You receive messy input while working with {topic}. Write a function or query that handles the main edge cases and explain your approach.",
        "Implement a practical {topic} task that could appear in a {role} interview. State the expected input, output, and one important edge case.",
        "Debug-oriented challenge: create a short solution involving {topic}, then explain the bug or design risk a candidate should watch for.",
        "Build a minimal example using {topic} that solves a realistic workplace problem for a {role}. Explain why your implementation is appropriate.",
        "Write a solution involving {topic} that would still behave correctly when the input is empty, very large, or contains unexpected values.",
        "Create a small interview exercise for {role} that uses {topic}. Include one performance concern the candidate should address.",
        "Write a function, query, or pseudocode solution using {topic}, then describe one test case that could reveal a hidden bug.",
        "Solve a realistic data or application task involving {topic}. Keep the implementation concise and explain the key design decision.",
        "Implement a simple version of a common {topic} operation and then explain how you would improve it for production use.",
    ],
    "mcq": [
        "Which statement best describes the practical purpose of {topic} when working with {skill} as a {role}?",
        "A {role} is debugging a problem involving {topic}. Which action is the most appropriate first step?",
        "Which scenario is the clearest example of using {topic} correctly in a {role} project?",
        "Which trade-off should a {role} consider when choosing an approach related to {topic}?",
        "Which statement about {topic} is most accurate for a {skill}-based interview?",
        "Which outcome would most strongly indicate that {topic} has been implemented correctly?",
        "Which mistake is most likely to cause problems when using {topic} in a real {role} project?",
        "Which option would be the best reason for a {role} to use {topic} rather than a simpler alternative?",
    ],
}


def get_role_catalog():
    """Return a frontend-friendly role/category/skill/topic hierarchy."""
    categories = {}
    for role in ROLE_CATALOG:
        category = categories.setdefault(role["category"], {"id": role["category"].lower().replace(" & ", "-").replace(" ", "-"), "name": role["category"], "roles": []})
        category["roles"].append({
            "id": role["id"],
            "name": role["name"],
            "skills": [
                {"name": skill, "topics": topics}
                for skill, topics in role["skills"].items()
            ],
        })
    return list(categories.values())


def get_role(role_id):
    return ROLE_BY_ID.get((role_id or "").strip().lower())


def _question_hash(role_id, skill, topic, difficulty, question_type, question):
    import hashlib
    raw = "|".join([
        role_id.strip().lower(), skill.strip().lower(), topic.strip().lower(),
        difficulty.strip().lower(), question_type.strip().lower(),
        " ".join(question.lower().split()),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _fallback_question(role, skill, topic, difficulty, question_type, offset=0):
    templates = _FALLBACK_QUESTION_TEMPLATES[question_type]
    template = templates[offset % len(templates)]
    question = template.format(role=role["name"], skill=skill, topic=topic)

    if question_type == "mcq":
        mcq_variants = [
            (
                [
                    f"It addresses a real problem associated with {topic}",
                    f"It removes every possible need for {skill}",
                    "It guarantees perfect production performance in every case",
                    "It is unrelated to the selected role",
                ], "A",
            ),
            (
                [
                    "Inspect the relevant inputs, assumptions, and failure symptoms first",
                    "Immediately rewrite the entire application",
                    "Ignore the error until production",
                    "Remove the selected feature without investigation",
                ], "A",
            ),
            (
                [
                    f"A realistic {role['name']} task where {topic} solves the stated problem",
                    "A task that has no connection to the role",
                    "A scenario where requirements are deliberately ignored",
                    "A situation where no data or input exists",
                ], "A",
            ),
            (
                [
                    "Performance, correctness, maintainability, and context",
                    "Only the number of lines of code",
                    "Only whether the code looks complex",
                    "Whether the approach is popular on social media",
                ], "A",
            ),
            (
                [
                    f"{topic} should be understood in terms of its actual use and trade-offs",
                    f"{topic} makes every other {skill} concept unnecessary",
                    "{topic} always has zero implementation cost",
                    "{topic} never requires testing",
                ], "A",
            ),
            (
                [
                    f"The implementation satisfies its intended {topic} requirements and handles important edge cases",
                    "The implementation has the longest possible code",
                    "The implementation has no tests",
                    "The implementation uses the newest syntax regardless of need",
                ], "A",
            ),
            (
                [
                    f"Ignoring important edge cases or assumptions around {topic}",
                    "Writing a short comment",
                    "Using descriptive variable names",
                    "Testing normal input",
                ], "A",
            ),
            (
                [
                    f"It solves a genuine requirement where {topic} provides a useful advantage",
                    "It makes the project impossible to maintain",
                    "It guarantees no future bugs",
                    "It eliminates the need to understand requirements",
                ], "A",
            ),
        ]
        options, correct = mcq_variants[offset % len(mcq_variants)]
        return {
            "question": question,
            "options": options,
            "correct_option": correct,
            "explanation": f"Option {correct} best addresses the practical interview context for {topic}.",
        }
    if question_type == "coding":
        language = "python" if "python" in skill.lower() or skill in {"Data Processing", "Testing"} else "text"
        return {
            "question": question,
            "starter_code": "# Write your solution here\n",
            "language": language,
            "sample_solution": "# A correct solution should address the stated input, output, validation and edge case requirements.",
            "explanation": f"Focus on a correct, readable implementation of {topic} and explain the trade-offs.",
        }
    return {
        "question": question,
        "model_answer": f"A strong {role['name']} answer should explain what {topic} does, when it is useful in {skill}, and support the explanation with a concrete example.",
        "key_points": ["Define the concept clearly", "Explain when/why it is used", "Give a practical example"],
    }


def _normalize_generated_item(item, role, skill, topic, difficulty, question_type, source="ai"):
    question = (item.get("question") or "").strip()
    if not question:
        return None
    return {
        "role_id": role["id"],
        "role_name": role["name"],
        "skill": skill,
        "topic": topic,
        "difficulty": difficulty,
        "question_type": question_type,
        "question": question,
        "options": item.get("options") or [],
        "correct_option": item.get("correct_option") or None,
        "explanation": item.get("explanation") or "",
        "starter_code": item.get("starter_code") or "",
        "language": item.get("language") or "",
        "sample_solution": item.get("sample_solution") or "",
        "model_answer": item.get("model_answer") or "",
        "key_points": item.get("key_points") or [],
        "source": source,
    }


def get_question_bank_set(role_id, skill, topic, difficulty="medium", count=20, question_type="mixed", user=None):
    """Fetch cached questions and top up with small Gemini batches when needed."""
    from .models import QuestionBankQuestion

    role = get_role(role_id)
    if not role:
        raise ValueError("Unknown job role.")
    if skill not in role["skills"]:
        raise ValueError("Skill is not available for the selected role.")
    if topic not in role["skills"][skill]:
        raise ValueError("Topic is not available for the selected skill.")
    if difficulty not in {"easy", "medium", "hard"}:
        raise ValueError("Difficulty must be easy, medium or hard.")
    if question_type not in QUESTION_TYPES and question_type != "mixed":
        raise ValueError("Question type must be mcq, coding, conceptual or mixed.")

    count = max(1, min(int(count), 20))
    types = ["mcq", "coding", "conceptual"] if question_type == "mixed" else [question_type]

    if question_type == "mixed":
        target_counts = {"mcq": round(count * 0.4), "coding": round(count * 0.3)}
        target_counts["conceptual"] = count - target_counts["mcq"] - target_counts["coding"]
    else:
        target_counts = {question_type: count}

    selected_by_type = {qtype: [] for qtype in types}
    existing_by_type = {qtype: list(
        (QuestionBankQuestion.objects.filter(
            role_id=role["id"], skill=skill, topic=topic,
            difficulty=difficulty, question_type=qtype,
        ).exclude(seen_by=user) if user is not None else QuestionBankQuestion.objects.filter(
            role_id=role["id"], skill=skill, topic=topic,
            difficulty=difficulty, question_type=qtype,
        )).order_by("-created_at")
    ) for qtype in types}

    for qtype in types:
        selected_by_type[qtype] = existing_by_type[qtype][:target_counts[qtype]]

    # Generate missing questions. For a mixed set, use ONE Gemini request and
    # let the model label each item. This is much friendlier to the free tier.
    if question_type == "mixed":
        missing_total = sum(max(0, target_counts[t] - len(selected_by_type[t])) for t in types)
        if missing_total > 0:
            exclusions = [
                q.question
                for qtype_items in existing_by_type.values()
                for q in qtype_items
            ]
            exclusions += [
                q.question
                for qtype_items in selected_by_type.values()
                for q in qtype_items
            ]
            try:
                generated = ai.generate_interview_question_batch(
                    role["name"], skill, topic, _DIFFICULTY_TO_AI_LEVEL[difficulty],
                    "mixed", min(missing_total, 12), exclusions,
                ) or []
            except Exception as exc:
                print("Question-bank Gemini generation failed:", exc)
                generated = []

            for raw in generated:
                generated_type = str(raw.get("question_type") or "conceptual").strip().lower()
                if generated_type not in types:
                    continue
                if len(selected_by_type[generated_type]) >= target_counts[generated_type]:
                    continue
                normalized = _normalize_generated_item(raw, role, skill, topic, difficulty, generated_type, "ai")
                if not normalized:
                    continue
                if generated_type == "mcq" and (len(normalized["options"]) != 4 or normalized["correct_option"] not in {"A", "B", "C", "D"}):
                    continue
                h = _question_hash(role["id"], skill, topic, difficulty, generated_type, normalized["question"])
                if QuestionBankQuestion.objects.filter(question_hash=h).exists():
                    continue
                normalized["question_hash"] = h
                try:
                    obj = QuestionBankQuestion.objects.create(**normalized)
                except Exception as exc:
                    print("Question-bank DB insert skipped:", exc)
                    continue
                selected_by_type[generated_type].append(obj)
    else:
        for qtype in types:
            missing = target_counts[qtype] - len(selected_by_type[qtype])
            if missing <= 0:
                continue
            exclusions = [q.question for qtype_items in existing_by_type.values() for q in qtype_items]
            exclusions += [q.question for qtype_items in selected_by_type.values() for q in qtype_items]
            try:
                generated = ai.generate_interview_question_batch(
                    role["name"], skill, topic, _DIFFICULTY_TO_AI_LEVEL[difficulty],
                    qtype, min(missing, 12), exclusions,
                ) or []
            except Exception as exc:
                print("Question-bank Gemini generation failed:", exc)
                generated = []
            for raw in generated:
                normalized = _normalize_generated_item(raw, role, skill, topic, difficulty, qtype, "ai")
                if not normalized:
                    continue
                if qtype == "mcq" and (len(normalized["options"]) != 4 or normalized["correct_option"] not in {"A", "B", "C", "D"}):
                    continue
                h = _question_hash(role["id"], skill, topic, difficulty, qtype, normalized["question"])
                if QuestionBankQuestion.objects.filter(question_hash=h).exists():
                    continue
                normalized["question_hash"] = h
                try:
                    obj = QuestionBankQuestion.objects.create(**normalized)
                except Exception as exc:
                    print("Question-bank DB insert skipped:", exc)
                    continue
                selected_by_type[qtype].append(obj)

    # If Gemini is unavailable or returns duplicates, fill with deterministic
    # local variations. These are also persisted, so they are not regenerated.
    for qtype in types:
        offset = 0
        existing_hashes = {q.question_hash for q in selected_by_type[qtype]}
        while len(selected_by_type[qtype]) < target_counts[qtype] and offset < 100:
            raw = _fallback_question(role, skill, topic, difficulty, qtype, offset)
            offset += 1
            h = _question_hash(role["id"], skill, topic, difficulty, qtype, raw["question"])
            if h in existing_hashes or QuestionBankQuestion.objects.filter(question_hash=h).exists():
                continue
            normalized = _normalize_generated_item(raw, role, skill, topic, difficulty, qtype, "fallback")
            normalized["question_hash"] = h
            try:
                obj = QuestionBankQuestion.objects.create(**normalized)
                selected_by_type[qtype].append(obj)
                existing_hashes.add(h)
            except Exception:
                pass

    # Interleave types so a mixed practice set feels varied instead of being
    # presented as all MCQs followed by all coding questions.
    selected = []
    while len(selected) < count:
        progressed = False
        for qtype in types:
            if selected_by_type[qtype]:
                selected.append(selected_by_type[qtype].pop(0))
                progressed = True
                if len(selected) >= count:
                    break
        if not progressed:
            break

    data = []
    for q in selected[:count]:
        data.append({
            "id": q.id,
            "role_id": q.role_id,
            "role_name": q.role_name,
            "skill": q.skill,
            "topic": q.topic,
            "difficulty": q.difficulty,
            "question_type": q.question_type,
            "question": q.question,
            "options": q.options or [],
            "correct_option": q.correct_option,
            "explanation": q.explanation or "",
            "starter_code": q.starter_code or "",
            "language": q.language or "",
            "sample_solution": q.sample_solution or "",
            "model_answer": q.model_answer or "",
            "key_points": q.key_points or [],
            "source": q.source,
        })
    if user is not None:
        for item in selected[:count]:
            item.seen_by.add(user)

    return data

def generate_targeted_interview_questions(role_id, skill, topic, difficulty="medium", session_type="mixed", limit=6, user=None):
    """Build a mock interview from the same role/skill/topic hierarchy as the bank."""
    question_type = "mixed"
    if session_type == "mcq":
        question_type = "mcq"
    elif session_type == "technical":
        question_type = "mixed"
    elif session_type == "behavioral":
        # Behavioral mock remains available through the existing job-match flow.
        question_type = "conceptual"

    bank = get_question_bank_set(role_id, skill, topic, difficulty, max(limit, 6), question_type, user=user)
    if not bank:
        return []

    if session_type == "technical":
        ordered = [q for q in bank if q["question_type"] == "coding"] + [q for q in bank if q["question_type"] == "mcq"] + [q for q in bank if q["question_type"] == "conceptual"]
    else:
        ordered = bank

    questions = []
    for q in ordered[:limit]:
        questions.append({
            "question": q["question"],
            "category": "technical" if q["question_type"] != "conceptual" else "situational",
            "question_type": "open" if q["question_type"] == "conceptual" else q["question_type"],
            "related_skill": q["skill"],
            "expected_points": q.get("key_points", []),
            "options": q.get("options", []),
            "correct_option": q.get("correct_option"),
            "starter_code": q.get("starter_code"),
            "language": q.get("language"),
            "sample_solution": q.get("sample_solution"),
            "explanation": q.get("explanation") or q.get("model_answer", ""),
        })
    return questions
